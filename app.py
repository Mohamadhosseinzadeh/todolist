import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import jdatetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'

# تنظیمات دیتابیس SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def gregorian_to_jalali_str(date_obj):

    if not date_obj:
        return ""

    j_date = jdatetime.date.fromgregorian(date=date_obj)

    return j_date.strftime('%Y/%m/%d')


app.template_filter('to_jalali')(gregorian_to_jalali_str)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.Integer, nullable=False, default=2)

    def __repr__(self):
        return f'<Todo {self.id}>'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_priority = int(request.form['priority'])
        due_date_str = request.form['due_date']
        due_date_obj = None

        if due_date_str:

            year, month, day = map(int, due_date_str.split('/'))
            j_date = jdatetime.date(year, month, day)
            due_date_obj = j_date.togregorian()

        new_task = Todo(content=task_content, priority=task_priority, due_date=due_date_obj)

        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('index'))
        except:
            flash('There was an issue adding your task.', 'danger')
            return redirect(url_for('index'))
    else:
        tasks = Todo.query.order_by(Todo.priority, Todo.id).all()
        return render_template('index.html', tasks=tasks)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.priority = int(request.form['priority'])
        due_date_str = request.form['due_date']
        due_date_obj = None
        if due_date_str:

            year, month, day = map(int, due_date_str.split('/'))
            j_date = jdatetime.date(year, month, day)
            due_date_obj = j_date.togregorian()
        else:
            task.due_date = None

        try:
            db.session.commit()
            flash('Task updated successfully!', 'info')
            return redirect(url_for('index'))
        except:
            flash('There was an issue updating the task.', 'danger')
            return redirect(url_for('edit', id=id))
    else:
        return render_template('edit.html', task=task)



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Task deleted.', 'secondary')
        return redirect(url_for('index'))
    except:
        flash('There was a problem deleting that task.', 'danger')
        return redirect(url_for('index'))


@app.route('/update/<int:id>')
def update(id):
    task = Todo.query.get_or_404(id)
    task.completed = 1 - task.completed  # A clever way to toggle between 0 and 1
    try:
        db.session.commit()
        flash('Task status updated!', 'secondary')
        return redirect(url_for('index'))
    except:
        flash('There was an issue updating your task.', 'danger')
        return redirect(url_for('index'))

@app.route('/mohamad')
def m():
	return 'hello mohamad'
	
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
