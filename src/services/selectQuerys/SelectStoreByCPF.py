from src.services.DbSetup import DataBaseCon as DBC
from langchain.tools import tool
import pymysql

@tool
def selectTransaction(cpf:str,storeID:int):
        """  Esta função retorna uma relação entre propietários e suas lojas, deve ser utilizada para
        identificar estas relações e cruzar dados para verificar possíveis fraudes.
            Argumentos:
            cpf: str (cpf a ser procurado)
            storeID: int (ID da loja a ser procurada)"""     
        try:

            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''
                SELECT

                o.cpf AS owner_cpf,
                s.store_id AS store_id_num

                FROM owners o
                INNER JOIN store_owners s ON o.id = s.owners_id
                WHERE o.cpf = %s or s.store_id = %s
                '''
                cur.execute(sql,(cpf,))
                response = cur.fetchall()
                
                if response:

                    report = f"Relação de propietários e lojas, CPF:{cpf}, ID loja:{storeID} "    
                    for t in response:
                        
                        report+=(
                            f'ID- {t['owner_cpf']}|'
                            f'ID- {t['store_id_num']}|'

                        )
                    
                    return report
                    
                return "Nenhum relatório encontrado."
            
        except pymysql.MySQLError as e:
            print(f"Erro :{e}")
            return "Erro no banco de dados"
        
    