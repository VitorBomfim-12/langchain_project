from services.DbSetup import DataBaseCon as DBC
from schemas.requestDTOs.TransactionDTO import TransactionDTO
from services.selectQuerys.ActiveStoreQuery import ActiveStore

import pymysql

class InsertTransaction:

    @staticmethod
    def insertTransaction(t:TransactionDTO):
        
        if not ActiveStore(t.storeID):
                return "Estabelecimento inativo"
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''INSERT INTO transactions(transaction_value,transaction_date,
                transaction_cpf,transaction_location,transaction_status,reason,transaction_store_id_FK
                VALUES (%s,%s,%s,%s,%s,%s,%s)'''
                params = (t.value,t.data,t.cpf,t.location,t.status,t.reason,t.storeID)
                cur.execute(sql,params)
                con.commit()
        except pymysql.MySQLError as e:
            return f"Erro no banco de dados{e}"
        
        finally:
            if 'con' in locals() and con.open:
                con.close()