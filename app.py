from flask import Flask, render_template, url_for, request, redirect, send_file
import os
import sys
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
    from myutils import stage1_data2db, stage2_db2csv, read_config_json
    from io import StringIO
    
    original_stdout = sys.stdout
    tmp_out = StringIO()
    sys.stdout = tmp_out
    stage1_data2db()
    stage2_db2csv()
    myconfig = read_config_json()
    log_name = myconfig['path_to_logs'] + '/log_' + str(datetime.utcnow())[:19].replace(' ', '_').replace(':','-') + '.txt'
    with open(log_name, 'w') as f:
        f.write(tmp_out.getvalue())
    sys.stdout = original_stdout
    return '<p>{}</p>'.format(tmp_out.getvalue())

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

@app.route('/showall')
def showall():
    external_expense = ExpenseExternal.query.order_by(ExpenseExternal.created_date)
    internal_expense = ExpenseInternal.query.order_by(ExpenseInternal.created_date)
    revenue = Revenue.query.order_by(Revenue.created_date)
    
    return render_template("showall.html", revenue=revenue, internal_expense=internal_expense, external_expense=external_expense)

@app.route('/delete/<id>')
def delete(id):
    record_to_delete = ExpenseExternal.query.get_or_404(id)
    try:
        db.session.delete(record_to_delete)
        db.session.commit()
    except:
        return '<h1>There is a problem when deleting, please try again..</h1>'
    
    return redirect(url_for('showall'))

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
    app.run(debug=True, port=3000, host="0.0.0.0")
    # app.run()
    # app.run(debug=True, port=3000)
