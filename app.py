from flask import Flask, render_template, url_for, request, redirect, send_file
import os
import sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json
from log_handler import logger
from myutils import process_reports_from_vendor, read_config_json, process_billing_status, process_ecncost, data2csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///effort_data.db'
db = SQLAlchemy(app)
@app.route('/read_reports_from_vendor')
def read_reports_from_vendor():
    t_config = read_config_json()
    processed_reports = t_config['vendor_reports']['processed_reports']
    reports = process_reports_from_vendor(t_config['vendor_reports']['report_folder'])
    return render_template('read_reports_from_vendor.html', processed_reports=processed_reports, reports=reports)

@app.route('/read_ecn_cost')
def read_ecn_cost():
    process_ecncost()
    return send_file('default.log', mimetype = 'log', download_name= 'default.log', as_attachment = False)

@app.route('/read_billing_status')
def read_billing_status():
    process_billing_status()
    return send_file('default.log', mimetype = 'log', download_name= 'default.log', as_attachment = False)

@app.route('/print_data/<file_to_print>')
def print_file(file_to_print):
    data_to_print = {'billing_status':'billing_status.json', 'ecn_cost':'ecn_cost.json', 'vendor_report':'from_vendor.json', 'current_config':'config/config.json', 'logs':'default.log'}
    return send_file(data_to_print[file_to_print], mimetype = 'json', download_name= 'tmp.json', as_attachment = False)

@app.route('/generate_pivot')
def generate_pivot():
    data2csv()
    return '<a href="ms-excel:ofe|u|//bosch.com/dfsrb/DfsCN/loc/Sgh/RBCN/RBEI_ECN/RBEI_ECN/01-Projects/@Partner_Cost/@ExpenseReport.xlsx">Open in Excel</a>'

@app.route('/')
def index():
    data_to_print = ('billing_status', 'ecn_cost', 'vendor_report', 'current_config', 'logs')
    return render_template('index.html', data_to_print=data_to_print)

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
