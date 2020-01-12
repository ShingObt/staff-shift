from database import db

class Employee(db.Model):
    __tablename__ = "employees"
    employee_id = db.Column(db.String(), primary_key=True)
    nickname = db.Column(db.String(), nullable=False)
    
    def get_employees():
        return Employee.query.order_by(Employee.employee_id).all()
    
    def add_employee(nickname):
        max_id_num = db.session.query(db.func.max(Employee.employee_id)).scalar()
        if max_id_num == None:
            max_id_num = 0

        employee_id = str(int(max_id_num) + 1).zfill(6)
        employee = Employee(employee_id=employee_id, nickname=nickname)
        db.session.add(employee)
        db.session.commit()

    def get_one_employee(employee_id):
        return Employee.query.filter(Employee.employee_id==employee_id).one()

    def del_employee(employee_id):
        db.session.query(Shift).filter(Shift.employee_id==employee_id).delete()
        db.session.query(Employee).filter(Employee.employee_id==employee_id).delete()
        db.session.commit()

class Shift(db.Model):
    __tablename__ = "shifts"
    day = db.Column(db.Date(), primary_key=True)
    employee_id = db.Column(db.String(), primary_key=True)
    start_time = db.Column(db.Time(), nullable=False)
    end_time= db.Column(db.Time(), nullable=False)
    
    def get_monthly_shift(target_month, end_target):
        monthly_shift = Shift.query.join(Employee, Shift.employee_id==Employee.employee_id) \
                .add_columns(Shift.day, Employee.nickname, Shift.start_time, Shift.end_time) \
                .filter(Shift.day.between(target_month, end_target)).order_by(Shift.start_time).all()
        return monthly_shift

    def get_daily_shift(target_date):
        daily_shift = Shift.query.join(Employee, Shift.employee_id==Employee.employee_id) \
                .add_columns(Shift.day, Employee.employee_id, Employee.nickname, Shift.start_time, Shift.end_time) \
                .filter(Shift.day==target_date).order_by(Shift.start_time, Employee.employee_id).all()
        return daily_shift
    
    def add_shift(target_date, employee_id, start_time, end_time):
        shift = Shift(day=target_date, employee_id=employee_id, start_time=start_time, end_time=end_time)
        db.session.add(shift)
        db.session.commit()
    
    def del_shift(target_date, employee_id):
        db.session.query(Shift).filter(Shift.day==target_date, Shift.employee_id==employee_id).delete()
        db.session.commit()

