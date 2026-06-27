from src.services.DbSetup import DataBaseCon as DBC
from src.schemas.requestDTOs.TransactionStatusDTO import TransactionStatus
import pymysql

class AlterTransaction():

    @staticmethod
    def alterTransaction(t: TransactionStatus):

        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = """UPDATE transactions
                SET transaction_status = CASE 
                    WHEN 
                     transaction_status <> %s 
                    THEN %s 
                    else transaction_status
                END
                WHERE id = %s
                """
                params = (t.status,t.status,t.transactionID)
                cur.execute (sql,params)
                con.commit()
                return 'Sucesso.'     
        except pymysql.MySQLError as e:
            print(e)
            return "Erro no banco de dados."
        
        finally:
                con.close()