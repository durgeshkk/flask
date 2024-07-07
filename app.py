from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# app = Flask(__name__)  # Created an app

app = Flask(__name__)

# Provide config for Database :
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# If getting a warning for Track Modifications in SQLAlchemy  just set it to false
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a class Todo to define Schema of our database
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


with app.app_context():
    db.create_all()

# End points     
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/products')
def products():
    return 'This is products page'

@app.route('/dk-page', methods=['GET', 'POST'])
def sample_template():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        print(title+" "+desc)
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    # This will return the index.html page from templates directory. 
    # Making the use of Jinja2
    return render_template('index.html', allTodo = alltodo)  

# This will use __repr__ function created in database
@app.route('/show')
def show():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'Check database details in Terminal where the app is running'

# Delete will take serial no. as input for performing delete ops from DB
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = db.get_or_404(Todo,sno)
    # todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    print(todo)
    # To redirect user again to /dk-page
    return redirect("/dk-page")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/dk-page")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)  

# To Run app.py
if __name__ == "__main__":
    app.run(debug=True, port=8000) # To run on desired port
    # app.run(debug=True) 