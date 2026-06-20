from src.services.DbSetup import DataBaseCon as DBC
from src.schemas.requestDTOs.TransactionDTO import TransactionDTO
from src.services.selectQuerys.ActiveStoreQuery import ActiveStore

import pymysql

class InsertTransaction:

    @staticmethod
    def insertTransaction(t:TransactionDTO):
    
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''INSERT INTO transactions
                (transaction_value,
                transaction_date,
                transaction_cpf,
                transaction_location,
                transaction_status,
                transaction_risk,
                reason,
                transaction_store_id_FK)

                VALUES (%s,%s,%s,ST_PointFromText(%s, 4326),%s,%s,%s,%s)'''

                point_string = f"POINT({t.location[1]} {t.location[0]})"
                
                params = (t.value,t.data,t.cpf,point_string,t.status,t.risk,t.reason,t.storeID)
                cur.execute(sql,params)
                con.commit()
            return "Sucesso."
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados."
        
        finally:
            if  con.open:
                con.close()