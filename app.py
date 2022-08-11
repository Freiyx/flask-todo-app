from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ayylmaowtfidcxd'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    complete = db.Column(db.Boolean(), default=False, nullable=False)
    priority = db.Column(db.Integer(), nullable=False)

class addTask(FlaskForm):
    range = range(1,6)
    name = StringField(label="Task Name: ", validators=[DataRequired()])
    priority = SelectField(label="Set Priority: ", choices=range, validators=[DataRequired()])
    submit = SubmitField(label="Add Task")

class complete(FlaskForm):
    submit = SubmitField(label="Complete")

class delete(FlaskForm):
    submit = SubmitField(label="Delete")

@app.route('/', methods=['GET','POST'])
def index():

    add_task_form = addTask()
    complete_form = complete()
    delete_form = delete()

    if add_task_form.validate_on_submit():
        adding_task = Todo(name= add_task_form.name.data,
                            priority=add_task_form.priority.data,
                           )
        db.session.add(adding_task)
        db.session.commit()
        return redirect(url_for('index'))

    if complete_form.validate_on_submit():
        completed_task = request.form.get('completed_task')
        completed_task_obj = Todo.query.filter_by(id=completed_task).first()
        if completed_task_obj:
            completed_task_obj.complete = True
            db.session.commit()
            return redirect(url_for('index'))

    if delete_form.validate_on_submit():
        deleted_task = request.form.get('deleted_task')
        deleted_task_obj = Todo.query.filter_by(id=deleted_task).first()
        if deleted_task_obj:
            db.session.delete(deleted_task_obj)
            db.session.commit()
            return redirect(url_for('index'))

    ongoing_task = Todo.query.filter_by(complete=False).order_by(Todo.priority.desc())
    completed_task = Todo.query.filter_by(complete=True).order_by(Todo.priority.desc())

    return render_template('base.html', ongoing_task=ongoing_task, completed_task=completed_task, add_task_form=add_task_form, complete_form=complete_form, delete_form=delete_form)

if __name__ == '__main__':
    db.create_all()

    app.run(debug=True)