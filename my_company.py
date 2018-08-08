import sys
import MySQLdb
from prettytable import PrettyTable
import warnings

warnings.filterwarnings('ignore')


'''----------- Function to establish a connection with database -----------'''
def dbconnect():
    try:
        db = MySQLdb.connect(
            host="127.0.0.1",
            user="<username>",
            passwd="<password>",
        )
    except Exception as e:
        sys.exit("Can't connect to Database")
    return db

class MyCompany:
    def __init__(self, emp_id, first_name, last_name,gender, age):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age

    def emp_profile(self):
        db = dbconnect()
        cursor = db.cursor()

        # for creating database this line will hide warning
        cursor.execute("SET sql_notes = 0;")

        # Create Database:
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format("my_company"))

        """Note: Create Database and Tables."""
        cursor.execute("SET sql_notes = 0;")

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS {}.{}(emp_id INT PRIMARY KEY UNIQUE KEY auto_increment,
                                                first_name VARCHAR(30),
                                                last_name VARCHAR(30),
                                                gender ENUM('M','F'),
                                                age INT,
                                                dept_name VARCHAR(30),
                                                position VARCHAR(30));""".format("my_company", "employee"))
        cursor.execute("SET sql_notes = 1;")

        try:
            cursor.execute("""INSERT INTO {}.{}(emp_id,first_name,last_name,gender,age)
                                                 VALUES (%s,%s,%s,%s,%s)""".format("my_company","employee"),
                           (self.emp_id, self.first_name, self.last_name, self.gender, self.age))
        except:
            print "Employee Already Exists.. Try Again."
        db.commit()
        return self.emp_id, self.first_name, self.last_name, self.gender, self.age

'''custom function to check if employee already exists or not ----start'''
def emp_exists_or_not(emp_id):
    db = dbconnect()
    cursor = db.cursor()
    cursor.execute("""SELECT COUNT(1) FROM my_company.employee
                                            WHERE emp_id = {}""".format(emp_id))
    emp_exists = cursor.fetchone()[0]
    return emp_exists

'''--------end----------'''

''' Function to show all employees '''
def all_profiles():
    db = dbconnect()
    cursor = db.cursor()
    cursor.execute("SELECT emp_id,first_name, last_name, gender, age, dept_name, position FROM my_company.employee")
    data = cursor.fetchall()
    j = PrettyTable(["emp_id", "first_name", "last_name", "gender", "age", "dept_name", "position"])
    j.title = 'Results for method Foo'
    for row in data:
        j.add_row([row[0],row[1], row[2],row[3], row[4], row[5], row[6]])
    print j

''' Function to show single employee profile '''
def single_profile(emp_id):
    db = dbconnect()
    cursor = db.cursor()

    cursor.execute("""SELECT COUNT(1) FROM my_company.employee
                    WHERE emp_id = {}""".format(emp_id))
    aaa = cursor.fetchone()[0]

    if aaa == 1:
        cursor.execute("""SELECT emp_id,first_name, last_name, gender, age, dept_name, position FROM my_company.employee
                           WHERE emp_id = {}""".format(emp_id))
        data =cursor.fetchone()
        j = PrettyTable(["emp_id", "first_name", "last_name", "gender", "age", "dept_name", "position"])
        j.title = 'Newly Created Employee'
        j.add_row([data[0], data[1], data[2], data[3], data[4], data[5], data[6]])
        print j
    else:
        print "sorry"

class CompanyDepartment(MyCompany):
    def __init__(self, emp_id, first_name, last_name,gender, age,dept_name,position):
        MyCompany.__init__(self, emp_id, first_name, last_name,gender,age)
        self.dept_name = dept_name
        self.position = position

    def departments(self):
        db = dbconnect()
        cursor = db.cursor()


        try:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS {}.{}(emp_id INT UNIQUE KEY,first_name VARCHAR(30),last_name VARCHAR(30),gender ENUM('M','F'),
                    age INT,dept_name VARCHAR(30),position VARCHAR(30),FOREIGN KEY(emp_id) REFERENCES my_company.employee (emp_id));""".format("my_company", "departments"))
            cursor.execute("SET sql_notes = 1;")

            cursor.execute("""UPDATE {}.{}
                                SET dept_name = %s, position = %s
                                WHERE emp_id = %s""".format("my_company","employee"),(self.dept_name,self.position,self.emp_id))

            cursor.execute("""UPDATE {}.{}
                                SET dept_name = %s, position = %s
                                WHERE emp_id = %s""".format("my_company", "departments"),(self.dept_name, self.position, self.emp_id))

        except MySQLdb.IntegrityError as e:
            print "Duplicate entry, Please try again \n", e

    '''Custom function to update Department and Position'''
    def update_dept_position(self):
        db = dbconnect()
        cursor = db.cursor()
        try:
            cursor.execute("""UPDATE {}.{}
                                SET dept_name = %s, position = %s
                                WHERE emp_id = %s""".format("my_company", "employee"),(self.dept_name, self.position, self.emp_id))

            cursor.execute("""UPDATE {}.{}
                                SET dept_name = %s, position = %s
                                WHERE emp_id = %s""".format("my_company", "departments"),(self.dept_name, self.position, self.emp_id))
        except MySQLdb.IntegrityError as e:
            print "Please try again \n", e

    '''Custom function to Insert, update Department name and Position in Employee and Departments table '''
    def create_department(self):
        db = dbconnect()
        cursor = db.cursor()
        try:
            cursor.execute("""INSERT INTO my_company.departments(emp_id,first_name,last_name,gender,age,dept_name,position)
                                SELECT * FROM my_company.employee
                                WHERE emp_id = {}
                                ON DUPLICATE KEY UPDATE emp_id = %s""".format(self.emp_id),(self.emp_id))

            cursor.execute("""UPDATE {}.{}
                                SET dept_name = %s, position = %s
                                WHERE emp_id = %s""".format("my_company", "employee"),(self.dept_name, self.position, self.emp_id))

            cursor.execute("""UPDATE {}.{}
                                SET dept_name = %s, position = %s
                                WHERE emp_id = %s""".format("my_company", "departments"),(self.dept_name, self.position, self.emp_id))
        except MySQLdb.IntegrityError as e:
            print "Please try again \n", e
        db.commit()

'''Create New employee if not exists'''
def create_new_emp():
    print "\n--------Create New Employee-------------\n"

    while True:
        emp_id = raw_input("Employee ID: ")

        if emp_id.isdigit():
            emp_exists = emp_exists_or_not(emp_id)
            if emp_exists != 1:
                break
            print "Sorry Employee already exists"
        else:
            print "Please enter a number"

    while True:
        first_name = raw_input("First Name: ")
        if first_name.isalpha():
            break
        print "Please enter a alphabet"

    while True:
        last_name = raw_input("Last Name: ")
        if last_name.isalpha():
            break
        print "Please enter a alphabet"

    while True:
        gender = raw_input("Gender : ")
        if gender == "m" or gender == "f":
            break
        print "Please enter 'm' for Male or 'f' for Female"

    while True:
        age = raw_input("Age: ")
        if age in str(range(1, 100)):
            break
        print "Enter valid age"

    MyCompany(emp_id, first_name, last_name, gender, age).emp_profile()
    single_profile(emp_id)

''' ----------- Main function to call the main manu -------------------'''
def main():
    print "========= User choices ==========\n 1 : Show all employee\n 2 : Create New Employee\n 3 : Add Employee to the Department"
    # user_input = input("\nEnter choice ")
    while True:
        user_input = raw_input("\nEnter choice ")
        if user_input == '1' or user_input == '2' or user_input == '3':
            break
        print "Please enter a valid option "

    if user_input=='1':
        all_profiles()
        main()
    elif user_input=='2':
        create_new_emp()
        main()

    elif user_input == '3':
        while True:
            emp_id = raw_input("\nEmployee ID: ")

            if emp_id.isdigit():
                break
            print "please enter number"
        emp_exists = emp_exists_or_not(emp_id)
        if emp_exists == 0:

            print "Warning: Sorry Employee Not exists\n"
            print "========= Sorry Employee Not exists ==========\nWhat would you like to do?\n 1 : Create a New Employee\n 2 : Return to main menu"
            while True:
                user_input = raw_input("\nEnter choice!! ")
                if user_input == '1' or user_input == '2':
                    break
                print "Please enter a valid option either 1 or 2"
            if user_input == '1':
                create_new_emp()
                print "Would you like to assign Department and Position to the New Employee now?\n 1 : Yes\n 2: Main Menu"
                while True:
                    user_input = raw_input("\nEnter choice ")
                    if user_input == '1' or user_input == '2':
                        break
                    print "Please enter a valid option "
                if user_input=='1':
                    while True:
                        dept_name = raw_input("Department Name: ")
                        if dept_name.isalpha():
                            break
                        print "Please enter a alphabet"
                    while True:
                        position = raw_input("Position: ")
                        if position.isalpha():
                            break
                        print "Please enter a alphabet"
                    CompanyDepartment(emp_id, "", "", "", "", dept_name, position).departments()
                    CompanyDepartment(emp_id, "", "", "", "", dept_name, position).create_department()
                elif user_input=='2':
                    main()

            elif user_input == '2':
                main()

        elif emp_exists ==1:

            print "Now assign the Department and Position to New Employee"

            db = dbconnect()
            cursor = db.cursor()
            cursor.execute("""SELECT COUNT(dept_name) FROM my_company.employee
                                                                WHERE emp_id = {} """.format(emp_id))

            dept_pos_exists = cursor.fetchone()[0]

            if dept_pos_exists !=1:
                while True:
                    dept_name = raw_input("Department Name: ")
                    if dept_name.isalpha():
                        break
                    print "Please enter a alphabet"
                while True:
                    position = raw_input("Position: ")
                    if position.isalpha():
                        break
                    print "Please enter a alphabet"
                CompanyDepartment(emp_id, "", "", "", "", dept_name, position).create_department()

            elif dept_pos_exists ==1:
                print "Would you like to update employee Department & Position ?\n 1 : Update employee Department & Position\n 2 : Return to main menu"
                while True:
                    user_input = raw_input("\nEnter choice ")
                    if user_input == '1' or user_input == '2':
                        break
                    print "Please enter a valid option either"
                if user_input == '1':
                    while True:
                        dept_name = raw_input("Department Name: ")
                        if dept_name.isalpha():
                            break
                        print "Please enter a alphabet"
                    while True:
                        position = raw_input("Position: ")
                        if position.isalpha():
                            break
                        print "Please enter a alphabet"
                    CompanyDepartment(emp_id, "", "", "", "", dept_name, position).create_department()
                    CompanyDepartment(emp_id, "", "", "", "", dept_name, position).update_dept_position()
                    main()
                elif user_input == '2':
                    main()
main()
