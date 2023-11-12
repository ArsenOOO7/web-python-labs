from flask import redirect, url_for, request, flash, session
from flask_login import current_user, login_required

from app import *
from app.common.common import render
from app.domain.Task import Task, Status
from app.forms import AddTask, UpdateTask


@app.route('/tasks', methods=['GET'])
def tasks():
    task_list = data_base.session.query(Task).all()
    return render('tasks/tasks_main', tasks=task_list)


@app.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    add_task_form = AddTask()
    if request.method == 'GET':
        return render('tasks/add_task', form=add_task_form)
    if add_task_form.validate_on_submit():
        task_name = add_task_form.name.data
        description = add_task_form.description.data

        existing_task = Task.query.filter(Task.name == task_name).first()
        if existing_task is not None:
            flash("There is the Task with this name.", category="danger")
            return redirect(url_for('add_task'))

        task = Task(name=task_name, description=description)
        data_base.session.add(task)
        data_base.session.commit()
        flash(f"You have successfully created task {task_name}", category='success')
        return redirect(url_for('tasks'))
    return render('tasks/add_task', form=add_task_form)


@app.route('/tasks/<int:id>', methods=['GET'])
@login_required
def get_task(id=None):
    if id is None:
        return redirect(url_for('tasks'))

    task = data_base.get_or_404(Task, id)
    update_form = UpdateTask()
    update_form.status.default = task.status.value
    return render('tasks/update_task', task=task, form=update_form)


@app.route('/tasks/<int:id>', methods=['POST'])
@login_required
def update_task(id=None):
    if id is None:
        return redirect(url_for('tasks'))

    task = data_base.get_or_404(Task, id)
    update_form = UpdateTask()
    if not update_form.validate_on_submit():
        return render('tasks/update_task', task=task, form=update_form)

    name = update_form.name.data
    description = update_form.description.data
    status = Status[update_form.status.data]

    existing_task = data_base.session.query(Task).filter(Task.name == name).first()
    if existing_task is not None and existing_task.id != task.id:
        flash("There is the Task with this name.", category="danger")
        return redirect(url_for('add_task'))

    task.name = name
    task.description = description
    task.status = status
    data_base.session.commit()
    flash("You have successfully updated task", category='success')
    return redirect(url_for('tasks'))


@app.route('/tasks/<int:id>/delete')
@login_required
def delete_task(id=None):
    if id is None:
        return redirect(url_for('tasks'))

    task = data_base.get_or_404(Task, id)
    data_base.session.delete(task)
    data_base.session.commit()
    flash(f"You have successfully deleted task {task.name}", category='success')
    return redirect(url_for('tasks'))
