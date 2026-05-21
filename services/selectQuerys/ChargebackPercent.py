from services.DbSetup import DataBaseCon as DBC
from datetime import date
from langchain.tools import tool
import pymysql

class ChargebackPercent:

    @tool
    @staticmethod
    def selectChargebackPercent(storeID:int,initialDate:date,finalDate:date) -> str:
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql=''' SELECT 

                        SUM(transaction_value) AS total_values,
                        COUNT(*) as total_transactions,
                        COUNT(*) (CASE WHEN transaction_status = "CHARGEBACK" THEN 1 END) as total_chargeback,
                        (COUNT(CASE WHEN transaction_status = "CHARGEBACK" THEN 1 END)/(COUNT(*)))*100 as tax_chargeback,

                        FROM transactions
                        WHERE transaction_id_fk=%s and transaction_date BETWEEN %s and %s
                     '''
                cur.execute(sql,(storeID,initialDate,finalDate))
                response = cur.fetchall()
                
                if response:
                    data = response[0]
                    report = f'''
                    Relatório financeiro da loja de ID:{storeID}, entre as datas de {initialDate} e {finalDate}\n
                    Valor total de vendas{data['total_values']}\n
                    Total de transações:{data['total_transactions']}\n
                    Total de chargebacks:{data["total_chargebacks"]}\n
                    Taxa de chargeback:{data["tax_chargeback"]:.2f}%\n
                    '''
                
                return report


        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
        finally:
            if con and con.open:
                con.close()