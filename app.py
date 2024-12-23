from flask import Flask, render_template, request, redirect, url_for, jsonify, flash ,session
app = Flask(__name__ , static_folder="static")
app.secret_key = "your_secret_key"  # Needed for flash messages

users = { }
userslogout={ "username": "N/A",
            "password": "N/A",
            "email": "N/A",
            "phone": "N/A",
            "courses": "N/A",}
@app.route("/")
def home():
    return render_template("/index.html")


@app.route("/index.html")
def homme():
        return render_template("/index.html")



@app.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]

        if username in users:
            flash("Username already taken", "error")
            return redirect(("/register.html"))
        if any(user["email"] == email for user in users.values()):
            flash("Email already taken", "error")
            return redirect(("/register.html"))
        
        # Save user
        users[username] = {
            "username": username,
            "password": password,
            "email": email,
            "phone": phone,
            "courses": "N/A",
        }
        flash("Registered successfully!", "success")
        return redirect(("/login.html"))
    return render_template("register.html")



@app.route("/login.html",  methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session['username'] = username 
            flash("Logged in successfully!", "success")
            return redirect(url_for("profile", username=username))
    
        flash("Invalid credentials", "error")
        return redirect(("/login.html"))
    return render_template("login.html")


@app.route('/profileunsignned.html',methods=["GET", "POST"])
def profileunsignned():
    # Check if the user is logged in
    if 'username' in session:
        # Get the logged-in user data
        username = session['username']
        user = users.get(username)
        return render_template("profileunsignned.html", user=user)
    else:
        # No user logged in, pass None to the template
        return render_template("profileunsignned.html", user=userslogout)




@app.route('/profile/<username>')
def profile(username):
    if 'username' in session and session['username'] == username:
        return render_template('profile.html',user=users[username])
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.pop('username', None)
    # Flash a message or just redirect the user to the login page or home page
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))  # Redirect to login or home page



@app.route('/enroll_course', methods=['POST'])
def enroll_course():
    if 'username' not in session:
        flash("You must be logged in to enroll in a course.", "error")
        return redirect(url_for('login'))  # Redirect to login if not logged in

    username = session['username']
    course = request.json.get('course')

    if not course:
        flash("No course provided.", "error")
        return redirect(url_for('pricing'))

    # If the user is already enrolled in the same course, do nothing
    if users[username]["courses"] == course:
        flash(f"You are already enrolled in the {course}.", "info")
        return redirect(url_for('pricing'))

    # Replace the old course with the new one
    users[username]["courses"] = course
    flash(f"Successfully enrolled in the {course}!", "success")

    return redirect(url_for('profileunsignned', username=username))




@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/class.html")
def classs():
    return render_template("class.html")



@app.route("/trainers.html")
def trainers():
    return render_template("trainers.html")


@app.route("/pricing.html")
def pricing():
    return render_template("pricing.html")




@app.route("/contact_us.html")
def contact_us():
    return render_template("contact_us.html")



if __name__ == "__main__":
    app.run(debug=True)
