
import json
import requests
from flask import Flask, request

conf = {
    'github_client_id': '<add_client_id_here>',
    'github_client_secret': '<add_client_secret_here>',
    'github_authorize_url': 'https://github.com/login/oauth/authorize',
    'self_repo_url': 'https://github.com/ForksInc/knife',
}

application = Flask(__name__)
state = "<generate_uuid_here>"

@application.route("/")
def hello():
    return '''
    <h1 style='color:blue'>Want to fork the knife repo?</h1>
    <p><a href="{url}?client_id={client_id}&state={state}&scope=repo">Absolutely!</a></p>
    '''.format(url=conf['github_authorize_url'], client_id=conf['github_client_id'], state=state)

@application.route("/authenticated/")
def authenticated():
    try:
        code = request.args['code']
        responded_state = request.args['state']
        if (responded_state != state):
            raise Exception
    except:
        return '''
            <h1>Not Authenticated</h1>
            <p>Oh dear. You've landed on this page with missing or invalid auth data.</p>
            <p>You'll probably want to <a href="/">start over.</a>
        '''
    else:
        success, token = get_token(code)
        if success:        
            success, new_repo_name = fork_repo(token)
            
            if success:
                url = "https://github.com/{path}".format(path=new_repo_name)
                return '''
                <h1 style='color:green'>Ok, cool. It's done.</h1>
                <p>Your fork... <a href="{url}">{url}</a></p>
                '''.format(url=url)

    # fail over to this catch all error output    
    return '''
    <h1 style='color:red'>Oh no.</h1>
    <p>Unfortunately, something went wrong. You can try a few things...</p>
    <ul>
        <li><a href="/">Start over</a></li>
        <li>Use the github native feature: <a href="{self_url}/fork">{self_url}/fork</a></li>
    </ul>
    '''.format(self_url=conf['self_repo_url'])       

def get_token(code):
    url = "https://github.com/login/oauth/access_token"
    data = {
        'client_id': conf['github_client_id'],
        'client_secret': conf['github_client_secret'],
        'code': code,
        'state': "jkhkjh"
    }
    headers = {'Accept': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    try:
        return True, json.loads(response.text)['access_token']
    except:
        return False, ''

def fork_repo(token):
    url = "https://api.github.com/repos/ForksInc/knife/forks"
    headers = {"Authorization": "token %s" % token}
    response = requests.post(url, headers=headers)
    if (response.status_code == 202):
        return True, json.loads(response.text)['full_name']
    else:
        return False, response.status_code

if __name__ == "__main__":
    application.run()