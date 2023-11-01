from flask import redirect, url_for, request

from app import *
from app.common.common import render, check_logged
from app.domain.Task import Task, Status
from app.forms import AddTask, UpdateTask


@app.route('/tasks', methods=['GET'])
def tasks():
    task_list = data_base.session.query(Task).all()
    return render('tasks/tasks_main', tasks=task_list)


@app.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    add_task_form = AddTask()
    if request.method == 'GET':
        return render('tasks/add_task', form=add_task_form)
    check_logged()
    if add_task_form.validate_on_submit():
        task_name = add_task_form.name.data
        task = Task(name=task_name)
        data_base.session.add(task)
        data_base.session.commit()
        return redirect(url_for('tasks'))
    return render('tasks/add_task', form=add_task_form)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id=None):
    check_logged()
    if id is None:
        return redirect(url_for('tasks'))

    task = data_base.get_or_404(Task, id)
    update_form = UpdateTask()
    return render('tasks/update_task', task=task, form=update_form)


@app.route('/tasks/<int:id>', methods=['POST'])
def update_task(id=None):
    check_logged()
    if id is None:
        return redirect(url_for('tasks'))

    task = data_base.get_or_404(Task, id)
    update_form = UpdateTask()
    if not update_form.validate_on_submit():
        return render('tasks/update_task', task=task, form=update_form)

    name = update_form.name.data
    status = Status[update_form.status.data]
    task.name = name
    task.status = status
    data_base.session.commit()
    return redirect(url_for('tasks'))


@app.route('/tasks/<int:id>/delete')
def delete_task(id=None):
    check_logged()
    if id is None:
        return redirect(url_for('tasks'))

    task = data_base.get_or_404(Task, id)
    data_base.session.delete(task)
    data_base.session.commit()
    return redirect(url_for('tasks'))
