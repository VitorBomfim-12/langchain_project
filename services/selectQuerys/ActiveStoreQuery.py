from services.DbSetup import DataBaseCon as DBC
import pymysql



def ActiveStore(storeID:int)->bool:
    """Essa função retorna um resultado booleano, caso o estabelecimento
    esteja ativo, retorna true, caso contrário, retorna false"""
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
        return False
    
   