# Example Apache + Gunicorn configuration

Im these exampels, replace `cl8.example.net` with your domain, and `/path/to/constellate` with the path to your constellate installation.
There should be a virtualenv (configured using `pipenv`) in the project root directory, as described in Constellate's [installation](https://github.com/Greening-Digital/constellate/blob/master/docs/installation.md) and [deployment](https://github.com/Greening-Digital/constellate/blob/master/docs/deployment.md) docs.

## Gunicorn systemd config
This config assumes that gunicorn is running only a single application. 
`/etc/systemd/system/gunicorn.service`:
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
# the specific user that our service will run as
User=www-data
Group=www-data
# another option for an even more restricted service is
# DynamicUser=yes
# see http://0pointer.net/blog/dynamic-users-with-systemd.html
#RuntimeDirectory=gunicorn
WorkingDirectory=/path/to/constellate/backend
ExecStart=/usr/local/bin/pipenv run gunicorn --bind unix:/run/gunicorn.sock config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

`/etc/systemd/system/gunicorn.socket`
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
# Our service won't need permissions for the socket, since it
# inherits the file descriptor by socket activation
# only the nginx daemon will need access to the socket
User=www-data
# Optionally restrict the socket permissions even more.
# Mode=600

[Install]
WantedBy=sockets.target
```

## Apache virtual host config

This config requires `mod_ssl`, `mod_rewrite`, `mod_alias`, and `mod_proxy_http` apache modules to be enabled.

For better performance and security, this config sets `AllowOverride none`, so `.htaccess` files will be ignored; if you need to change the config, do so in this file instead and then restart apache to pick up changes.

`/etc/apache/sites-enabled/constellate.conf`:
```
# Port 80 virtual host used to redirct to secure site
# and also to obtain letsencrypt certificates without requiring config changes
<VirtualHost *:80>
    ServerAdmin webmaster@exequo.org
    DocumentRoot /path/to/constellate/frontend/public
    ServerName cl8.example.net
    ErrorLog /var/log/apache2/cl8.example.net.errlog
    CustomLog /var/log/apache2/cl8.example.net.log combined

    # This target directory needs to exist and be writable by apache
    Alias /.well-known/acme-challenge/ /var/www/letsencrypt/.well-known/acme-challenge/

    <Directory "/var/www/letsencrypt/.well-known/acme-challenge">
        Options None
        AllowOverride None
        ForceType text/plain
        Require all granted
    </Directory>

    CheckSpelling On
    <Directory /path/to/constellate/frontend/public>
        Require all granted
    </Directory>
    #Redirect to secure, except for letsencrypt validations
    #Disable the next 3 lines to stop the redirect to secure
    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^.*/\.well-known/.*$ [NC]
    RewriteRule (.*) https://cl8.example.net%{REQUEST_URI}
</VirtualHost>

# Secure virtual host
<VirtualHost *:443>
    ServerAdmin webmaster@exequo.org
    DocumentRoot /path/to/constellate/frontend/public
    ServerName cl8.example.net
    ErrorLog /var/log/apache2/cl8.example.net.errlog
    CustomLog /var/log/apache2/cl8.example.net.log combined
    Protocols h2 http/1.1

    DirectoryIndex index.html
    CheckSpelling On
    <Directory /path/to/constellate/frontend/public>
        Require all granted
    </Directory>

    <Directory /path/to/constellate/backend/staticfiles>
        Require all granted
    </Directory>

    <Directory /path/to/constellate/backend/media>
        Require all granted
    </Directory>

    SSLEngine on
    # These 3 lines will need commenting out until you have obtained certificates for the domain
    SSLCertificateFile /etc/letsencrypt/live/cl8.example.net/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/cl8.example.net/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/cl8.example.net/chain.pem
    Header always set Strict-Transport-Security "max-age=15552000"
    SSLUseStapling on

    # These aliases allow Apache to serve static content directly without going via gunicorn
    Alias /static/ /path/to/constellate/backend/staticfiles/
    Alias /media/ /path/to/constellate/backend/media/
    Alias /favicon.ico /path/to/constellate/backend/staticfiles/images/favicons/favicon.ico

    ProxyPreserveHost On

    #Point all other requests at the gunicorn socket
    <Location />
        RequestHeader set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}
        RequestHeader set "X-Forwarded-SSL" expr=%{HTTPS}
        ProxyPass unix:/run/gunicorn.sock|http://cl8.example.net/
        ProxyPassReverse unix:/run/gunicorn.sock|http://cl8.example.net/
    </Location>

</VirtualHost>
```
