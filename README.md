# step to run this app
- git clone ...
- virtualenv env
- edit config
- cp /externalExpense_Template.xlsx /data4database/externalExpense_Template.xlsx
- gunicorn -b 127.0.0.1:3000 app:app