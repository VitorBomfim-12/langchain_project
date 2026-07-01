from src.services.DbSetup import DataBaseCon as DBC
from src.schemas.requestDTOs.StoreDTO import StoreDTO
import pymysql



def insertStore(t: StoreDTO):

    try:
        con = DBC.db_connect()
        with con.cursor() as cur:
            sql = '''INSERT INTO store(
            store_name,
            store_type,
            cnpj,
            transaction_value_limit,
            mcc_code,
            location) 
    
            VALUES(%s,%s,%s,%s,%s,ST_GeomFromText(%s, 4326))'''
            
            point_string = f"POINT({t.location[1]} {t.location[0]})"

            params = (t.storeName,t.storeType,t.cnpj,t.transactionValueLimit,t.mccCode,point_string)
            cur.execute(sql,params)
            con.commit()
            con.close()
    except pymysql.MySQLError as e:
        print(f"Erro :{e}")
        return "Erro no banco de dados."
    
    
        