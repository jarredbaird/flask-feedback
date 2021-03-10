from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import NewUserForm, LoginForm, AddFeedbackForm, EditFeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = "thebestkeyofalltime!!!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

debug = DebugToolbarExtension(app)


""" PART 3: MAKE ROUTES FOR USERS """
# GET /
@app.route('/')
def go_to_register():
    return redirect('/register')

# GET /register
# POST /register
@app.route('/register', methods=["GET", "POST"])
def register():
    form = NewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username=username,
                                 pwd=password, 
                                 email=email, 
                                 first=first_name, 
                                 last=last_name)
        flash(f"Welcome {username}! You have successfully registered")
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.username
        return redirect(f'/users/{username}')
    
    else:
        return render_template('register.html', form=form)

# GET /login
# POST /login
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.authenticate(username=username, pwd=password):
            session['user_id'] = username
            flash(f"Welcome back {username}!")
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Wrong creds"]
        
    return render_template('login.html', form=form)

# GET /secret
@app.route('/secret')
def render_secret():
    try:
        return render_template('secret.html')
    except KeyError:
        flash("Please login or register first ;(")
        return redirect('/register')

""" PART 5: LOG OUT USERS """
# GET /logout
@app.route('/logout', methods=["GET"])
def logout():
    session.pop('user_id')
    return redirect('/register')

""" PART 6: LET'S CHANGE /secret TO /users/<username> """
# # GET /users/<username>
# @app.route('/users/<username>')
# def display_user(username):
#     try:
#         if session['user_id'] == username:
#             user = User.query.get_or_404(username)
#             return render_template('user.html', user=user)
#     except KeyError:
#         flash("Please login or register first ;(")
#         return redirect('/register')

""" PART 8: MAKE/MODIFY ROUTES FOR USERS AND FEEDBACK """
# GET /users/<username>
@app.route('/users/<username>')
def display_user(username):
    try:
        if session['user_id'] == username:
            user = User.query.get_or_404(username)
            fb = Feedback.query.all()
            return render_template('user.html', user=user, fb=fb)
        else:
            flash(f"You are {session['user_id']}, not {username}. Stay in your lane!")
            return redirect(f"/users/{session['user_id']}")
    except KeyError:
        flash("Please login or register first ;(")
        return redirect('/register')

# POST /users/<username>/delete
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    try:
        if session['user_id'] == username:
            user = User.query.filter_by(username=username).first()
            db.session.delete(user)
            session.pop("user_id")
            db.session.commit()
            return redirect('/')
        else:
            flash(f"You are {session['user_id']}. Why are you trying to delete {username}?!")
            redirect(f"/users/{session['user_id']}")
    except KeyError:
        flash("Please login or register first ;(")
        return redirect('/register')
# GET /users/<username>/feedback/add
@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    form = AddFeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        try:
            if session['user_id'] == username:
                fb = Feedback(title=title, content=content, username=username)
                db.session.add(fb)
                db.session.commit()
                return redirect(f'/users/{username}')
            else:
                flash(f"Stop trying to add content under {username}!")
                redirect(f"/users/{session['user_id']}")
        except KeyError:
            flash("Please login or register first ;(")
            return redirect('/register')
    else:
        try:
            if session['user_id'] == username:
                user = User.query.filter_by(username=username).first()
            else:
                flash(f"Stop trying to add content under {username}!")
                redirect(f"/users/{session['user_id']}")
        except KeyError:
            flash("Please login or register first ;(")
            return redirect('/register')
        return render_template('add_feedback.html', user=user, form=form)

@app.route('/feedback/<int:fb_id>/update', methods=["POST", "GET"])
def update_feedback(fb_id):
    try:
        if session['user_id']:
            fb = Feedback.query.filter_by(fb_id=fb_id).first()
            if not fb:
                flash(f"feedback id {fb_id} does not exist")
                return redirect(f"/users/{session['user_id']}")
            print(f"session user: {session['user_id']}, feedback user: {fb.username}")
        if session['user_id'] != fb.username:
            flash("Stop trying to update someone else's feedback!")
            return redirect(f"/users/{session['user_id']}")
    except KeyError:
            flash("Please login or register first ;(")
            return redirect('/register')
    form = EditFeedbackForm()
    title = form.title.data
    content = form.content.data
    if form.validate_on_submit():
        if title and title != fb.title:
            fb.title = title
        if content and content != fb.content:
            fb.content = content
        db.session.add(fb)
        db.session.commit()
        flash(f"Feedback title '{fb.title}' has been updated")
        return redirect(f"/users/{session['user_id']}")

    else:
        return render_template('edit_feedback.html', fb=fb, form=form)

@app.route('/feedback/<int:fb_id>/delete', methods=["POST"])
def delete_feedback(fb_id):
    try:
        if session['user_id']:
            fb = Feedback.query.filter_by(fb_id=fb_id).first()
            if not fb:
                flash(f"feedback id {fb_id} does not exist")
                return redirect(f"/users/{session['user_id']}")
            print(f"session user: {session['user_id']}, feedback user: {fb.username}")
        if session['user_id'] != fb.username:
            flash("Stop trying to update someone else's feedback!")
            return redirect(f"/users/{session['user_id']}")
    except KeyError:
        flash("Please login or register first ;(")
        return redirect('/register')
    del_fb = Feedback.query.filter_by(fb_id=fb_id).first()
    title = del_fb.title
    db.session.delete(del_fb)
    db.session.commit()
    flash(f"Feedback titled '{title}' has been pwned")
    return redirect(f"/users/{session['user_id']}")