# Supported ways to sign in with Constellate

Constellate supports sign in via three routes:

1. **username /password** - this is mainly used for admin users
2. email "passwordless" - this is the primary route if you don't have slack set up
3. sign in via slack - this is for workspaces that have installed a corresponding slack app


## Username and password

This is 

## Email passwordless



### What I need to do is subclass the `DefaultSocialAccountAdapter`, 

```
SocialAccountAdapter(DefaultSocialAccountAdapter)
```


and then the  `SlackOpenIdConnectProvider`, implementing the following methods

extract_uid(self, data):
extract_common_fields(self, data):
extract_extra_data(self, data):
extract_email_addresses(self, data):



### Slack

When you sign in , you are sent to the slack.com website.

https://github.com/pennersr/django-allauth/pull/1410/files

the oauthloginvieew needs to redirect to 

`/openid/connect/authorize`, but it currently redirects to `https://slack.com/oauth/authorize`

Sign in with your credentials.



Then your details need to be passed along to the profile or user, using `extract_common_fields` and the `populate_user` on the SOCIALACCOUNT_ADAPTER





### How the slack log in works

A request comes in for slack endpoint on django app

User is redirected to slack with a `/openid/connect/authorize`

User POSTS back to django app endpoint, `/accounts/slack_openid_connect/login/callback/?code=153694826117.5382992184355.542eeb49d73ed7313dadd1ef43071e79ddd9dc891661be0c69be03a8c1b7e5d1&state=1vZ4VSAWucSg`


Once back you are directed to the `oauth2_callback` view

This then leads to the calling `complete_social_login` dance. 

This calls the signal, and the `pre_social_login` method, but if we want to integrate properly, we need to create and store the social signins and the rest

Which eventually ends with

`complete_social_signup`











### how allauth works

Allauth has the notion of a social account wgich is linked to a single user, and an email address, which is _also_ linked to a single user.

becauase these only ever link to a single user, if you have the social account, or recognise the email account you can follow the link to the user.

#### signing in

When you sign in, you get back the data for a social account, that also has email addresses. 



To log you in, a subclass of the OAuth2CallbackView calls `dispatch` on the code request, which calls the `complete_login` methods on your chosen adapter. This delegates to the provider associated with that specific adapter. 

So the `OAuth2Adapter` adapter *view*, calls `complete_login` on the the *adapter*, which calls further detailed methods on the *provider*, for pulling out the sociallogin info from the data sent to the callback. This provider class is responsible for pulling out usernames, uids, email addresses and so on, but not saving anything.

Finally, the OAuth2CallbackView, finishes the sign-in process, now that it has an instantied user and social login by calling the method `complete_social_login`.

Inside there, for a new user we end up calling `save_user()`, via the helper `_process_signup` method in `complete_social_login`. By default, this will create:

1. a `User` in the database, with no real info
2. a `SocialAccount` object in the database, linking to the user, and containing the stored data from the oauth callback
3. an `EmailAddress` object in the database linking to the user

there is a separate `user_signed_up` signal triggered we can listen to, for making further changes, as well as `pre_login`, and `post_login`


#### signing up


This is our chance to save user info, populating it with sensible names, but this is mainly concerned with saving our sociallogin, and having a link 

This method contains the code for persisting information to a database, via 



The SlackOpenIdConnectAdapter adapter view, called `complete_login`, which delegates to your chosen provider.


Your provider calls `sociallogin_from_response`, and inside that there is logic to instantiate the EmailAddress for a given user, and a sociallogin, 

At this point, you have an unsaved `socialaccount`, and `emailaddresses`, but no link back to a user in our system.

That comes when we create a `SocialLogin`, passing in our email address and our social account. A sociallogin "Represents a social user that is in the process of being logged in."

The code in DefaultSocialAccountAdapter, determines how a user is created or fetched, based on the returned info.

complete_social_login

when we have a new_user, we instead the new user using the basic `get_user_model` method





```json
{
    'ok': True,
    'sub': 'UCM06DU1K',
    'https://slack.com/user_id': 'UCM06DU1K',
    'https://slack.com/team_id': 'T4HLEQA3F',
    'email': 'chris@productscience.co.uk',
    'email_verified': True,
    'date_email_verified': 1621952515,
    'name': 'Chris Adams',
    'picture': 'https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_512.jpg',
    'given_name': 'Chris',
    'family_name': 'Adams',
    'locale': 'en-US',
    'https://slack.com/team_name': 'ClimateAction.tech',
    'https://slack.com/team_domain': 'climate-tech',
    'https://slack.com/user_image_24': 'https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_24.jpg',
    'https://slack.com/user_image_32': 'https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_32.jpg',
    'https://slack.com/user_image_48': 'https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_48.jpg',
    'https://slack.com/user_image_72': 'https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_72.jpg',
    'https://slack.com/user_image_192': 'https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_192.jpg',
    'https://slack.com/user_image_512': 'https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_512.jpg',
    'https://slack.com/user_image_1024': 'https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_1024.jpg',
    'https://slack.com/team_image_34': 'https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_34.png',
    'https://slack.com/team_image_44': 'https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_44.png',
    'https://slack.com/team_image_68': 'https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_68.png',
    'https://slack.com/team_image_88': 'https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_88.png',
    'https://slack.com/team_image_102': 'https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_102.png',
    'https://slack.com/team_image_132': 'https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_132.png',
    'https://slack.com/team_image_230': 'https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_230.png',
    'https://slack.com/team_image_default': False
}
```



References

https://django-allauth.readthedocs.io/en/latest/advanced.html#customizing-providers
https://speakerdeck.com/tedtieken/signing-up-and-signing-in-users-in-django-with-django-allauth?slide=78



# Why was this failing?

there was already a chris in the system from the earlier import.

this meant that the sign up process was failing becuase when it encountered a user with the same email address it would redirect the user to sign up with a new user name instead of trying to find the correct user.

it did this because it assumed the email could not be trusted.


