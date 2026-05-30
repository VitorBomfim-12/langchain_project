from src.services.DbSetup import DataBaseCon as DBC
import pymysql


class StoreLimitQuery:

    @staticmethod
    def storeLimit(storeID:int)->bool:
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = 'SELECT transaction_value_limit FROM store WHERE id = %s'
                cur.execute(sql,storeID)
                limit = cur.fetchone()

                if limit:
                    return limit['transaction_value_limit']
                
            
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
      