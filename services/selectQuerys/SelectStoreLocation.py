from src.services.DbSetup import DataBaseCon as DBC
import pymysql


class StoreLocation:

    @staticmethod
    def GetLocation(storeID:int)->str:
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''SELECT 
                ST_X(location) AS lat, 
                ST_Y(location) AS lon,
                eletronic_fence as fence_dis
                FROM store WHERE id = %s
                '''
                cur.execute(sql,storeID)
                localResponse = cur.fetchone()

                return localResponse
            
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
       