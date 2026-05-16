from services.DbSetup import DataBaseCon as DBC
from datetime import date
import pymysql


class SelectTransaction():
    
    @staticmethod
    def selectTransaction(storeID:int,startDate: date,finalDate: date):
        try:
            
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''SELECT * FROM transactions WHERE transaction_store_id_FK  = %s and transaction_date BETWEEN %s and %s'''
                cur.execute(sql,(storeID,startDate,finalDate))
                response = cur.fetchall()
                
                if response:

                    relatorio = f"Número de relatórios econtrados na loja{response["transaction_store_id_FK"]: len(response)}\n"    
                    for t in response:
                        relatorio+=(

                            f'ID- {t['id']}|'
                            f'valor:R${t['transaction_value']}|'
                            f'Data:   {t['transaction_date'].strftime('%d/%m/%Y %H:%M')}|'
                            f'CPF:    {t['transaction_cpf']}|'
                            f'local:  {t['transaction_location']}|'
                            f'status: {t['transaction_status']}|\n'

                        )
                        return relatorio
                    
                return "Nenhum relatório encontrado."
            
        except pymysql.MySQLError as e:
            print(f"Erro técnico ocultado: {e}")
            return "Erro no banco de dados"
        
        finally:
            con.close()
