from flask import Flask, render_template, url_for, request, redirect, send_file
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///effort_data.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    with open('config/config.json', 'r') as f:
        myStr = f.read()
    return render_template('index.html', myStr=myStr)


@app.route('/run')
def run():
    return 0


@app.route('/update_config', methods=['POST', 'GET'])
def update_config():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            now = str(datetime.now())[:10]
            bak_name = 'config_' + now + '.json.bak'
            os.rename('config/config.json', os.path.join('config/', bak_name))
            file.save('config/config.json')
        return redirect(url_for('index'))
    else:
        return render_template('update_config.html')


class ExpenseInternal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(64))
    invoice_date = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)

class Revenue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(64))
    invoice_date = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)

class ExpenseExternal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(64))
    item = db.Column(db.String(255))
    invoice_date = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)
    category = db.Column(db.String(64))
    partner = db.Column(db.String(64))

if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
    # app.run(debug=True, port=3000)
