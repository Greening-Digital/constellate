# Supported ways to sign in with Constellate

Constellate supports sign in via three routes:

1. **username /password** - this is mainly used for admin users
2. **sign in via slack** - this is for workspaces that have installed a corresponding slack app
3. email "passwordless" - this route works as an alternative, and has working API endpoints but no UI implemented

## Username and password

As you would expect. Accessible at `/admin`


## Slack

If the constellation you're signing into is linked to a slack workspace, you can sign in using your slack login.


## Email passwordless

_There is an API, but the form is a work in progress, sorry_

You enter the email you provided when joining the constellation.

An email is sent to the address you signed up with, listing a code.

You enter a code, and you are logged in.

The following views are available

```
/auth-token/    rest_framework.authtoken.views.ObtainAuthToken
/auth/email/    cl8.users.api.passwordless_views.ConstellateEmailCallbackToken  auth_email
/auth/token/    cl8.users.api.passwordless_views.ConstellateObtainAuthTokenFromCallbackToken    auth_token
/auth/verify/   drfpasswordless.views.VerifyAliasFromCallbackToken      verify_token
/auth/verify/email/     drfpasswordless.views.ObtainEmailVerificationCallbackToken      verify_email
```




---
