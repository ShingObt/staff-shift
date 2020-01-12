class SysConfig:

    DBUSER = 'maguro'
    PASSWD = 'password'
    DBHOST = 'localhost'
    DBPORT = '5432'
    DATABASE = 'maguro_market'

    SQLALCHEMY_DATABASE_URI = "postgresql://" \
                              + DBUSER + ":" \
                              + PASSWD + "@" \
                              + DBHOST + ":" \
                              + DBPORT + "/" \
                              + DATABASE

    SQLALCHEMY_TRACK_MODIFICATIONS = False

Config = SysConfig
