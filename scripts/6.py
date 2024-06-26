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
def upload_file():
    if request.method == 'POST':
            print(2222)
            return redirect(url_for('home' ))
    return '''
    <!doctype html>
<form method=post enctype=multipart/form-data>
    <div>
        <input type="text" id="first-name" placeholder="First Name" name="first-name"autoComplete="first-name" required />
    </div>
    <div>
        <input type="text" id="last-name" placeholder="Last Name" name="last-name" autoComplete="last-name" required />
    </div>
    <div>
        <input type="email" id="email" placeholder="Email"name="email" autoComplete="email" required />
    </div>
    <div>
        <input type="phone" id="phone" placeholder="Phone Number" name="phone" autoComplete="phone" required />
    </div>                
    <div>
        <input type="company" id="company" placeholder="Company" name="company" autoComplete="company" required />
    </div>
    <div>
    <textarea id="message" placeholder="Company"  name="message" rows="5" cols="33"></textarea>
    </div>
      <input type=submit value=Upload>
</form>
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
