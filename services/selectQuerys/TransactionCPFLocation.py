from services.DbSetup import DataBaseCon as DBC
import datetime
import pymysql


class TransactionCPFLocation:

    @staticmethod
    def selectTransactionCPFLocation(cpf:str,initialDate:datetime,finalDate:datetime):
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''
                    SELECT
                    transaction_value as value,
                    transaction_location as location,
                    transaction_date as date,
                    transaction_status as status

                    FROM transactions
                    WHERE transaction_cpf = %s and transaction_date BETWEEN %s and %s
                        '''
                
                cur.execute(sql,(cpf,initialDate,finalDate))
                response = cur.fetchall()
                if response:
                    
                    report = f'''Relatório localização e compras no CPF:{cpf}, entre as datas de 
                    {initialDate} e {finalDate}\n'''

                    for t in response:
                        report+=(
                            f'Localização:{t['location']}'
                            f'valor:{t['value']}'
                            f'date{t['date'].strftime('%d/%m/%Y %H:%M')}'
                            f'status:{t['status']}'
                        )
                    return report
                return f'Nenhum relatório encontrado'
        
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
        finally:
            if con and con.open:
                con.close()