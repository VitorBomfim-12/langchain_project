from services.DbSetup import DataBaseCon as DBC
from schemas.requestDTOs import StoreAndOwnersDTO
from services.selectQuerys.ActiveStoreQuery import ActiveStore
import pymysql

class InsertStoreAndOwners:

    @staticmethod
    def insertStoreAndOwners(t: StoreAndOwnersDTO):
        try:
            if not ActiveStore(t.storeID):
                return "Estabelecimento inativo"
            
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql='INSERT INTO store_owners (owners_id,store_id) VALUES (%s,%s)'
                params = (t.ownerID,t.storeID)
                cur.execute(sql,params)
                con.commit()
        
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
        finally:
            con.close()
