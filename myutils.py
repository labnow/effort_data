from datetime import datetime, date
import json
from openpyxl import load_workbook
import sys
from app import db, ExpenseInternal, Revenue, ExpenseExternal
import os
 
# JSON file
def read_config_json():
    with open('config/config.json', "r") as f:
        myconfig = json.loads(f.read())

    if myconfig:
        # print('config load successfully.')
        return myconfig
    else:
        print('config not exist')

def check_data(my_project, my_date, my_amount):
    myconfig = read_config_json()
    
    if not my_project in myconfig['default']['projects']:
        print('\tInvalid Project Name')
        return False
    if not isinstance(my_date, date):
        print('\tInvalid Invoice Date')
        return False
    if not isinstance(my_amount, (int, float, complex)):
        print('\tInvalid Amount')
        return False

    return True

def read_ecncost():
    ExpenseInternal.query.delete()
    # delete all records, then insert read records
    print('Reading ecn_cost/internal_expense data...')
    myconfig = read_config_json()
    wb = load_workbook(myconfig['default']['ecnCost']['filePath'], data_only=True)
    ws = wb[myconfig['default']['ecnCost']['sheetName']]

    myData = []
    myDataTotal = 0

    row_start = myconfig['default']['ecnCost']['dataStartFromRow']
    row_end = myconfig['default']['ecnCost']['dataEndAtRow']
    column_start = myconfig['default']['ecnCost']['dataStartFromColumn'] # B
    column_end = myconfig['default']['ecnCost']['dataEndAtColumn'] # K
    table_header = myconfig['default']['ecnCost']['tableHeaderRow']
    table_index = myconfig['default']['ecnCost']['tableIndexColumn']
    
    for row in range(row_start, row_end + 1):
        for col in range(column_start, column_end + 1):
            tmp_cell = ws.cell(row=row, column=col)
            if tmp_cell.value:
                myProject = ws.cell(row=table_header, column=col).value
                myDate = date(2021,ws.cell(row=row, column=table_index).value,1)
                myAmount = tmp_cell.value
                if check_data(myProject, myDate, myAmount):
                    try:
                        expense_internal = ExpenseInternal(project=myProject, invoice_date=myDate, amount=myAmount)
                        db.session.add(expense_internal)
                        db.session.commit()
                        myDataTotal += myAmount
                        myTuple = (myProject, myDate, myAmount)
                        myData.append(myTuple)
                        print('\t{} add to database successfully'.format(myTuple))
                    except:
                        print('\t{} can not be added to database'.format(myTuple))
                else:
                    print('\t{} {} {} has been dropped'.format(myProject, myDate, myAmount))

    # print(myData)
    myDataLength = len(myData)
    print(str(myDataLength) + ' value read, sum of amount is ' + str(myDataTotal))

def read_billing_status():
    Revenue.query.delete()
    # delete all records, then insert read records
    print('Reading billing_status/revenue data...')
    myconfig = read_config_json()

    wb = load_workbook(myconfig['default']['billing_status']['filePath'], data_only=True)
    ws = wb[myconfig['default']['billing_status']['sheetName']]

    row_start = myconfig['default']['billing_status']['dataStartFromRow']
    row_end = myconfig['default']['billing_status']['dataEndAtRow']
    column_project = myconfig['default']['billing_status']['column_project']
    column_date = myconfig['default']['billing_status']['column_date']
    column_amount = myconfig['default']['billing_status']['column_amount']

    myData = []
    myDataTotal = 0

    for row in range(row_start, row_end + 1):
        # read property:date
        myDate = ws.cell(row=row, column=column_date).value
        # read property:project
        row_tmp = row
        while True:
            myProject = ws.cell(row=row_tmp, column=column_project).value
            if myProject:
                break
            row_tmp -= 1
        # read property:amount
        myAmount = ws.cell(row=row, column=column_amount).value
        if check_data(myProject, myDate, myAmount):
            try:
                revenue = Revenue(project=myProject, invoice_date=myDate, amount=myAmount)
                db.session.add(revenue)
                db.session.commit()
                myDataTotal += myAmount
                myTuple = (myProject, myDate, myAmount)
                myData.append(myTuple)
                print('\t{} add to database successfully'.format(myTuple))
            except:
                print('\t{} can not be added to database'.format(myTuple))
        else:
            print('\t{} {} {} has been dropped'.format(myProject, myDate, myAmount))

    myDataLength = len(myData)
    print(str(myDataLength) + ' value read, sum of amount is ' + str(myDataTotal))

def read_external_effort():
    import shutil
    myconfig = read_config_json()

    wb = load_workbook(myconfig['default']['external_effort']['filePath'], data_only=True)
    ws = wb.active

    myData = []
    myDataTotal = 0
    for row in ws.values:
        # excel header ['category', 'project', 'item', 'amount', 'invoice_date', 'partner']
        current_data = [x for x in row]
        if check_data(current_data[1], current_data[4], current_data[3]):
            try:
                expense_external = ExpenseExternal(project=current_data[1], item=current_data[2], invoice_date=current_data[4], amount=current_data[3], category=current_data[0], partner=current_data[5])
                db.session.add(expense_external)
                db.session.commit()
                myDataTotal += current_data[3]
                myData.append(current_data)
                print('\t{} add to database successfully'.format(current_data))
            except:
                print('\t{} can not be added to database'.format(current_data))         
        else:
            print('\t{} has been dropped'.format(current_data))

    now = str(datetime.now())[:10]
    os.rename(myconfig['default']['external_effort']['filePath'], myconfig['default']['external_effort']['filePath'] + '_' + now)
    shutil.copyfile('externalExpense_Template.xlsx', 'externalExpense.xlsx')
    myDataLength = len(myData)
    print(str(myDataLength) + ' value read, sum of amount is ' + str(myDataTotal))


def stage1_data2db():
    read_ecncost()
    read_billing_status()
    read_external_effort()

def stage2_db2json():
    return 0

if __name__ == '__main__':
    # sys.stdout = open('log', 'w')
    # print('u r directly execcutng this script')
    # # read_ecncost()
    # read_billing_status()
    # sys.stdout.close()
    stage1_data2db()