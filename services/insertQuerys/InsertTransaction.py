from first_project.services.DbSetup import DataBaseCon as DBC
from first_project.schemas.requestDTOs.TransactionDTO import TransactionDTO
from first_project.services.selectQuerys.ActiveStoreQuery import ActiveStore

import pymysql

class InsertTransaction:

    @staticmethod
    def insertTransaction(t:TransactionDTO):
    
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''INSERT INTO transactions(transaction_value,transaction_date,
                transaction_cpf,transaction_location,transaction_status,reason,transaction_store_id_FK
                VALUES (%s,%s,%s,%s,%s,%s,%s)'''
                params = (t.value,t.data,t.cpf,t.location,t.status,t.reason,t.storeID)
                cur.execute(sql,params)
                con.commit()
            return "Sucesso."
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados."
        
        finally:
            if con and con.open:
                con.close()