# coding=utf-8
from flask import Flask, jsonify, abort, make_response, request, Response
from baidubaike import Baidubaike

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/get_info', methods=['GET'])
def get_info():
    item = request.args.get('item', '')
    try:
        obj = Baidubaike(item)
        result = obj.get_content()
        return jsonify({'info': result}), 200
    except:
        return jsonify({'info': None}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', processes=8,port = 40000)