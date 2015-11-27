from flask import current_app
import datetime

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

def set_expire_time():
	expire_date = datetime.datetime.now()
	expire_date = expire_date + datetime.timedelta(days=30)
	return expire_date
