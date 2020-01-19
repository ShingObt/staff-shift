class SysConfig:

    DBUSER = 'manager'
    PASSWD = 'password'
    DBHOST = 'localhost'
    DBPORT = '5432'
    DATABASE = 'staff_shift'

    SQLALCHEMY_DATABASE_URI = "postgresql://" \
                              + DBUSER + ":" \
                              + PASSWD + "@" \
                              + DBHOST + ":" \
                              + DBPORT + "/" \
                              + DATABASE

    SQLALCHEMY_TRACK_MODIFICATIONS = False

Config = SysConfig
