# teststoricard

## Description
A simple python app that processes all files in a directory. The file contain a list of debit/credit transactions on an account in csv format.
Transactions could be Credit transactions, marked with + symbol, or Debit transaction, marked with - symbol.

An execution the program show the next information based on the file:
Total balance is 39.74
Number of transactions in July: 2
Number of transactions in August: 2
Average debit amount: -15.38
Average credit amount: 35.25

All the transactions are write in a sqlite db

When finish the process the app will send a email with this information.

## Assumptions 
- We are talking about the same client int this exercise
- For the propouse of evaluation there are no restriction about insertion in DB
- The DB never will be read
- As this is a exercise, the "from" mail and "to" mail are the same. And always be a gmail account. I created an gmail account for this.
- It is necessary to see the result on the terminal
- It is necessary run the app as stand alone app
- For simplicity reasons all the code is in a single script
- The mounted directory is only to share the csv files, so, we dont need a volume

## Parts
- **app.py:** All the program
- **stori.jpg:** unedited logo image 
- **txns.csv:** demo file
- **env:** environment variables file

## Environment variables
- **SC_PRINT_DB_TRANSACTIONS:** *(YES/NO)*: Print at the end of each file all the data in the DB
- **SC_DIR:** csv directory
- **SC_SCV_DELIMITER:**: Delimiter of the csv format
- **SC_DB_NAME:** Name of the database
- **SC_MAIL_FROM:** Gmail account
- **SC_MAIL_TO:** Destination
- **SC_MAIL_PWD:** Password for the from account



## Run

You have 2 ways to run the app

### Stand Alone
- Be sure you have python on your system
- You don´t need the env file. only need *app.py,stori.jpg and txns.csv*
- Copy *app.py,stori.jpg and txns.csv* in the same dir.
- run with *python app.py -d* command. This set a hardcode environment variables
- access to gmail account to see te result (**mail:** *test.storicard@gmail.com*, **pwd:** *JCRStoriCard2022*). **This account will be delete automatically the next week**

### Docker
- Create a directory *(ej. /test)* and copy this files: *app.py,stori.jpg and env*
- Create a subdirectory ej. mountdir and copy *txns.csv*
- In your first directory *(/test)* Build the container: *docker build -t test .*
- Run the container: *docker run --env-file env  test*
- You can chance configuration in *env* file


## Screen Shots
![image](https://user-images.githubusercontent.com/106209282/170161209-74daefff-8125-4fd8-823f-2bd9c4d2abe9.png)
![image](https://user-images.githubusercontent.com/106209282/170161288-d1379a0d-7c98-4bc7-8610-d942c56f6a09.png)
![image](https://user-images.githubusercontent.com/106209282/170161469-f67b083e-24f1-49b5-afe0-b4ea61036273.png)



