import mysql.connector
from mysql.connector import Error


class Database():
    def __init__(self,
                 host="localhost",
                 port="3300",
                 database="banks_portal",
                 user='root',
                 password='root'):

        self.host       = host
        self.port       = port
        self.database   = database
        self.user       = user
        self.password   = password
        self.connect()
    

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host         = self.host,
                port         = self.port,
                database     = self.database,
                user         = self.user,
                password     = self.password)
            
            if self.connection.is_connected():
                return
        except Error as e:
            print("Error while connecting to MySQL", e)
    

    def getAllAccounts(self):
        if self.connection.is_connected():
            self.cursor= self.connection.cursor();
            query = "select * from accounts"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def getAllTransactions(self):
        ''' Complete the method to execute
                query to get all transactions'''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "SELECT * FROM transactions"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
       
    def deposit(self, accountID, amount):
        ''' Complete the method that calls store procedure
                    and return the results'''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            params = (accountID, amount)
            self.cursor.callproc('deposit', params)
            result = self.cursor.stored_results()
            return result.fetchone()[0]
   

    def withdraw(self, p_accountID, p_amount):
        ''' Complete the method that calls store procedure
                    and return the results'''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            params = (p_accountID, p_amount)
            self.cursor.callproc('withdraw', params)
            self.connection.commit()

            result_sets = list(self.cursor.stored_results())
            if len(result_sets) > 0:
                result = result_sets[0].fetchone()
                if result is not None:
                    return result[0]
                else:
                    return None
            else:
                return None

        
    def addAccount(self, ownerName, owner_ssn, balance, account_status):
        ''' Complete the method to insert an
                    account to the accounts table'''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "INSERT INTO accounts(ownerName, owner_ssn, balance, account_status) VALUES (%s, %s, %s, %s)"
            params = (ownerName, owner_ssn, balance, account_status)
            self.cursor.execute(query, params)
            self.connection.commit()
  
    def accountTransactions(self, accountID):
        ''' Complete the method to call
                    procedure accountTransaction return results'''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            params = (accountID,)
            self.cursor.callproc('accountTransactions', params)
            result = self.cursor.stored_results()
            return result.fetchall()
  
    def deleteAccount(self, AccountID):
        ''' Complete the method to delete account
                and all transactions related to account'''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "DELETE FROM accounts WHERE account_id = %s"
            params = (AccountID,)
            self.cursor.execute(query, params)
            self.connection.commit()

            # also delete all transactions associated with this account
            query = "DELETE FROM transactions WHERE account_id = %s"
            self.cursor.execute(query, params)
            self.connection.commit()

    def searchTransactions(self, accountID, start_date, end_date):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor();
            query = "SELECT * FROM transactions WHERE accountID = %s AND transaction_date BETWEEN %s AND %s"
            self.cursor.execute(query, (accountID, start_date, end_date))
            records = self.cursor.fetchall()
            return records

        
        
        
    
    
