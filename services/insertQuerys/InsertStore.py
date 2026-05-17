from services.DbSetup import DataBaseCon as DBC
import pymysql
from schemas.requestDTOs.StoreDTO import StoreDTO

class InsertStore:
    @staticmethod
    def insertStore(t: StoreDTO):
    
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = "INSERT INTO store(store_name,cnpj,mcc_code,location) VALUES(%s,%s,%s,ST_GeomFromText(%s, 4326))"
                params = (t.storeName,t.cnpj,t.mccCode,t.location)
                cur.execute(sql,params)
                con.commit()

        except pymysql.MySQLError as e:
            return f"Erro no banco de dados: {e}"
        
        finally:
                con.close()