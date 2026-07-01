from src.services.DbSetup import DataBaseCon as DBC
from datetime import datetime,time
from langchain.tools import tool
import pymysql



@tool
def selectChargebackPercent(storeID:int,initialDate:datetime,finalDate:datetime) -> str:
    """Essa função retorna um relatório, com o total dos valores das transações, numero total de transações e porcentagem das
        transações que passaram por chargeback
        Argumentos:
        storeID(int): representa o id do estabelecimentono banco
        initialDate(datetime): data inicial para geração do relatório
        finalDate(datetime): data final para geração do relatório, passe o último horário possível para o dia. ex: 11:59:59
        """
    try:
        con = DBC.db_connect()
        with con.cursor() as cur:
            sql=''' SELECT 
                    COALESCE(SUM(transaction_value), 0) AS total_values,
                    COUNT(*) as total_transactions,
                    COUNT(CASE WHEN transaction_status = 'CHARGEBACK' THEN 1 END) as total_chargeback,
                   (COUNT(CASE WHEN transaction_status = 'CHARGEBACK' THEN 1 END) / COUNT(*)) * 100 as tax_chargeback
                
                    FROM transactions
                    WHERE transaction_store_id = %s and transaction_date BETWEEN %s and %s'''
            initialDateQuery = datetime.combine(initialDate.date(),time.max)
            finalDateQuery = datetime.combine(finalDate.date(),time.max)
            cur.execute(sql,(storeID,initialDateQuery,finalDateQuery))
            response = cur.fetchall()
            
            if response:
                data=response[0]
                report = f'''
                Relatório financeiro da loja de ID:{storeID}, entre as datas de {initialDate} e {finalDate}\n
                Valor total de vendas{data['total_values']}\n
                Total de transações:{data['total_transactions']}\n
                Total de chargebacks:{data["total_chargeback"]}\n
                Taxa de chargeback:{data["tax_chargeback"]}%\n
                '''
            
            return report
    except pymysql.MySQLError as e:
        print(f"Erro :{e}")
        return "Erro no banco de dados"
    
