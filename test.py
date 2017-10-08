import json
from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
app = Flask(__name__)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

class User(UserMixin):

    def __init__(self, id):
        self.id = id
        with open('users.json') as jsonfile:
            data = json.load(jsonfile)
            self.name = data[str(id)]['name']
            self.password = data[str(id)]['password']
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

leaderboard = []

davide = {}
davide['name'] = 'Davide'
davide['score'] = 20
leaderboard.append(davide)

pawel = {}
pawel['name'] = 'Pawel'
pawel['score'] = 10
leaderboard.append(pawel)

mark = {}
mark['name'] = 'Mark'
mark['score'] = 1
leaderboard.append(mark)

sven = {}
sven['name'] = 'Sven'
sven['score'] = -5
leaderboard.append(sven)

wille = {}
wille['name'] = 'Wille'
wille['score'] = -15
leaderboard.append(wille)

cook = davide
eaters = ["Pawel", "Mark", "Sven"]

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route("/")
@login_required
def index():
    return render_template('index.html', leaderboard=leaderboard, cook=cook, eaters=eaters)

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        jsonfile = open('users.json')
        data = json.load(jsonfile)
        for i in range(1, 1 + int(data['nofusers'])):
            if data[str(i)]['name'] == username and data[str(i)]['password'] == password:
                id = i
                jsonfile.close()
                user = User(id)
                login_user(user)
                return redirect(request.args.get("next"))
        jsonfile.close()
        return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)