from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pandas as pd
app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    company = db.Column(db.String(100))
    message = db.Column(db.String)
    complete = db.Column(db.Boolean)
with app.app_context():
    db.create_all()



@app.route('/test', methods=['GET', 'POST'])
def add_contact_message():
    if request.method == 'POST':
            first_name = request.form['first-name']
            last_name = request.form['last-name']
            email = request.form['email']
            phone = request.form['phone']
            company = request.form['company']
            message = request.form['message']
            if not first_name:
                flash('Name is required!')
            elif not last_name:
                flash('Last is required!')
            elif not email:
                flash('Email is required!')
            elif not phone:
                flash('Phone Number is required!')
            elif not company:
                flash('Phone Number is required!')
            elif not message:
                flash('Message is required!')            
            else:
                new_todo = Todo(first_name=first_name, last_name=last_name, email=email, phone=phone, company=company, message=message,   complete=False)
                db.session.add(new_todo)
                db.session.commit()
                print(new_todo)
            return redirect(url_for('add_contact_message' ))
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
<form action="/db" method="get">df = pd.DataFrame({'name' : ['User 1', 'User 2', 'User 3']})
    <div class="form-label-group">
        <label for="key">Tasks data-base</label>
        <input type="text" id="key" name="key" value="todo" <br><br>
        <label for="field">Task Id:</label>
        <input type="text" id="field" name="field"><br><br>
        <input type="submit" value="Submit">
    </div>
</form>
    '''

    
@app.route("/db")
def get_contact_message():
    todo_list = Todo.query.all()
    df = pd.DataFrame({'name' : ['User 1', 'User 2', 'User 3']})
    #a = df.to_sql(name='name', con=db.engine)
    with db.engine.connect() as conn:
        b = conn.execute(text("SELECT * FROM todo")).fetchall()
        print(b)
    return("22") 





@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))   



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
