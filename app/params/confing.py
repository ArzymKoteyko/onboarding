from os import getenv

DBUSER = getenv('DBUSER', 'admin123')
DBPASSWORD = getenv('DBPASSWORD', 'p0ssw0rd')
DBHOST = getenv('DBHOST', 'db')
DBNAME = getenv('DBNAME', 'postgres')
DBPORT = getenv('DBPORT', '5432')
RESET_DB = getenv('RESET_DB', 'True')

TEST = bool(getenv('RESET_DB', 'True'))
