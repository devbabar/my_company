# my_company
Simple script to show basic operation in any organization like display all employee, create new employee, assign department and positions.

# Steps to run this script:
## Step 1.
Create a folder.

$ mkdir my_company

Create a virtual enviroment.

$pip install virtualenv

$ cd my_company

$ virtualenv env

$ source env/bin/activate

## Step 2.
Install requirements.txt

$pip install -r requirements.txt

## Step 3.
In order to establish the connection with database, edit the following function with your own database credentials.

'''----------- Function to establish a connection with database -----------'''

def dbconnect():
    
    try:
       
       db = MySQLdb.connect(
           
           host="127.0.0.1",
           
           user="username", (database username)
           
           passwd="password", (database password)
        )
    except Exception as e:
        sys.exit("Can't connect to Database")
    return db

## Step 4.
Open my_company.py file in PyCharm and run.
