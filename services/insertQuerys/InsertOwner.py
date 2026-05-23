from src.first_project.services.DbSetup import DataBaseCon as DBC
from src.first_project.schemas.requestDTOs.OwnerDTO import OwnerDTO
import pymysql

class InsertOwner:

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
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
        finally:
            if con and con.open:
                con.close()