#!/usr/bin/env python
from flask import Flask

app = Flask(__name__)

# root
@app.route('/')
def index():
    return "CIPAPI gateway service"

# close case
@app.route('/api/1/ir/report/<str:case_id>/', methods=['POST'])
def close_ir():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)