from flask import Flask, jsonify, request
from flask_cors import CORS
from redis import Redis
from tasks import check_files
from celery.result import AsyncResult
from tasks import celeryApp
import config


app = Flask(__name__)
redis = Redis(host='redis', port=6379)
CORS(app)


@app.route('/filecheck', methods=['POST'])
def file_check():
    file_ids = []
    files = request.files
    for input_name in files.keys():
        for file in files.getlist(input_name):
            res = check_files.delay(file.filename, str(file.read()))
            file_ids.append(res.id)
    old_ids = redis.json().get('task_ids')
    if not old_ids:
        old_ids = []
    redis.json().set('task_ids', '$', old_ids + file_ids)
    return jsonify(file_ids), 200


@app.route('/statistics', methods=['GET'])
def statistics():
    task_ids = redis.json().get('task_ids')
    if task_ids:
        return_value = {}
        for task_id in task_ids:
            res = AsyncResult(task_id, app=celeryApp)
            if res.state == 'SUCCESS':
                return_value[task_id] = {'status': res.state, 'data': redis.json().get(task_id)}
            elif res.state == 'PENDING':
                return_value[task_id] = {'status': res.state}
            else:
                return_value[task_id] = {'status': 'unknown task id'}
        return jsonify(return_value), 200
    return jsonify(''), 200


# @app.route('/details', methods=['GET'])
# def details():
#     task_id = request.args.get('id')
#     res = AsyncResult(task_id, app=celeryApp)
#     if res.state == 'SUCCESS':
#         return redis.get(f'{task_id}_results').decode('utf-8')
#     elif res.state == 'PENDING':
#         return 'the file is being checked', 200
#     return 'information is absent', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
