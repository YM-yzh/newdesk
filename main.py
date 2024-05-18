from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# 连接MySQL数据库
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='2021210978',
                     database='acsystem')

# 用户登录
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return jsonify({'message': 'Login successful', 'user': user})
    else:
        return jsonify({'message': 'Login failed'})

# 查询用户账单
@app.route('/api/bill', methods=['GET'])
def get_bill():
    user_id = request.args.get('user_id')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM bills WHERE user_id = %s", (user_id,))
    bills = cursor.fetchall()
    cursor.close()
    return jsonify({'bills': bills})

# 查询所有用户信息（管理员功能）
@app.route('/api/users', methods=['GET'])
def get_users():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return jsonify({'users': users})

# 查询所有账单明细（管理员功能）
@app.route('/api/all_bills', methods=['GET'])
def get_all_bills():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM bills")
    all_bills = cursor.fetchall()
    cursor.close()
    return jsonify({'all_bills': all_bills})

if __name__ == '__main__':
    app.run(debug=True)
