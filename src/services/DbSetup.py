import pymysql,os,dotenv




class DataBaseCon:
    
    
    @staticmethod
    def db_connect():
       host_db = os.getenv("localhost")
       connection = pymysql.connect(host=host_db,
                                 user='root',
                                 password=os.getenv("DB_PASSWORD"),
                                 database='financial_data',
                                 cursorclass=pymysql.cursors.DictCursor)
       return connection
