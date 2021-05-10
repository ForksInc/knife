from flask import Flask, request, render_template
from github import get_token, fork_repo
from settings import conf

application = Flask(__name__)

@application.route("/")
def hello():
    """Root endpoint, renders the home.html template to allow the user to click the lone link."""
    return render_template('home.html', url=conf['github_authorize_url'], client_id=conf['github_client_id'], state=conf['state'])


@application.route("/authenticated/")
def authenticated():
    """Callback/landing page from github auth flow. Retrieves an access token and attempts to fork the repo."""
    try:
        code = request.args['code']
        
        # check for state mismatch (given vs provided)
        responded_state = request.args['state']
        if (responded_state != conf['state']):
            raise Exception

    except Exception:
        # auth fail covers missing code, missing state, or state mismatch (and any other errors)
        return render_template('auth_fail.html')
    
    else:
        # authenticated = actually retrieved a token
        authenticated, token = get_token(code)
        if authenticated:     
            print("AUTHENTICATED")   

            # once a valid token has been retrieved, fork the repo
            success, new_repo_name = fork_repo(token, 'ForksInc/knife')
            if success:
                # if the repo create was successful, render the done template and present the repo url to the user 
                url = "https://github.com/{path}".format(path=new_repo_name)               
                return render_template('done.html', url=url)

    # fail over to this catch-all error output    
    return render_template('error.html', self_url=conf['self_repo_url'])      

if __name__ == "__main__":
    application.run()