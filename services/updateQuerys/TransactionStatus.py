from src.first_project.services.DbSetup import DataBaseCon as DBC
from src.first_project.schemas.requestDTOs.TransactionStatusDTO import TransactionStatus
import pymysql

class AlterTransaction():

    @staticmethod
    def alterTransaction(t: TransactionStatus):

        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = "UPDATE transactions SET transaction_status = %s, reason = %s WHERE id =%s"
                params = (t.status,t.reason,t.transactionID)
                cur.execute (sql,params)
                con.commit()
        
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
        finally:
                con.close()