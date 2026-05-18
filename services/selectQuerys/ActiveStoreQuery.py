from services.DbSetup import DataBaseCon as DBC
import pymysql


class ActiveStore:

    @staticmethod
    def ActiveStore(storeID:int)->bool:
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = 'SELECT is_active FROM store WHERE id = %s'
                cur.execute(sql,storeID)
                boolResponse = cur.fetchone()

                if boolResponse:
                    return True
                return False
            
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
        finally:
            if con and con.open:
                con.close()