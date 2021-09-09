from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "i292ijeheekei"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.String(100), default=str(datetime.now())[:-7])
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.sno} - {self.title} - {self.desc}"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    todos = db.relationship("Todo")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        todo = Todo(
            title=request.form["title"], desc=request.form["desc"], user_id=current_user.id)
        if todo.title and todo.desc:
            db.session.add(todo)
            db.session.commit()
            flash("A todo was added", 'success')
        else:
            flash("Title and Description can't be empty.", "danger")
    return render_template("index.html", user=current_user)


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect("/")
    return render_template('update.html', todo=todo, user=current_user)


@app.route('/search', methods=['GET', 'POST'])
def search():
    todos = None
    if request.method == "POST":
        user = current_user
        print(current_user)
        todos_list = []
        input = request.form["search"].lower()
        todos = user.todos
        for todo in todos:
            if input in todo.title.lower() or input in todo.desc.lower():
                todos_list.append(todo)
        if not todos_list:
            flash('No results Found! ', 'info')
            return render_template('search.html', todos=todos_list, user=current_user)
        else:
            return render_template('search.html', todos=todos_list, user=current_user)

    return render_template("search.html", todos=todos, user=current_user)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    #flash(f"{todo} was deleted.")
    todos = Todo.query.all()
    return redirect("/")


def validate(name, email, password, confirm_password):
    c = 4
    user = User.query.filter_by(email=email).first()
    if user:
        flash(f"Email already been used!", "danger")
        return False
    if len(name) < 2:
        flash(f"Username can't be less than 2 characters", "danger")
        c -= 1
    if len(email) < 4:
        flash(f"Email can't be less than 4 characters", "danger")
        c -= 1
    if len(password) < 8:
        flash(f"Password must be of 8 characters",  "danger")
        c -= 1
    if confirm_password != password:
        flash(f"Password must match with confirm password", "danger")
        c -= 1

    if c == 4:
        return True

    else:
        return False


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("Congratulations! Successfully logged in!", "success")
                    login_user(user, remember=True)
                    return redirect("/")
                else:
                    flash("Password or may be incorrect!", "danger")
                    return redirect("/login")
            else:
                flash("Email may be incorrect!", "danger")
                return redirect("/login")
        else:
            flash("Enter email and password to login!", "warning")
            return redirect("/login")
    else:
        return render_template('login.html', user=current_user)


@app.route("/logout",  methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully !", "success")
    return redirect("login")


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm_password")
        if validate(name, email, password, confirm_pass):
            new_user = User(name=name, email=email, password=generate_password_hash(
                password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created for {name}", "success")
            login_user(new_user, remember=True)
            return redirect("/")
        else:
            pass

    return render_template('sign_up.html', user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
