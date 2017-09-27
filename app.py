from flask import Flask,redirect, request,render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

#### DATABASE ELEMENTS ##############
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mytasks = db.Column(db.String(200))
    done = db.Column(db.Boolean)

    def __init__(self, mytasks):
        self.mytasks = mytasks
        self.done = False

####### TO CREATE DATABASE(todo.db) ##########
db.create_all()

@app.route('/')
def list():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

####### TO Create TASK ############
@app.route('/create', methods=['POST'])
def create():
    content = request.form['tasks']
    if not content:
        return redirect('/')
    task = Todo(request.form['tasks'])
    
    db.session.add(task)
    db.session.commit()
    return redirect('/')

######## TO DELETE THE TASK ########

@app.route('/delete/<id>')
def delete(id):
    task = Todo.query.get(id)

    db.session.delete(task)
    db.session.commit()
    return redirect('/')

##### TO MARK THE TASK ############

@app.route('/done/<id>')
def mark(id):
    task = Todo.query.get(id)

    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/')


########## APP ##############
if __name__ == '__main__':
    app.debug = True
    port = os.environ.get('PORT',8000)
    app.run(host='0.0.0.0',port=port)
   
