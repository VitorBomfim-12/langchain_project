import pymysql,os,dotenv


dotenv.load_dotenv()

class DataBaseCon:
    
    
    @staticmethod
    def db_connect():
       connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=os.getenv("DB_PASSWORD"),
                                 database='financial_data',
                                 cursorclass=pymysql.cursors.DictCursor)
       return connection
    
