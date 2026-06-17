from services.DbSetup import DataBaseCon as DBC
from datetime import datetime
import pymysql


class SelectAVGValue:

    @staticmethod
    def GetAVGValue(storeID:int,initialDate:datetime,finalDate:datetime)->str:
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''SELECT 
                AVG(transaction_value) as avg_value,
                FROM transactions
                WHERE transaction_store_id_FK =v%s AND transaction_date BETWEEN %s AND %s
                '''
                cur.execute(sql,storeID,initialDate,finalDate)
                response = cur.fetchone()

                return response
            
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
        