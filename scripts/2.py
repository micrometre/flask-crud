from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    email = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
with app.app_context():
    db.create_all()

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))   

@app.route('/test', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
            email = request.form['email']
            new_todo = Todo(title=email, complete=False)
            db.session.add(new_todo)
            db.session.commit()
            print(email)
            return redirect(url_for('message' ))
    return '''
    <!doctype html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">
    <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"></script>
</head>
<div style="margin-top: 50px;" class="ui container">
        <form class="ui form"  method=post>
            <div class="field">
                <label>Todo Title</label>
                <input type="email" id="email" placeholder="Email"name="email" autoComplete="email" required />
            </div>
            <button class="ui blue button" type="submit">Add</button>
        </form>
        <hr>
        <div class="ui segment">
            <p class="ui big header"></p>
            <span class="ui gray label">Not Complete</span>
            <span class="ui green label">Completed</span>
            <a class="ui blue button" href="/update/">Update</a>
            <a class="ui red button" href="/delete/">Delete</a>
        </div>
</div>

    '''




@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)






@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
