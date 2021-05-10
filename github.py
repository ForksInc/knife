import json
import requests
from settings import conf

"""A set of connectors for the github api which utilizes oauth to authenticate the end user."""

def get_token(code):
    """Given an authentication code from the oauth web flow, retrieve the user's access token."""
    data = {
        'client_id': conf['github_client_id'],
        'client_secret': conf['github_client_secret'],
        'code': code,
        'state': conf['state']
    }
    headers = {'Accept': 'application/json'}
    response = requests.post("https://github.com/login/oauth/access_token", data=data, headers=headers)
    try:
        # attempt to return the access token
        return True, json.loads(response.text)['access_token']
    except Exception:
        # gobble all errors and return false (user will be given options)
        return False, ''

def fork_repo(token, repo_path):
    """Given a valid authentication token and a repo path, create a fork in the user's account."""
    headers = {"Authorization": "token %s" % token}
    response = requests.post("https://api.github.com/repos/{path}/forks".format(path=repo_path), headers=headers)
    if (response.status_code == 202):
        # return full_name, which is the name of the new repo (to be used with the github main url to link to it)
        return True, json.loads(response.text)['full_name']
    else:
        # return false for anything but a 202 (user will be given options)
        return False, response.status_code