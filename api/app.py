import celery.states as states
from flask import Flask, Response, request
from flask import url_for, jsonify
from worker import celery

from redis_worker import redis_db
from mock import mock_class_info, mock_office_hours_info

dev_mode = True
app = Flask(__name__)


@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


@app.route('/health_check')
def health_check() -> Response:
    return jsonify("OK")

@app.route('/test/<string:param1>')
def test(param1: str) -> str:
    redis_db.set('param1', param1)
    redis_db.set('param2', 'param2')
    print("test2")
    return jsonify("OK")

@app.route('/class_info', methods=['GET', 'POST'])
def class_info() -> str:
    return jsonify(mock_class_info.MOCK_CLASS_INFO)

@app.route('/office_hours_info', methods=['GET'])
def get_office_hours_info() -> str:
    print("test")
    return jsonify(mock_office_hours_info.MOCK_OFFICE_HOURS_INFO)

@app.route('/office_hours_info', methods=['POST'])
def post_office_hours_info() -> str:
    user_id = request.form.get('user_id')
    user_info = request.form.get('user_info')
    class_id = request.form.get('class_id')

    return jsonify(mock_office_hours_info.MOCK_OFFICE_HOURS_INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
