from datetime import datetime, date
import json
from openpyxl import load_workbook
import sys
 
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
                    myDataTotal += myAmount
                    myTuple = (myProject, myDate, myAmount)
                    myData.append(myTuple)
                    print('\t{} add to database successfully'.format(myTuple))
                else:
                    print('\t{} {} {} has been dropped'.format(myProject, myDate, myAmount))

    # print(myData)
    myDataLength = len(myData)
    print(str(myDataLength) + ' value read, sum of amount is ' + str(myDataTotal))

def read_billing_status():
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
            myDataTotal += myAmount
            myTuple = (myProject, myDate, myAmount)
            myData.append(myTuple)
            print('\t{} add to database successfully'.format(myTuple))
        else:
            print('\t{} {} {} has been dropped'.format(myProject, myDate, myAmount))

    myDataLength = len(myData)
    print(str(myDataLength) + ' value read, sum of amount is ' + str(myDataTotal))

def read_external_effort():
    myconfig = read_config_json()

    wb = load_workbook(myconfig['default']['external_effort']['filePath'], data_only=True)
    ws = wb.active
    for row in ws.values:
        print('new line')
        for value in row:
            print(value)

def stage1_data2db():
    # read_ecncost()
    # read_billing_status()
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