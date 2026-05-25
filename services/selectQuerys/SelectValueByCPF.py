from services.DbSetup import DataBaseCon as DBC
from langchain.tools import tool
import pymysql

class ValueByCPF:

    @tool
    @staticmethod
    def selectValueByCPF(cpf:str):
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''
                SELECT
                transaction_cpf AS CPF,
                SUM(transaction_value) AS total_value,
                COUNT(*) AS total_transactions
                FROM transactions

                WHERE transaction_date >= NOW() - INTERVAL 1 DAY 
                AND transaction_cpf = %s
                GROUP BY transaction_cpf
                        '''
                cur.execute(sql,(cpf,))
                response = cur.fetchall()
                if response:
                        data = response[0]
                        report = f'''Relatório de valor total de compras no CPF :{cpf} nas últimas 24 horas\n
                        valor total: {data['total_value']}
                        quantidade de compras: {data['total_transactions']}

                         '''
                        return report
                return "nenhuma compra neste CPF nas últimas 24 horas. "
            
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
       