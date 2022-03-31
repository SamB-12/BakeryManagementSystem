import sqlite3


conn = sqlite3.connect('bakerydb.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Employee(
Emp_id INTEGER PRIMARY KEY UNIQUE,
Emp_name TEXT,
Emp_Phone TEXT,
Emp_Address TEXT,
Join_date TEXT,
Salary INTEGER
);''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Customer(
Cust_id INTEGER PRIMARY KEY UNIQUE,
Cust_name TEXT,
Cust_Address TEXT,
Cust_Phone TEXT UNIQUE
);''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Product(
P_id INTEGER PRIMARY KEY UNIQUE,
P_Name TEXT,
Price INTEGER,
Stock INTEGER
); ''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Account(
Username TEXT UNIQUE,
Password TEXT,
PRIMARY KEY(Username)
);''')


cur.execute('''
CREATE TABLE IF NOT EXISTS Transactions(
T_id INTEGER PRIMARY KEY UNIQUE,
Emp_id INTEGER,
Cust_Phone TEXT,
P_id INTEGER,
Quantity INTEGER,
Price INTEGER,
Date TEXT,
FOREIGN KEY(P_id) REFERENCES Product(P_id),
FOREIGN KEY(Cust_Phone) REFERENCES Customer(Cust_Phone),
FOREIGN KEY(Emp_id) REFERENCES Employee(Emp_id)
);''')

conn.commit()







def Choice():
    while True:
        try:
            choice = int(input('Enter your choice:- '))
            return choice
        except:
            print('Enter Valid Literal')







def StockIn():
    print('Stock-In'.center(211,'-'))
    try:
        productId = int(input('Enter the Product ID:-'))
        quant = int(input('Enter the Quantity to StockIn:-'))

        with conn:
            cur.execute('UPDATE Product SET Stock = Stock + ? WHERE P_id = ?',(quant,productId))
            print('The Stock was updated Successfully')
            cur.execute('SELECT Stock,P_Name FROM Product WHERE P_id = ?',(productId,))
            stock = cur.fetchone()

        print('The Quantity of ',str(stock[1]),'is ',str(stock[0]))

        return
    except:
        print('Wrong product ID , try again')
        return



def StockOut():
    print('Stock-out'.center(211,'-'))
    try:
        productId = int(input('Enter the Product ID:-'))
        quant = int(input('Enter the Quantity to stock out:-'))

        with conn:
            cur.execute('SELECT Stock FROM Product WHERE P_id = ?',(productId,))
            stockCheck = cur.fetchone()
            if int(stockCheck[0]) - quant <= 0:
                print('The stock can\'t be zero')
                return
            else:
                cur.execute('UPDATE Product SET Stock = Stock - ? WHERE P_id = ?',(quant,productId))
                print('The Stock was updated Successfully')
                cur.execute('SELECT Stock,P_Name FROM Product WHERE P_id = ?',(productId,))
                stock = cur.fetchone()

                print('The Quantity of ',str(stock[1]),'is ',str(stock[0]))

                return
    except:
        print('Wrong product ID ')
        return



def AddProduct():
    print('Add a New Product'.center(211,'-'))
    try:
        productName = input('Enter Product Name:-')
        price = int(input('Enter the Price:-'))
        stock = int(input('Enter the Initial Stock:-'))

        with conn:
            cur.execute('INSERT INTO Product(P_Name,Price,Stock) VALUES(?,?,?)',(productName,price,stock))
            print('The item was added Successfully')
            cur.execute('SELECT P_id FROM Product WHERE P_Name = ?',(productName,))
            p_id = cur.fetchone()

        print('The Product ID for ',productName,'is ',str(p_id[0]))

        return
    except:
        print('Enter proper Credentials')
        return




def DisplayParticular():
    print('Display'.center(211,'-'))
    try:
        productId = int(input('Enter The product ID : -'))
    except:
        print('Enter numeric product ID')
        return

    try:
        with conn:
            cur.execute('SELECT P_Name FROM Product WHERE P_id = ?',(productId,))
            prodCheck = cur.fetchone()
            if prodCheck[0] == None:
                print('Phone Number Doesn\'t Exist - Enter The proper PhoneNumber' )
    except:
        print('Enter only valid product ID')
        return

    with conn:
        cur.execute('SELECT * FROM Product WHERE P_id = ?',(productId,))
        dispOne = cur.fetchone()
    print()
    print('%20s %20s %20s %20s'%('Product_ID','Product Name','Price','Stock'))
    print()
    print('%20s %20s %20s %20s'%(str(dispOne[0]),str(dispOne[1]),str(dispOne[2]),str(dispOne[3])))

    return



def DisplayAll():
    print('Display'.center(211,'-'))

    with conn:
        cur.execute('SELECT * FROM Product')
        dispAll = cur.fetchall()
    print()
    print('%20s %20s %20s %20s'%('Product_ID','Product Name','Price','Stock'))
    print()
    for row in dispAll:
        print('%20s %20s %20s %20s'%(str(row[0]),str(row[1]),str(row[2]),str(row[3])))

    return



def DisplayProduct():
    while True:
        print('Display'.center(211,'-'))
        print('1.Show a particular product')
        print('2.Show all products')
        print('3.Go back')

        choice = Choice()

        if choice == 1:
            DisplayParticular()
        elif choice == 2:
            DisplayAll()
        else:
            print('Going Back')
            return



def Product():
    while True:
        print('Bakery Management System'.center(211,'-'))
        print('Product'.center(211,'-'))
        print('1.Stock-in')
        print('2.Stock-out')
        print('3.Add a new Product')
        print('4.List of Product')
        print('5.Back to Mainmenu')

        choice = Choice()

        if choice == 1:
            StockIn()
        elif choice == 2:
            StockOut()
        elif choice == 3:
            AddProduct()
        elif choice == 4:
            DisplayProduct()
        else:
            print('Going back to the Mainmenu')
            return







def AddEmployee():
    print('Add an Employee'.center(211,'-'))
    try:
        employeeName = input('Enter the name of Employee:-')
        employeePhoneNumber = input('Enter the Employee Phone Number:-')
        employeeAdress = input('Enter the Adress:-')
        salary = int(input('Enter the Salary:-'))
        joinDate = input('Enter the joining Date:-')

        with conn:
            cur.execute('INSERT INTO Employee(Emp_name,Emp_Phone,Emp_Address,Join_date,Salary) VALUES(?,?,?,?,?)',(employeeName,employeePhoneNumber,employeeAdress,joinDate,salary))
            print('Employee was added Successfully')
            cur.execute('SELECT Emp_id FROM Employee WHERE Emp_name = ?',(employeeName,))
            e_id = cur.fetchone()

        print('The employee id for ',employeeName,'is ',str(e_id[0]))

        return
    except:
        print('Enter proper salary')
        return



def RemoveEmployee():
    print('Remove an Employee'.center(211,'-'))
    try:
        employeeId = int(input('Enter the Employee ID to be removed '))
    except:
        print('Enter only numeric ID')
        return

    try:
        with conn:
            cur.execute('SELECT Emp_name FROM Employee WHERE Emp_id = ?',(employeeId,))
            empCheck = cur.fetchone()
            if empCheck[0] == None:
                print('Employee Doesn\'t exist' )
    except:
        print('Enter only valid Employee ID')
        return

    with conn:
        cur.execute('SELECT Emp_name FROM Employee WHERE Emp_id = ?',(employeeId,))
        e_name = cur.fetchone()
        cur.execute('DELETE FROM Employee WHERE Emp_id = ?',(employeeId,))

    print('Employee ',str(e_name[0]), 'Removed Successfully')

    return



def DisplayEmployee():
    print('List of Employees'.center(211,'-'))

    with conn:
        cur.execute('SELECT * FROM Employee')
        empAll = cur.fetchall()
    print()
    print('%20s %20s %20s %20s %20s %20s'%('Employee_ID','Employee Name','Phone','Address','Join Date','Salary'))
    print()
    for row in empAll:
        print('%20s %20s %20s %20s %20s %20s'%(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5])))

    return





def Employee():
    while True:
        print('Bakery Management System'.center(211,'-'))
        print('Employee'.center(211,'-'))
        print('1.Add an Employee')
        print('2.Remove an Employee')
        print('3.List of All Employees')
        print('4.Back to Mainmenu')

        choice = Choice()

        if choice == 1:
            AddEmployee()
        elif choice == 2:
            RemoveEmployee()
        elif choice == 3:
            DisplayEmployee()
        else:
            print('Going Back')
            return







def AddCustomer():
    print('Add a New Customer'.center(211,'-'))
    try:
        customerName = input('Enter the customer name:-')
        customerAddress = input('Enter the Address:-')
        customerPhone = input('Enter the Phone Number:-')

        with conn:
            cur.execute('INSERT INTO Customer(Cust_name,Cust_Address,Cust_Phone) VALUES(?,?,?)',(customerName,customerAddress,customerPhone))
            print('Customer was added Successfully')
            cur.execute('SELECT Cust_id FROM Customer WHERE Cust_name = ?',(customerName,))
            customerId = cur.fetchone()

        print('The customer id for ',customerName, 'is ',str(customerId[0]))

        return
    except:
        print('Customer Already Exists')
        return



def DisplayAllCustomer():
    print('Display Customer'.center(211,'-'))

    with conn:
        cur.execute('SELECT * FROM Customer')
        custAll = cur.fetchall()
        print()
        print('%20s %20s %20s %20s'%('Customer_ID','Customer Name','Address','Phone'))
        print()

        for row in custAll:
            print('%20s %20s %20s %20s'%(str(row[0]),str(row[1]),str(row[2]),str(row[3])))

        return



def DisplayOneCustomer():
    print('Display Customer'.center(211,'-'))

    try:

        customerPhone = input('Enter the Phone Number of the Customer:-')

        with conn:
            cur.execute('SELECT Cust_name FROM Customer WHERE Cust_Phone = ?',(customerPhone,))
            phoneCheck = cur.fetchone()
            if phoneCheck[0] == None:
                print('Wrong Phone Number Try Again')
                return
            else:
                with conn:
                    cur.execute('SELECT * FROM Customer WHERE Cust_Phone = ?',(customerPhone,))
                    custOne = cur.fetchone()
                    print()
                    print('%20s %20s %20s %20s'%('Customer_ID','Customer Name','Address','Phone'))
                    print()
                    print('%20s %20s %20s %20s'%(str(custOne[0]),str(custOne[1]),str(custOne[2]),str(custOne[3])))

                return
    except:
        print('Wrong Entry Try Again')
        return


def DisplayCustomer():
    while True:
        print('Display Customer'.center(211,'-'))
        print('1.Display Particular Customer Details')
        print('2.Print All Customer Details')
        print('3.Go Back')

        choice = Choice()

        if choice == 1:
            DisplayOneCustomer()
        elif choice == 2:
            DisplayAllCustomer()
        else:
            print('Going Back')
            return



def Customer():
    while True:
        print('Bakery Management System'.center(211,'-'))
        print('Customer'.center(211,'-'))
        print('1.Add a new Customer')
        print('2.Show Customer details')
        print('3.Go Back')

        choice = Choice()

        if choice == 1:
            AddCustomer()
        elif choice == 2:
            DisplayCustomer()
        else:
            print('Going Back')
            return







def Purchase():
    print('Purchase'.center(211,'-'))
    try:
        try:
            customerPhone = int(input('Enter the Phone Number:-'))
            employeeId = int(input('Enter the employeeId:-'))
        except:
            print('Enter only Numeric')
            return
        try:
            with conn:
                cur.execute('SELECT Cust_name FROM Customer WHERE Cust_Phone = ?',(customerPhone,))
                phoneCheck = cur.fetchone()
                if phoneCheck[0] == None:
                    print('Phone Number Doesn\'t Exist - Enter The proper PhoneNumber' )
        except:
            print('Enter only valid phone Number')
            return

        try:
            with conn:
                cur.execute('SELECT Emp_name FROM Employee WHERE Emp_id = ?',(employeeId,))
                empCheck = cur.fetchone()
                if empCheck[0] == None:
                    print('Phone Number Doesn\'t Exist - Enter The proper PhoneNumber' )
        except:
            print('Enter only valid Employee ID')
            return

        totalPrice = 0
        date = input('Enter the Date:-')
        while True:
            productId = input('Enter the product id:-')
            if productId == '':
                break
            try:
                productId = int(productId)
            except:
                print('Enter only productid')
                return
            quantity = int(input('Enter the quantity:-'))
            with conn:
                cur.execute('SELECT Stock FROM Product WHERE P_id = ?',(productId,))
                stockCheck = cur.fetchone()
                if int(stockCheck[0]) - quantity <= 0:
                    print('Insufficent Stock')
                    continue
                else:
                    cur.execute('SELECT P_Name,Price FROM Product WHERE P_id = ?',(productId,))
                    priceOne = cur.fetchone()
                    price = (int(priceOne[1])*quantity)
                    totalPrice += price
                    print('The price of ',quantity,str(priceOne[0]),'is ',price)
                    cur.execute('INSERT INTO Transactions(Emp_id,Cust_Phone,P_id,Quantity,Price,Date) VALUES(?,?,?,?,?,?)',(employeeId,customerPhone,productId,quantity,price,date))
                    cur.execute('UPDATE Product SET Stock = Stock - ? WHERE P_id = ?',(quantity,productId))

                print('The total Price of the session is ',totalPrice)

        return
    except:
        print('Wrong Entry Please try again')
        return





def AllTransactionHistory():
    print('Transaction History'.center(211,'-'))
    date = input('Enter the date Required:-')


    with conn:
        cur.execute('''SELECT T.T_id,P.P_id,C.Cust_name,C.Cust_Phone,E.Emp_name,P.P_Name,T.Quantity,T.Price
         FROM Transactions T, Product P,Customer C,Employee E
          WHERE E.Emp_id = T.Emp_id
          AND C.Cust_Phone = T.Cust_Phone
          AND P.P_id = T.P_id
          AND T.Date = ?''',(date,))
        dispAll = cur.fetchall()
        print()
        print('%20s %20s %20s %20s %20s %20s %20s %20s'%('Transaction_ID','Product ID','Customer Name','Customer Phone','Employee Name','Product Name','Quantity','Price'))
        print()

        for row in dispAll:
            print('%20s %20s %20s %20s %20s %20s %20s %20s'%(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7])))

        return



def CustomerAllTransactionHistory():
    print('Transaction History'.center(211,'-'))
    try:
        phoneNumber = input('Enter the phone number of the customer:-')

        with conn:
            cur.execute('SELECT Cust_name FROM Customer WHERE Cust_Phone = ?',(phoneNumber,))
            custName = cur.fetchone()
            print('The customer name is ',str(custName[0]))
            cur.execute('''SELECT T.T_id,E.Emp_name,P.P_Name,T.Quantity,T.Price,T.Date
            FROM Transactions T,Employee E,Product P,Customer C
            WHERE C.Cust_Phone = T.Cust_Phone
            AND P.P_id = T.P_id
            AND E.Emp_id = T.Emp_id
            AND T.Cust_Phone = ?''',(phoneNumber,))
            custAll = cur.fetchall()
            print()
            print('%20s %20s %20s %20s %20s %20s '%('Transaction_ID','Employee_Name','Product_Name','Quantity','Price','Date_of_Purchase'))
            print()

            for row in custAll:
                print('%20s %20s %20s %20s %20s %20s '%(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5])))

        return
    except:
        print('Wrong Phone Number - Try again')
        return




def CustomerParticularTransactionHistory():
    print('Transaction History'.center(211,'-'))
    try:
        phoneNumber = input('Enter the phone number of the customer:-')
        dateOfTransaction = input('Enter the date of Transaction:-')

        with conn:
            cur.execute('SELECT Cust_name FROM Customer WHERE Cust_Phone = ?',(phoneNumber,))
            custName = cur.fetchone()
            print('The Transaction of  ',str(custName[0]),' on ',dateOfTransaction,'is ')
            cur.execute('''SELECT T.T_id,E.Emp_name,P.P_Name,T.Quantity,T.Price
            FROM Transactions T,Employee E,Product P,Customer C
            WHERE C.Cust_Phone = T.Cust_Phone
            AND P.P_id = T.P_id
            AND E.Emp_id = T.Emp_id
            AND T.Cust_Phone = ?
            AND T.Date = ?''',(phoneNumber,dateOfTransaction))
            custParticular = cur.fetchall()
            print()
            print('%20s %20s %20s %20s %20s '%('Transaction_ID','Employee_Name','Product_Name','Quantity','Price'))
            print()

            for row in custParticular:
                print('%20s %20s %20s %20s %20s '%(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4])))

        return
    except:
        print('Wrong phoneNumber try again')
        return




def CustomerTransactionHistory():
    while True:
        print('Transaction History'.center(211,'-'))
        print('1.Display All Transaction of A particular Customer')
        print('2.Display Transaction on a Particular Date')
        print('3.Go Back')

        choice = Choice()

        if choice == 1:
            CustomerAllTransactionHistory()
        elif choice == 2:
            CustomerParticularTransactionHistory()
        else:
            print('Going Back')
            return




def EmployeeAllTransactionHistory():
    print('Transaction History'.center(211,'-'))
    try:
        employeeId = input('Enter the employee ID of the Employee:-')

        with conn:
            cur.execute('SELECT Emp_name FROM Employee WHERE Emp_id = ?',(employeeId,))
            employeeName = cur.fetchone()
            print('The Employee name is ',str(employeeName[0]))
            cur.execute('''SELECT T.T_id,C.Cust_name,P.P_Name,T.Quantity,T.Price,T.Date
            FROM Transactions T,Employee E,Product P,Customer C
            WHERE C.Cust_Phone = T.Cust_Phone
            AND P.P_id = T.P_id
            AND E.Emp_id = T.Emp_id
            AND T.Emp_id = ?''',(employeeId,))
            custAll = cur.fetchall()
            print()
            print('%20s %20s %20s %20s %20s %20s '%('Transaction_ID','Customer_Name','Product_Name','Quantity','Price','Date_of_Purchase'))
            print()

            for row in custAll:
                print('%20s %20s %20s %20s %20s %20s '%(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5])))

        return
    except:
        print('Wrong ID try again')
        return




def EmployeeParticularTransactionHistory():
    print('Transaction History'.center(211,'-'))
    try:
        employeeId = input('Enter the Employee ID of the Employee:-')
        dateOfTransaction = input('Enter the date of Transaction:-')

        with conn:
            cur.execute('SELECT Emp_name FROM Employee WHERE Emp_id = ?',(employeeId,))
            employeeName = cur.fetchone()
            print('The Transaction of  ',str(employeeName[0]),' on ',dateOfTransaction,'is ')
            cur.execute('''SELECT T.T_id,C.Cust_name,P.P_Name,T.Quantity,T.Price
            FROM Transactions T,Employee E,Product P,Customer C
            WHERE C.Cust_Phone = T.Cust_Phone
            AND P.P_id = T.P_id
            AND E.Emp_id = T.Emp_id
            AND T.Emp_id = ?
            AND T.Date = ?''',(employeeId,dateOfTransaction))
            custParticular = cur.fetchall()
            print()
            print('%20s %20s %20s %20s %20s '%('Transaction_ID','Customer_Name','Product_Name','Quantity','Price'))
            print()

            for row in custParticular:
                print('%20s %20s %20s %20s %20s '%(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4])))

        return
    except:
        print('Wrong Id try again')
        return




def EmployeeTransactionHistory():
    while True:
        print('Transaction History'.center(211,'-'))
        print('1.Display All Transaction carried out by a Particular Employee')
        print('2.Display Transactions carried out by on a Particular Date')
        print('3.Go Back')

        choice = Choice()

        if choice == 1:
            EmployeeAllTransactionHistory()
        elif choice == 2:
            EmployeeParticularTransactionHistory()
        else:
            print('Going Back')
            return




def RecentTransaction():
    print('Transaction History'.center(211,'-'))
    print('The Last 20 Transactions are')


    try:
        with conn:
            cur.execute('''SELECT T.T_id,P.P_id,C.Cust_name,C.Cust_Phone,E.Emp_name,P.P_Name,T.Quantity,T.Price,T.Date
             FROM Transactions T, Product P,Customer C,Employee E
             WHERE E.Emp_id = T.Emp_id
             AND C.Cust_Phone = T.Cust_Phone
             AND P.P_id = T.P_id
             ORDER BY T_id DESC
             LIMIT 20''')
            dispAll = cur.fetchall()
            print()
            print('%20s %20s %20s %20s %20s %20s %20s %20s %20s'%('Transaction_ID','Product ID','Customer Name','Customer Phone','Employee Name','Product Name','Quantity','Price','Date'))
            print()

            for row in dispAll:
                print('%20s %20s %20s %20s %20s %20s %20s %20s %20s'%(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7]),str(row[8])))

            return
    except:
        print('There\'s a problem mate' )
        return





def DisplayTransactionHistory():
    while True:
        print('Bakery Management System'.center(211,'-'))
        print('Transaction History'.center(211,'-'))
        print('1.Choose All Transaction History by Date')
        print('2.Choose Transaction History of Particular Customer')
        print('3.Choose Transaction History of Particular Employee')
        print('4.Last 20 Transaction')
        print('5.Go Back')

        choice = Choice()

        if choice == 1:
            AllTransactionHistory()
        elif choice == 2:
            CustomerTransactionHistory()
        elif choice == 3:
            EmployeeTransactionHistory()
        elif choice == 4:
            RecentTransaction()
        else:
            print('Going Back ')
            return




def Transaction():
    while True:
        print('Bakery Management System'.center(211,'-'))
        print('Transaction'.center(211,'-'))
        print('1.New Customer')
        print('2.Existing Customer')
        print('3.Transaction History')
        print('4.Go Back')

        choice = Choice()

        if choice == 1:
            AddCustomer()
        elif choice == 2:
            Purchase()
        elif choice == 3:
            DisplayTransactionHistory()
        else:
            print('Going Back')
            return








def mainMenu():
    while True:
        print('Bakery Management System'.center(211,'-'))
        print('Main Menu'.center(211,'-'))
        print('1.Product')
        print('2.Employee')
        print('3.Customer')
        print('4.Transaction')
        print('5.Log Out')

        choice = Choice()

        if choice == 1:
            Product()
        elif choice == 2:
            Employee()
        elif choice == 3:
            Customer()
        elif choice == 4:
            Transaction()
        else:
            print('Going back to the login screen')
            return




def Login():
    print('User Login'.center(211,'-'))
    userName = input('Enter the Username:-')
    password = input('Enter the Password:-')

    try:
        with conn:
            cur.execute('SELECT Username,Password FROM Account WHERE Username = ?',(userName,))
            cred = cur.fetchone()

            if userName == str(cred[0]) and password == str(cred[1]):
                print('Login Successful')
                mainMenu()
            else:
                print('Wrong Credentials - Try after sometime')
                return
    except:
        print('Account Doesn\'t Exist - Make a new One')
        return

def Register():
    print('User Registration'.center(211,'-'))
    userName = input('Enter the userName:-')
    try:
        with conn:
            cur.execute('SELECT Username FROM Account WHERE Username = ?',(userName,))
            name = cur.fetchone()
            if userName == str(name[0]) :
                print('This userName Already Exists , Try after sometime')
                return
    except:
        print('The Username is ',userName)
    password = input('Enter the password:-')
    rePassword = input('Reenter the password:-')
    if password == rePassword:
        print('Account Created Successfully')

        with conn:
            cur.execute('INSERT INTO Account VALUES(?,?)',(userName,password))

        return
    else:
        print('Account Creation Failed - retry after sometime')
        return




while True:
    print('Bakery Management System'.center(211,'-'))
    print('1.Login')
    print('2.Register')
    print('3.Exit')
    print()

    print('Copyright © 2021 All Rights Reserved SamB and KaifGhori Enterprises'.center(211))

    choice = Choice()


    if choice == 1:
        Login()
    elif choice == 2:
        Register()
    else:
        print('Logging out the session')
        conn.commit()
        conn.close()
        exit()
