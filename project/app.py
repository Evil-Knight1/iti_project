from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# todo class


class Todo(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # this means we want to have a unique value for each item
    title = db.Column(db.String(100))  # the max chars is 100
    complete = db.Column(db.Boolean, default=False)


@app.route("/")
def index():
    # show all todo
    todo_list = Todo.query.all()
    total_todo = Todo.query.count()
    uncmlt_cnt = Todo.query.filter_by(complete=False).count()
    cmlt_cnt = Todo.query.filter_by(complete=True).count()
    print(todo_list)
    return render_template(
        "dashboard/index.html",
        **locals(),
        # todo_list=todo_list,
        # total_todo=total_todo,
        # cmlt_cnt=cmlt_cnt,
        # uncmlt_cnt=uncmlt_cnt,
    )


@app.route("/about")
def about():
    return render_template("dashboard/about.html")


@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


# update
@app.route("/update/<int:id>")
def update(id):
    # add new item
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))


# delete
@app.route("/delete/<int:id>")
def delete(id):
    # add new item
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
