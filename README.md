# knife
Knife

## Prereqs
* Python 3.x
* Flask `pip3 install flask` (on many platforms) 
* Requests `pip3 install requests` (on many platforms)

## References
* https://docs.github.com/en/developers/apps/authorizing-oauth-apps
* https://github.com/settings/applications/new
* https://docs.github.com/en/developers/apps/scopes-for-oauth-apps#available-scopes
* https://docs.github.com/en/rest/reference/repos#forks

## To set up and run locally
* go here and create a new app: https://github.com/settings/applications/new
* obtain client id and client secret
* add `github_client_id`, `github_client_secret`, and a unique `state` to your conf (around line 6 of [knife.py])
* install prereqs
* run `python3 knife.py`


