import pymysql,os,dotenv




class DataBaseCon:
    
    
    @staticmethod
    def db_connect():
        
        dotenv.load_dotenv()
        host_db = os.getenv('DB_HOST', "localhost")
        port_db = int(os.getenv('DB_PORT', 3306))
        connection = pymysql.connect(host=host_db,
                                     port=port_db,
                                     user=os.getenv("DB_HOST",'usuario'),
                                     password=os.getenv("DB_PASSWORD"),
                                     database='financial_data',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    
