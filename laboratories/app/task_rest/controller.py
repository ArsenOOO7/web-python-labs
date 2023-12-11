from flask import jsonify, make_response, abort, request

from app import data_base
from app.domain.Task import Task, Status
from . import task_rest_bp


@task_rest_bp.errorhandler(404)
def not_found(error):
    message = error.description['message'] or 'Could not find resource.'
    return make_response(jsonify({'error': message})), 404


@task_rest_bp.route('/<int:id>', methods=['GET'])
def get_task(id=None):
    task = Task.query.get(id)
    if not task:
        abort(404, {'message': f"Undefined Task with id {id}."})
    return jsonify(task.to_dict()), 200


@task_rest_bp.route("/", methods=['GET'])
@task_rest_bp.route("/list", methods=['GET'])
def task_list():
    return jsonify([task.to_dict() for task in Task.query.all()]), 200


@task_rest_bp.route("/", methods=['POST'])
def create_task():
    json = request.json
    task_name = json['name']
    task_description = json['description']

    task = Task(name=task_name, description=task_description, status=Status.TODO)
    data_base.session.add(task)
    data_base.session.commit()

    return jsonify(task.to_dict()), 201


@task_rest_bp.route("/<int:id>", methods=['PUT'])
def update_task(id=None):
    json = request.json

    task: Task = Task.query.get(id)
    if not task:
        abort(404, {'message': f"Undefined Task with id {id}."})

    task_name = json['name']

    existing_task = Task.query.filter(Task.name == task_name).first()
    if existing_task is not None and existing_task.id != task.id:
        abort(400)

    task_description = json['description']
    task_status = Status[json['status']]

    task.name = task_name
    task.description = task_description
    task.status = task_status

    data_base.session.commit()
    return jsonify(task.to_dict()), 200


@task_rest_bp.route('/<int:id>', methods=['DELETE'])
def delete_task(id=None):
    task: Task = Task.query.get(id)
    if not task:
        abort(404, {'message': f"Undefined Task with id {id}."})

    data_base.session.delete(task)
    data_base.session.commit()
    return jsonify({}), 200
