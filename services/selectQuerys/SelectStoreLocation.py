from first_project.services.DbSetup import DataBaseCon as DBC
import pymysql


class StoreLocation:

    @staticmethod
    def GetLocation(storeID:int)->bool:
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''SELECT 
                ST_X(location) AS lat, 
                ST_Y(location) AS lon 
                FROM store WHERE id = %s
                '''
                cur.execute(sql,storeID)
                localResponse = cur.fetchone()

                return localResponse
            
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
        finally:
            if con and con.open:
                con.close()