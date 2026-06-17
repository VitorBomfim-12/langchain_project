from fastapi import HTTPException
from langchain_project.src.services.DbSetup import DataBaseCon as DBC
from langchain_project.src.schemas.requestDTOs.OwnerDTO import OwnerDTO
import pymysql


@staticmethod
def insertOwner(t: OwnerDTO):
    
    try:
        con = DBC.db_connect()
        with con.cursor() as cur:
            sql = 'INSERT INTO owners (name,cpf,birthday) VALUES (%s,%s,%s)'
            params = (t.name,t.cpf,t.birthday)
            cur.execute(sql,params)
            con.commit()

    except pymysql.MySQLError as e:
        error_code = e.args[0]
        if error_code == 1062:
            raise HTTPException(status_code=409, detail="Valores já existentes no banco de dados.")
    
    finally:
        if con and con.open:
            con.close()