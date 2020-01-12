from flask import Flask, render_template, request, redirect, url_for
from database import init_db
import models
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
import calendar

# 日付フォーマットの定数
YEAR_MONTH_FORMAT = "%Y%m"
DATE_FORMAT = "%Y%m%d"

# Flaskインスタンスの生成
app = Flask(__name__)
app.config.from_object('config.Config')
app = init_db(app)

# URLによって振り分けられる関数群
@app.route('/')
def top():
    return render_template('index.html', title='従業員シフト入力システム')

@app.route('/employee')
def employee_list():
    employees = models.Employee.get_employees()
    return render_template('employee.html', title='従業員一覧', employees=employees)

@app.route('/add_employee')
def add_employee():
    return render_template('add_employee.html', title='従業員追加')

@app.route('/add_employee_commit', methods=['POST'])
def add_employee_commit():
    nickname = request.form['nickname']
    models.Employee.add_employee(nickname)
    return redirect("/employee")

@app.route('/del_employee', methods=['POST'])
def del_employee():
    employee_id = request.form['employee_id']
    employee = models.Employee.get_one_employee(employee_id)
    return render_template("del_employee.html", title="従業員削除確認", employee=employee)

@app.route('/del_employee_commit', methods=['POST'])
def del_employee_commit():
    employee_id = request.form['employee_id']
    models.Employee.del_employee(employee_id)
    return redirect("/employee")

@app.route('/show_monthly_shift/')
@app.route('/show_monthly_shift/<string:year_month>')
def show_monthly_shift(year_month=None):
    if year_month == None:
        year_month = datetime.now().strftime(YEAR_MONTH_FORMAT)

    target_month = datetime.strptime(year_month, YEAR_MONTH_FORMAT)

    monthly_calendar = calendar.Calendar(6).monthdatescalendar(target_month.year, target_month.month)

    end_target = target_month + relativedelta(months=1, days=-1)

    monthly_shift = models.Shift.get_monthly_shift(target_month, end_target)

    pre_year_month = target_month + relativedelta(months=-1)
    next_year_month = target_month + relativedelta(months=1)

    return render_template('monthly_shift.html', title='月間シフト', target_month=target_month, \
                            pre_year_month=pre_year_month, next_year_month=next_year_month, \
                            monthly_cal=monthly_calendar, monthly_shift=monthly_shift)

@app.route('/show_daily_shift/')
@app.route('/show_daily_shift/<string:date>')
def show_daily_shift(date=None):
    if date == None:
        date = datetime.now().strftime(DATE_FORMAT)

    target_date = datetime.strptime(date, DATE_FORMAT)

    daily_shift = models.Shift.get_daily_shift(target_date)

    pre_date = target_date + timedelta(days=-1)
    next_date = target_date + timedelta(days=1)

    return render_template('daily_shift.html', title='当日のシフト', target_date=target_date, \
                            pre_date=pre_date, next_date=next_date, daily_shift=daily_shift)

@app.route('/add_daily_shift/')
@app.route('/add_daily_shift/<string:date>')
def add_daily_shift(date=None):
    if date == None:
        date = datetime.now().strftime(DATE_FORMAT)

    target_date = datetime.strptime(date, DATE_FORMAT)

    employees = models.Employee.get_employees()
    return render_template('add_daily_shift.html', title='シフト追加', \
                           target_date=target_date, employees=employees)

@app.route('/add_daily_shift_commit', methods=['POST'])
def add_daily_shift_commit():
    date = request.form['target_date']
    start_time_hour = request.form['start_time_hour']
    start_time_minute = request.form['start_time_minute']
    end_time_hour = request.form['end_time_hour']
    end_time_minute = request.form['end_time_minute']
    employee_id = request.form['employee']

    target_date = datetime.strptime(date, DATE_FORMAT)
    start_time = time(int(start_time_hour), int(start_time_minute), 0)
    end_time = time(int(end_time_hour), int(end_time_minute), 0)

    models.Shift.add_shift(target_date, employee_id, start_time, end_time)

    redirect_uri = url_for('show_daily_shift', date=target_date.strftime('%Y%m%d'))
    return redirect(redirect_uri)

@app.route('/del_daily_shift', methods=['POST'])
def del_daily_shift():
    date = request.form['target_date']
    employee_id = request.form['del_id']

    target_date = datetime.strptime(date, DATE_FORMAT)

    models.Shift.del_shift(target_date, employee_id)

    redirect_uri = url_for('show_daily_shift', date=date)
    return redirect(redirect_uri)
