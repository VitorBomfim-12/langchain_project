from src.services.DbSetup import DataBaseCon as DBC
from src.schemas.requestDTOs.StoreDTO import StoreDTO
import pymysql



def insertStore(t: StoreDTO):

    try:
        con = DBC.db_connect()
        with con.cursor() as cur:
            sql = "INSERT INTO store(store_name,cnpj,transaction_value_limit ,mcc_code,location) VALUES(%s,%s,%s,%s,ST_GeomFromText(%s, 4326))"
            params = (t.storeName,t.cnpj,t.transactionValueLimit,t.mccCode,t.location)
            cur.execute(sql,params)
            con.commit()
    except pymysql.MySQLError as e:
        print(f"Erro :{e}")
        return "Erro no banco de dados."
    
    finally:
        if con and con.open:
            con.close()