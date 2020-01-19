from database import db

class Staff(db.Model):
    __tablename__ = "staffs"
    staff_id = db.Column(db.String(), primary_key=True)
    nickname = db.Column(db.String(), nullable=False)
    
    def get_staffs():
        return Staff.query.order_by(Staff.staff_id).all()
    
    def add_staff(nickname):
        max_id_num = db.session.query(db.func.max(Staff.staff_id)).scalar()
        if max_id_num == None:
            max_id_num = 0

        staff_id = str(int(max_id_num) + 1).zfill(6)
        staff = Staff(staff_id=staff_id, nickname=nickname)
        db.session.add(staff)
        db.session.commit()

    def get_one_staff(staff_id):
        return Staff.query.filter(Staff.staff_id==staff_id).one()

    def del_staff(staff_id):
        db.session.query(Shift).filter(Shift.staff_id==staff_id).delete()
        db.session.query(Staff).filter(Staff.staff_id==staff_id).delete()
        db.session.commit()

class Shift(db.Model):
    __tablename__ = "shifts"
    day = db.Column(db.Date(), primary_key=True)
    staff_id = db.Column(db.String(), primary_key=True)
    start_time = db.Column(db.Time(), nullable=False)
    end_time= db.Column(db.Time(), nullable=False)
    
    def get_monthly_shift(target_month, end_target):
        monthly_shift = Shift.query.join(Staff, Shift.staff_id==Staff.staff_id) \
                .add_columns(Shift.day, Staff.nickname, Shift.start_time, Shift.end_time) \
                .filter(Shift.day.between(target_month, end_target)).order_by(Shift.start_time).all()
        return monthly_shift

    def get_daily_shift(target_date):
        daily_shift = Shift.query.join(Staff, Shift.staff_id==Staff.staff_id) \
                .add_columns(Shift.day, Staff.staff_id, Staff.nickname, Shift.start_time, Shift.end_time) \
                .filter(Shift.day==target_date).order_by(Shift.start_time, Staff.staff_id).all()
        return daily_shift
    
    def add_shift(target_date, staff_id, start_time, end_time):
        shift = Shift(day=target_date, staff_id=staff_id, start_time=start_time, end_time=end_time)
        db.session.add(shift)
        db.session.commit()
    
    def del_shift(target_date, staff_id):
        db.session.query(Shift).filter(Shift.day==target_date, Shift.staff_id==staff_id).delete()
        db.session.commit()

