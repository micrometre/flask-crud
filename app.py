import sys
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from flask import Flask, flash, json, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pandas as pd
import markdown
import markdown.extensions.fenced_code

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    company = db.Column(db.String(100))
    message = db.Column(db.String)
    complete = db.Column(db.Boolean)

with app.app_context():
    db.create_all()
@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route('/add', methods=['GET', 'POST'])
def add_contact_message():
    if request.method == 'POST':
            title = request.form['title']
            first_name = request.form['first-name']
            last_name = request.form['last-name']
            email = request.form['email']
            phone = request.form['phone']
            company = request.form['company']
            message = request.form['message']
            if not title:
                flash('title is required!')
            elif not first_name:
                flash('Name is required!')
            elif not last_name:
                flash('Last name is required!')
            elif not email:
                flash('Email is required!')
            elif not phone:
                flash('Phone Number is required!')
            elif not company:
                flash('Phone Number is required!')
            elif not message:
                flash('Message is required!')            
            else:
                new_todo = Todo(title=title,  first_name=first_name, last_name=last_name, email=email, phone=phone, company=company, message=message,   complete=False)
                db.session.add(new_todo)
                db.session.commit()
                print(new_todo)
            return redirect(url_for('posts' ))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("get_contact_message"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("get_contact_message"))



@app.route("/db")
def get_contact_message():
    todo_list = Todo.query.all()
    return render_template("db.html", todo_list=todo_list)
























@app.route("/posts/")
def posts():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=False)
    return render_template('posts.html', posts=posts)

@app.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)