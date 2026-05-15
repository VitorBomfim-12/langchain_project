from services.DbSetup import DataBaseCon as DBC
from schemas.requestDTOs import StoreAndOwnersDTO
import pymysql

class InsertStoreAndOwners:

    @staticmethod
    def insertStoreAndOwners(t: StoreAndOwnersDTO):
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql='INSERT INTO store_owners (owners_id,store_id) VALUES (%s,%s)'
                params = (t.ownerID,t.storeID)
                cur.execute(sql,params)
                con.commit()
        
        except pymysql.MySQLError as e:
            return f"Erro no banco de dados{e}"
        
        finally:
            if 'con' in locals() and con.open:
                con.close()
