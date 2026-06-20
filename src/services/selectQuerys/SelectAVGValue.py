from src.services.DbSetup import DataBaseCon as DBC
from datetime import datetime
from langchain.tools import tool
import pymysql



@tool
def getAVGValue(storeID:int,initialDate:datetime,finalDate:datetime)->str:
    """Esta função retorna o valor médio das transações de uma loja.
        Parâmetros:
        storeID: id da loja, para identifica-la no banco.
        initialDate: Data inicial do intervalo para a busca ser feita.
        finalDate: Data final do intervalo para a busca."""
    try:
        con = DBC.db_connect()
        with con.cursor() as cur:
            sql = '''SELECT 
         AVG(transaction_value) as avg_value
        FROM transactions
        WHERE transaction_store_id_FK = %s 
        AND transaction_date BETWEEN %s AND %s
            '''
            cur.execute(sql,(storeID,initialDate,finalDate))
            response = cur.fetchone()
            return response
        
    except pymysql.MySQLError as e:
        print(f"Erro :{e}")
        return "Erro no banco de dados"
    
    