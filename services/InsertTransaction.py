from services.DbSetup import DataBaseCon as DBC
from schemas.requestDTOs.TransactionDTO import TransactionDTO
import pymysql

class InsertTransaction:

    @staticmethod
    def insertTransaction(t:TransactionDTO)
        
        try:
            con = DBC.db_connect()
            with con.cursor() as cur:
                sql = '''INSERT INTO transactions(transaction_value,transaction_date,
                transaction_cpf,transaction_location,transaction_status,reason,transaction_store_id_FK'''
                params = (t.value,t.data,t.cpf,t.location,t.status,t.reason,t.storeID)
