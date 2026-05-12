import pymysql,os,dotenv


dotenv.load_dotenv()

class DbPassUpdate:
    
    
    @staticmethod
    def db_connect():
       connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=os.getenv("DB_password"),
                                 database='financial_data',
                                 cursorclass=pymysql.cursors.DictCursor)
       return connection
    
