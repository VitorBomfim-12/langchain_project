from services.DbSetup import DataBaseCon as DBC
import pymysql
from validate_docbr import CNPJ

class InsertStore:
    @staticmethod
    def insertStore(storeName: str,cnpj:str, mccCode:str,location: str):
        validator = CNPJ()

        if not validator.validate(cnpj):
            return "Erro: cpnj invalido."
        
        cnpjClean = cnpj.replace(".", "").replace("/", "").replace("-", "")
    
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = "INSERT INTO store(store_name,cnpj,mcc_code,location) VALUES(%s,%s,%s,ST_GeomFromText(%s, 4326))"
                cur.execute(sql,(storeName,cnpjClean,mccCode,location))
                con.commit()

        except pymysql.MySQLError as e:
            return f"Erro no banco de dados: {e}"
        
        finally:
            if 'con' in locals() and con.open:
                con.close()