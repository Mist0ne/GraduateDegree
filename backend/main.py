from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/filecheck', methods=['POST'])
def file_check():
    return 'ok', 200


@app.route('/statistics', methods=['GET'])
def statistics():
    return jsonify({'task': {'id': '123'}}), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
