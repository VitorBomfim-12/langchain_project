from services.DbSetup import DataBaseCon as DBC
from schemas.requestDTOs.OwnerDTO import OwnerDTO
import pymysql

class insertOwner:

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
            return f"Erro ao conectar ao banco{e}"
        
        finally:
            if 'con' in locals() and con.open:
                con.close()