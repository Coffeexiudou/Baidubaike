# coding=utf-8
from flask import Flask, jsonify, abort, make_response, request, Response
from IPPool.db.dbHelper import DBHelper

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/get_ip', methods=['GET'])
def get_info():
    try:
        num = request.args.get('num', '')
        if num:
            dbHelper = DBHelper('ip')
            result = dbHelper.select(int(num))
        else:
            dbHelper = DBHelper('ip')
            result = dbHelper.select()
        dbHelper.close()
        return jsonify({'ipList': result,'status':200}), 200
    except:
        return jsonify({'info': None,'status':400}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', processes=8)