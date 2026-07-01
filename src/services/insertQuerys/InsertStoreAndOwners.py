from src.services.DbSetup import DataBaseCon as DBC
from src.schemas.requestDTOs import StoreAndOwnersDTO
from src.services.selectQuerys.ActiveStoreQuery import ActiveStore
from fastapi import HTTPException
import pymysql

def insertStoreAndOwners(t: StoreAndOwnersDTO):
    try:
        if not ActiveStore(t.storeID):
            return "Estabelecimento inativo."
        
        con = DBC.db_connect()
        with con.cursor() as cur:
            sql='INSERT INTO store_owners (owner_id,store_id) VALUES (%s,%s)'
            params = (t.ownerID,t.storeID)
            cur.execute(sql,params)
            con.commit()
            return "Sucesso."
    
    except pymysql.MySQLError as e:
        error_code = e.args[0]
        if error_code == 1062:
            raise HTTPException(status_code=409, detail="Valores já existentes no banco de dados.")
            
        else:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
    
    finally:
        if con.open:
            con.close()