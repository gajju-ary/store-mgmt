import pymysql
import time

# ONE TIME PROCESS 
#Design And Creation Of Database
def createDB():
    dbPort = pymysql.connect(
        host='localhost',
        user='root', #MySQL Username(Device Specific)
        password='@123', #MySQL Password(Device Specific)
    )
    mycursor = dbPort.cursor()
    mycursor.execute("CREATE DATABASE super_market")
    print("DataBase Created Succesfully...")

    #Re-assigning dbPort for Table Creation
    dbPort = pymysql.connect(
        host='localhost',
        user='root', #MySQL Username(Device Specific)
        password='@123', #MySQL Password(Device Specific)
        db = 'super_market'
    )
    mycursor = dbPort.cursor()
    mycursor.execute("CREATE TABLE products(p_name VARCHAR(255), p_quant INT, p_price INT)")
    print("Table Created Succesfully...")


# MySQL Connection function
def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root', #MySQL Username(Device Specific)
        password='@123', #MySQL Password(Device Specific)
        db='super_market',
    )
    return conn

#adding item to super market inventry
def addItem():
    print('\n\n<----------------ADD ITEMS----------------->\n\n')
    print('Please fill details of Product\n')
    p_name = input('Item name : ')
    
    while True:
        try:
            p_quant = int(input('Item quantity : '))
            break
        except ValueError:
                print('Quantity should only be in digits')
    while True:
        try:
            p_price = int(input('Price $ : '))
            break
        except ValueError:
                print('Price should only be in digits')

    try:
        conn = connection()
        cursor = conn.cursor()
        query = "INSERT INTO products VALUES(%s,%s,%s)"
        val = (p_name , p_quant, p_price)
        cursor.execute(query , val)
        conn.commit()
        print(cursor.rowcount,"Record Inserted Successfully...")
        input("Press Enter To Continue...")
        #conn.close()   
    except:
        print("Some Database Error Found")
    finally:
        conn.close()

#view super maarket inventry
def viewItem():
    conn = connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM products")
    myresult = mycursor.fetchall()
    if(len(myresult) > 0):
        print("\n"+str(len(myresult))+" Available Item Found\n")
        print("======================================================")
        print("|     Product Name        Quantity        Price      |")
        print("======================================================")
        for x in myresult:
            print("|%12s %15d %15d        |"%(x[0],x[1],x[2]) )
            print("------------------------------------------------------")
        else:
            print("======================================================\n\n")
    else:
        print("No Item Found...!")
    input("Press Enter to Continue...")

#search item in super market inventry/stock
def search(temp):
    conn = connection()
    mycursor = conn.cursor()
    sql = "SELECT * FROM products WHERE p_name=%s"
    val = (temp,) 
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()

    if(len(myresult) > 0):
        print("\n"+str(len(myresult))+" Item Found\n")
        print("======================================================")
        print("|     Product Name        Quantity        Price      |")
        print("======================================================")
        for x in myresult:
            print("|%12s %15d %15d        |"%(x[0],x[1],x[2]) )
            print("------------------------------------------------------")
        else:
            print("======================================================\n\n")
    else:
        print("\n"+str(len(myresult))+" Item Found\n")
    input("Press Enter to Continue...")
    return len(myresult)

#purchase item(Customer)
def purchase():
    viewItem()
    purchase_item = input("Enter Product Name to Purchase: ")
    purchase_quant = int(input("Enter Quantity Wanted: "))
    
    conn = connection()
    mycursor = conn.cursor()
    sql = "SELECT * FROM products WHERE p_name=%s"
    val = (purchase_item,) 
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()

    if(len(myresult) > 0):
        if(myresult[0][1] != 0):
            if(myresult[0][1] >= purchase_quant):
                cust_name = input("Please Enter Your Name: ")
                print("\nDear {} !\nPay {} $ at Checkout Counter.".format( cust_name,(purchase_quant * myresult[0][2])))
                
                query = "UPDATE products SET p_quant =%s WHERE p_name = %s"
                val = (myresult[0][1] - purchase_quant, purchase_item,)
                mycursor.execute(query , val)
                conn.commit()
                conn.close()
            else:
                print("\nRequired Quantity is Not Available...!")
        else:
            print("\nItem Out Of Stock...!")
    else:
        print("\nNo Item Found in Store...")    
    input("Press Enter to Continue...")

#edit product details
def editItem(temp):
    if(search(temp) > 0):
    
        new_name = input("Enter New Name: ")
        new_quant = int(input("Enter New Quantity: "))
        new_price = int(input("Enter New Price: "))
        try:
            conn = connection()
            cursor = conn.cursor()
            query = "UPDATE products SET p_name =%s, p_quant =%s, p_price = %s WHERE p_name = %s"
            val = (new_name , new_quant, new_price,temp)
            cursor.execute(query , val)
            conn.commit()  
            print(cursor.rowcount, " Product Edited") 
        except:
            print("\nSome Database Error Found")
        finally:
            conn.close()
    else:
        print("\nNo Item Found...")

################################################
#               PROGRAM START POINT            #
print("\n<-------------Program is Starting----------->")
for i in range(1,4):
    print(i,end=" ")
    time.sleep(0.5)
else:
    print("\nProgram is Started")


while True:
    print('\n<------------------WELCOME TO THE SUPERMARKET------------------>\n')
    print('1. Add items to inventory\n2. View items\n3. Search items\n4. Purchase items \n5. Edit items\n6. Exit\n\n99. Create Database and Required Table(Only for Admin)\n')
    ch = int(input('Enter choice : '))

##############################################
    if ch == 99: #Admin Access
        pin = int(input("Enter 4 Digit ADMIN PIN: "))
        if(pin == 0000): #Default Pin 
            try:
                createDB()
            except:
                print("\nOpps!! Database Already Available...\n")
                input("Press Enter Key to Continue....")
        else:
            print("\nI think You Are Not an ADMIN!!!\nTry with Correct Pin...")
            input("Press Enter Key to Continue....")

##############################################
    elif ch == 1:
        addItem()   
###########################################
    elif ch == 2:
        viewItem()
###########################################
    elif ch == 3:
        temp = input("Enter Product Name to Search Item: ")
        search(temp)
###########################################
    elif ch == 4:
        print("<----------Purchase Item----------->")
        purchase()
###########################################
    elif ch == 5:
        temp = input("Enter Product Name to Edit Item: ")
        editItem(temp)
###########################################
    elif ch == 6:
        print('\n\n------------------Thank You For Using App------------------')
        break
##########################################
    else:
        print("Invalid Choice...!")