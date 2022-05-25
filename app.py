import argparse
import calendar
import csv
import smtplib
import sqlite3
from os import environ, listdir, path
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage


#Welcom Message
welcom = '\
     _______________________________________________________________________\n\
    | Home Test from Stori Card                                             |\n\
    |                            TECH CHALLENGE                             |\n\
    | App that processes a file.                                            |\n\
    | The file will contain a list of debit and credit transactions on an   |\n\
    |  account                                                              |\n\
    | This app have to:                                                     |\n\
    |  1. Calculate balance                                                 |\n\
    |  2. Show number of transactions per month                             |\n\
    |  3. Send email with this result                                       |\n\
    |                                                                       |\n\
    | ▀▀▀▀█  ▀▀▀▀█  dont judge me                                           |\n\
    |                                                                       |\n\
    | I get fun developing                                    JCR Rules ®   |\n\
    |_______________________________________________________________________|\n\
    '

    
'''
Name of Environment Vars
'''
_SC_DIR                     = 'SC_DIR'
_SC_SCV_DELIMITER           = 'SC_SCV_DELIMITER'
_SC_DB_NAME                 = 'SC_DB_NAME'
_SC_PRINT_DB_TRANSACTIONS   = 'SC_PRINT_DB_TRANSACTIONS'
_SC_MAIL_FROM               = 'SC_MAIL_FROM'
_SC_MAIL_TO                 = 'SC_MAIL_TO'
_SC_MAIL_PWD                = 'SC_MAIL_PWD'

_TRANSACTION_LEGEND     = 'ID:{}\tMONTH:{}\tDAY:{}\tAMOUNT:{:10.2f}\tTOTAL BALANCE:{:10.2f}\tAVG_DEBIT:{:10.2f}\tAVG_CREDIT:{:10.2f}'
_TOTAL_BALANCE_LEGEND   = 'TOTAL BALANCE: {:10.4} AVG DEBIT AMOUNT: {:10.4} AVG CREDIT AMOUNT: {:10.4}'

class Transaction:
    def __init__(self, id, idClient, month, day, amount, totalBalance, averageDebit, averageCredit):
        self.id = id
        self.idClient = idClient
        self.month = month
        self.day = day
        self.amount = amount
        self.totalBalance = totalBalance
        self.averageDebit = averageDebit
        self.averageCredit = averageCredit
        
class Balance:
    def __init__(self):
        self.debit_transactions = 0
        self.debit_total        = 0
        self.credit_transactions= 0
        self.credit_total       = 0;
        self.transactions       = []
        
        self.total_balance      = 0
        self.average_debit      = 0
        self.average_credit     =0
        self.transactions_month ={}
        
    def _increment_transaction_month(self, month):
        if not month in self.transactions_month.keys():
            self.transactions_month[month] = 0
        self.transactions_month[month] = self.transactions_month[month] + 1
    
    def _add_credit(self, amount):
        self.credit_transactions += 1
        self.credit_total += amount
        self.average_credit = self.credit_total / self.credit_transactions
        
    def _add_debit(self, amount):
        self.debit_transactions += 1
        self.debit_total += amount
        self.average_debit = self.debit_total / self.debit_transactions
            
    
    def add_transaction(self, id, month_day, amount):
        date = month_day.split('/')
        month = date[0]
        day = date[1]
        self._increment_transaction_month(int(month))
        self.total_balance += amount
        if amount >= 0:
            self._add_credit(amount)
        else:
            self._add_debit(amount)
            
        transaction = Transaction(id, 1, month, day, amount, self.total_balance, self.average_debit, self.average_credit)
        self.transactions.append(transaction) 
        
        return transaction
    
    def to_string(self):
        to_str = _TOTAL_BALANCE_LEGEND.format(self.total_balance, self.average_debit, self.average_credit) + '\n'

        for t_month in self.transactions_month:
            to_str = to_str + 'Number of transactions in {}: {}'.format(calendar.month_name[t_month], self.transactions_month[t_month]) + '\n'
        
        return to_str
    

class MyDB(object):
    
    _qry_create_transactions ="""
    CREATE TABLE IF NOT EXISTS TRANSACTIONS(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        idClient INTEGER NOT NULL,
        idTransaction INTEGER,
        mounth INTEGER,
        day INTEGER,
        amount REAL,
        totalBalance REAL,
        averageDebit REAL,
        averageCredit REAL
        );
    """
    _qry_add_transaction = """
    INSERT INTO TRANSACTIONS (idClient, idTransaction, mounth, day, amount, totalBalance, averageDebit, averageCredit)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    
    _qry_get_transactions = """
    SELECT * FROM TRANSACTIONS ORDER BY id ASC;
    """
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance =super(MyDB, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        try:
            self.con = sqlite3.connect( environ.get(_SC_DB_NAME) )
            self.__create_test_db()
        except Exception as e:
            print(e)
        
    def __create_test_db(self):
        self.con.execute(MyDB._qry_create_transactions)
        
    def close(self):
        self.con.close()
        
    '''
    Here I have some assumptions:
    1. We are talking about the same client int this exercise, so, idCliet is always the same (1).
    2. For the propouse of evaluation there are no restriction about insertion in DB, 
        in other words, the same file can be processed several times without any kind of error.
    3. As this is a extra point, I assume the summary applies only for file data instead DB. 
        Account story is never read again from DB. If you want to see all records in DB, please, 
        set environment variable SC_PRINT_DB_TRANSACTIONS to "YES"
    '''
    def add_transaction(self, transaction):
        try:
            self.con.execute(MyDB._qry_add_transaction, (transaction.idClient, transaction.id, transaction.month, transaction.day, transaction.amount, transaction.totalBalance, transaction.averageDebit, transaction.averageCredit) )
            self.con.commit()
        except Exception as e:
            print(e)
    
    def get_transactions(self):
        data = self.con.execute(MyDB._qry_get_transactions)
        for row in data:
            print(row)

"""
Start in development mode. Set default values to environment variables
"""
def devolopment_mode():
    environ[_SC_DIR]                    = './'
    environ[_SC_SCV_DELIMITER]          = ','
    environ[_SC_DB_NAME]                = 'my.db'
    environ[_SC_PRINT_DB_TRANSACTIONS]  = 'NO'
    environ[_SC_MAIL_FROM]              = 'test.storicard@gmail.com'
    environ[_SC_MAIL_TO]                = 'test.storicard@gmail.com'
    environ[_SC_MAIL_PWD]               = 'JCRStoriCard2022'
    
    

def process_file(file_name):
    file = open(path.join(environ.get(_SC_DIR), file_name), "r")
    csv_reader = csv.reader(file, delimiter=environ.get(_SC_SCV_DELIMITER))
    next(csv_reader)
    client_balance = Balance()
    for row in csv_reader:
        transaction = client_balance.add_transaction(int(row[0]), row[1], float(row[2]) )
        MyDB().add_transaction(transaction)
    file.close()
    for _, transaction in enumerate(client_balance.transactions):
        print(_TRANSACTION_LEGEND.format(transaction.id, transaction.month, transaction.day, transaction.amount, transaction.totalBalance, transaction.averageDebit, transaction.averageCredit) )
        
    print(client_balance.to_string())
    
    send_mail(client_balance)
        
def send_mail(client_balance):
    
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Your Balance'
    msgRoot['From'] = environ.get(_SC_MAIL_FROM)
    msgRoot['To'] = environ.get(_SC_MAIL_TO)
    msgRoot['Cc'] =''
    msgRoot.preamble = 'Multi-part message in MIME format.'
    
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('<b>Your Balance</b><br/>' + client_balance.to_string().replace('\n','<br/>') + '<br/><img src="cid:image1">', 'html')
    msgAlternative.attach(msgText)
    
    fp = open('stori.jpg', 'rb') #Read image 
    msgImage = MIMEImage(fp.read())
    fp.close()
    
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
    
    context = ssl.create_default_context()
    context.options |= ssl.OP_ALL
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) 
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(environ.get(_SC_MAIL_FROM), environ.get(_SC_MAIL_PWD))
        server.sendmail(environ.get(_SC_MAIL_FROM), environ.get(_SC_MAIL_TO), msgRoot.as_string())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servicios Bautizador")
    parser.add_argument('-d','--dev', required=False, action='store_true', help='Stand Alone Run. Creates default Environment Vars')
    args = parser.parse_args()
    if args.dev:
        devolopment_mode()    
    
    print(welcom)
    
    files = listdir(environ.get(_SC_DIR))
    files = list( filter(lambda f: f.endswith('.csv'), files))
    
    if len(files)==0:
        print('No se han encontrado archivos')
    
    for _, val in enumerate(files):
        try:
            process_file(path.join(environ.get(_SC_DIR), val))
        except Exception as e:
            print(e)
    
    if environ.get(_SC_PRINT_DB_TRANSACTIONS) == 'YES':
        MyDB().get_transactions()
    MyDB().close()
    
    