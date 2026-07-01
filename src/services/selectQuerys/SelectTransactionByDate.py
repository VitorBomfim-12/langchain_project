from src.services.DbSetup import DataBaseCon as DBC
from datetime import datetime,time
from langchain.tools import tool
import pymysql

@tool
def selectTransaction(storeID:int,initialDate: datetime,finalDate: datetime):
    """Esta função retorna um relatório contendo todas as compras de um estabelecimento dentro de um período determinado.
        Argumentos:
        storeID : int (id único do estabelecimento)
        initialDate: datetime (data inicial para buscas no banco)
        finalDate: datetime (data final para buscas no banco)
        
        Observação: esta função retorna um relatório extenso, use-a para identificar padrões nas transações"""
        
    try:
        
        con = DBC.db_connect()
        with con.cursor() as cur:
            sql = '''SELECT * 
                            FROM transactions 
                            WHERE transaction_store_id  = %s AND 
                            transaction_date BETWEEN %s AND %s'''
            
            
            initialDateQuery = datetime.combine(initialDate.date(),time.max)
            finalDateQuery = datetime.combine(finalDate.date(),time.max)
            
            cur.execute(sql,(storeID,initialDateQuery,finalDateQuery))
            response = cur.fetchall()
            
            if response:
                report = f"Número de relatórios econtrados na loja de ID:{storeID}: {len(response)}\n"    
                for t in response:
                    
                    report+=(
                        f'ID- {t['id']}|'
                        f'valor:R${t['transaction_value']}|'
                        f'Data:   {t['transaction_date'].strftime('%d/%m/%Y %H:%M')}|'
                        f'CPF:    {t['transaction_cpf']}|'
                        f'local:  {t['transaction_location']}|'
                        f'status: {t['transaction_status']}|\n'
                    )
                
                return report
                
            return "Nenhum relatório encontrado."
        
    except pymysql.MySQLError as e:
        print(f"Erro :{e}")
        return "Erro no banco de dados"
    
   