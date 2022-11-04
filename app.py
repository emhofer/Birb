from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded - from CS50 finance
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies) - from CS50 finance
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database - from CS50 finance
db = SQL("sqlite:///project.db")


# From CS50 finance
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    # Get following
    rows = db.execute("SELECT following FROM follows WHERE follower = ?", session["username"])
    # Use list comprehension - https://www.w3schools.com/python/python_lists_comprehension.asp
    follows = [x["following"] for x in rows]
    follows.append(session["username"])

    # Get followers
    rows3 = db.execute("SELECT follower FROM follows WHERE following = ?", session["username"])

    return render_template("index.html", following=rows, followers=rows3)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Route via POST
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM accounts WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # Route via GET
    else:
        return render_template("login.html")


# From CS50 finance
@app.route("/logout")
@login_required
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Route via POST
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM accounts WHERE username = ?", request.form.get("username"))

        # Ensure username does not exist yet
        if len(rows) != 0:
            flash("Username already exists")
            return render_template("register.html")

        # Ensure password meets requirements
        elif len(request.form.get("password")) < 5 or not any(map(str.isdigit, request.form.get("password"))):
            flash("Password must be at least 5 characters long and include a number")
            return render_template("register.html")

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match")
            return render_template("register.html")

        # Create user in database
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        rows = db.execute("INSERT INTO accounts (username, hash) VALUES (?, ?)", username, password)

        flash("Success")
        return redirect("/login")

    # Route via GET
    else:
        return render_template("register.html")


@app.route("/delete", methods=["POST"])
@login_required
def delete():

    # Remove user account from database
    rows = db.execute("DELETE FROM accounts WHERE id = ?", session["user_id"])

    # Remove user chirps from database
    rows2 = db.execute("DELETE FROM chirps WHERE username = ?", session["username"])

    # Remove user follows from database
    rows3 = db.execute("DELETE FROM follows WHERE follower = ? OR following = ?", session["username"], session["username"])

    # Remove user likes from database
    rows4 = db.execute("DELETE FROM likes WHERE userid = ?", session["user_id"])

    return redirect("/logout")


@app.route("/chirp", methods=["POST"])
@login_required
def chirp():

    # Get text input
    chirp = request.form.get("chirp")

    # Record chirp in database
    rows = db.execute("INSERT INTO chirps (username, text) VALUES (?, ?)", session["username"], chirp)

    return redirect("/")


@app.route("/search")
@login_required
def search():

    # Get search term
    q = request.args.get("q")

    # Search accounts and chrips containing search term
    accounts = db.execute("SELECT username FROM accounts WHERE username LIKE ? ORDER BY username ASC", "%" + q + "%")
    chirps = db.execute("SELECT id, username, text FROM chirps WHERE text LIKE ? OR username LIKE ? ORDER BY timestamp DESC", "%" + q + "%", "%" + q + "%")

    # Get likes
    rows4 = db.execute("SELECT * FROM likes WHERE userid = ?", session["user_id"])
    likes = [x["chirpid"] for x in rows4]

    return render_template("search.html", accounts=accounts, chirps=chirps, likes=likes)


@app.route("/follow", methods=["POST"])
@login_required
def follow():

    # Get username to follow
    username = request.form.get("username")

    # Record follow in database
    rows = db.execute("INSERT INTO follows (follower, following) VALUES (?, ?)", session["username"], username)

    return redirect(request.referrer)


@app.route("/unfollow", methods=["POST"])
@login_required
def unfollow():

    # Get username to unfollow
    username = request.form.get("username")

    # Delete follow from database
    rows = db.execute("DELETE FROM follows WHERE follower = ? AND following = ?", session["username"], username)

    return redirect(request.referrer)


@app.route("/profile")
@login_required
def profile():

    # Get username
    user = request.args.get("name")

    # Get followingthem
    rows = db.execute("SELECT following FROM follows WHERE follower = ?", session["username"])
    followingthem = [x["following"] for x in rows]

    # Get following
    rows2 = db.execute("SELECT following FROM follows WHERE follower = ?", user)

    # Get followers
    rows3 = db.execute("SELECT follower FROM follows WHERE following = ?", user)


    return render_template("profile.html", user=user, followingthem=followingthem, following=rows2, followers=rows3)


@app.route("/like", methods=["POST"])
@login_required
def like():

    # Get chirp to like
    chirp = request.form.get("chirp")

    # Record like in database
    rows = db.execute("INSERT INTO likes (userid, chirpid) VALUES (?, ?)", session["user_id"], chirp)

    return redirect(request.referrer)


@app.route("/unlike", methods=["POST"])
@login_required
def unlike():

    # Get chirp to unlike
    like = request.form.get("like")

    # Delete like form database
    rows = db.execute("DELETE FROM likes WHERE chirpid = ? AND userid = ?", like, session["user_id"])

    return redirect(request.referrer)


@app.route("/feed")
@login_required
def feed():

    # Get following
    rows = db.execute("SELECT following FROM follows WHERE follower = ?", session["username"])
    follows = [x["following"] for x in rows]
    follows.append(session["username"])

    # Get chirp feed
    rows2 = db.execute("SELECT id, username, text FROM chirps WHERE username IN (?) ORDER BY timestamp DESC", follows)

    # Get likes
    rows4 = db.execute("SELECT * FROM likes WHERE userid = ?", session["user_id"])
    likes = [x["chirpid"] for x in rows4]

    return render_template("feed.html", feed=rows2, likes=likes)


@app.route("/likes")
@login_required
def likes():

    # Get user whose profile is shown
    username = request.args.get("username")
    userid = db.execute("SELECT id FROM accounts WHERE username = ?", username)[0]["id"]

    # Get like for user whose profile is shown
    likes = db.execute("SELECT chirps.id, chirps.username, chirps.text FROM chirps INNER JOIN likes ON chirps.id=likes.chirpid WHERE likes.userid = ? ORDER BY chirps.timestamp DESC", userid)

    return render_template("likes.html", likes=likes, userid=userid)


@app.route("/chirps")
@login_required
def chirps():

    # Get user whose profile is shown
    username = request.args.get("username")

    # Get chirps for user whose profile is shown
    feed = db.execute("SELECT id, username, text FROM chirps WHERE username = ? ORDER BY timestamp DESC", username)

    # Get likes
    rows4 = db.execute("SELECT * FROM likes WHERE userid = ?", session["user_id"])
    likes = [x["chirpid"] for x in rows4]

    return render_template("chirps.html", feed=feed, likes=likes)

@app.route("/deleteChirp", methods=["POST"])
@login_required
def deleteChirp():

    # Get chirp id to delete
    delete = request.form.get("delete")

    # Delete chirp by id
    rows = db.execute("DELETE FROM chirps WHERE id = ?", delete)

    return redirect(request.referrer)

@app.route("/change")
@login_required
def change():

    return render_template("change.html")

@app.route("/changeuser", methods=["POST"])
@login_required
def changeuser():

    # Get new username
    newuser = request.form.get("username")

    # Query database for username
    rows = db.execute("SELECT * FROM accounts WHERE username = ?", newuser)

    # Ensure username does not exist yet
    if len(rows) != 0:
        flash("Username already exists")
        return render_template("change.html")

    # Update database with new user
    rows2 = db.execute("UPDATE accounts SET username = ? WHERE id = ?", newuser, session["user_id"])
    rows3 = db.execute("UPDATE chirps SET username = ? WHERE username = ?", newuser, session["username"])
    rows4 = db.execute("UPDATE follows SET follower = ? WHERE follower = ?", newuser, session["username"])
    rows5 = db.execute("UPDATE follows SET following = ? WHERE following = ?", newuser, session["username"])

    # Set new session username
    session["username"] = newuser

    flash("Username changed successfully")
    return redirect("/")

@app.route("/changepassword", methods=["POST"])
@login_required
def changepassword():

    # Get old and new passwords
    oldpass = request.form.get("oldpassword")
    newpass = request.form.get("newpassword")
    newpassconfirm = request.form.get("confirmpassword")

    # Query database for password
    rows = db.execute("SELECT hash FROM accounts WHERE id = ?", session["user_id"])

    # Ensure username exists and password is correct
    if not check_password_hash(rows[0]["hash"], oldpass):
        flash("Old password is wrong")
        return render_template("change.html")

    # Ensure password meets requirements
    elif len(newpass) < 5 or not any(map(str.isdigit, newpass)):
        flash("New password must be at least 5 characters long and include a number")
        return render_template("change.html")

    # Ensure password and confirmation match
    elif newpass != newpassconfirm:
        flash("New passwords do not match")
        return render_template("change.html")

    # Update password
    password = generate_password_hash(newpass, method='pbkdf2:sha256', salt_length=8)
    rows = db.execute("UPDATE accounts SET hash = ? WHERE id = ?", password, session["user_id"])
    flash("Password changed successfully")
    return redirect("/")