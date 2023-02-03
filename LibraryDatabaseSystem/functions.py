#from msilib.schema import tables
from tkinter import *
#import tkinter as tk 
from ctypes import LibraryLoader
from turtle import update
from matplotlib.style import library
from numpy import insert
from sqlalchemy import create_engine
from datetime import date, datetime, timedelta
import mysql.connector
import csv
from test2 import *

# functions
libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")

mycursor = libraryDB.cursor()



#Membership Creation
# add_members = ("INSERT INTO Members " 
#                 "(id, Name, Faculty, PhoneNo, Email) " 
#                 "VALUES (%s, %s, %s, %s, %s)")
# data_member = ("A108C", "Jacky Ong", "Computing", "1234567", "jacky@nus.edu.sg")
# mycursor.execute(add_members, data_member)

# #Commit
# libraryDB.commit()

# def successPopupWithdrawBook():
#     frame = Toplevel()
#     frame.configure(bg="lightgreen")
#     title = Label(frame, text="Success", padx=20, pady=20)
#     title.pack()
#     contents = Label(frame, text="Withdraw Book Success", padx=10, pady=10)
#     contents.pack()
#     button = Button(frame, text="Back to Create Function", command=frame.destroy)
#     button.pack()
#     frame.mainloop()

# def failPopupWithdrawBook_noBook():
#     frame = Toplevel()
#     frame.configure(bg="red")
#     title = Label(frame, text="Fail", padx=20, pady=20)
#     title.pack()
#     contents = Label(frame, text="Withdraw Book not exist", padx=10, pady=10)
#     contents.pack()
#     button = Button(frame, text="Back to Create Function", command=frame.destroy)
#     button.pack()
#     frame.mainloop()

# def failPopupWithdrawBook_bookReserved():
#     frame = Toplevel()
#     frame.configure(bg="red")
#     title = Label(frame, text="Fail", padx=20, pady=20)
#     title.pack()
#     contents = Label(frame, text="Withdraw Book is reserved ", padx=10, pady=10)
#     contents.pack()
#     button = Button(frame, text="Back to Create Function", command=frame.destroy)
#     button.pack()
#     frame.mainloop()

def MembershipCreation(newID, newName, newFac, newPhone, newEmail):
    insert_query  = ("INSERT INTO Members " 
                 "(id, Name, Faculty, PhoneNo, Email) " 
                 "VALUES (%s, %s, %s, %s, %s)")
    new_member = (newID, newName, newFac, newPhone, newEmail)
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    mycursor.execute(insert_query, new_member)
    libraryDB.commit()
    successPopupCreateMembership()
#MembershipCreation("123","123","123","123","123")




#Display Members who have oustanding fines
def FinedMembers():
    fineID_query = "SELECT * FROM Members WHERE Members.id IN (SELECT fineID FROM Fine)"
    mycursor.execute(fineID_query)
    fineID = mycursor.fetchall()
    #fineID = list(map(lambda x: x.remove(','),fineID))
    return fineID
    #print(fineID)
# print ("Members with Outstanding Fines Table")
# print(FinedMembers())


#Membership Update
def updateMembership(newID,newName,newFac, newPhone,newEmail):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",
                               password="lozhihao", database="LIB_ALS")
    # print(mydb)
    mycursor = mydb.cursor()
    input_query = ("""
    UPDATE Members
    SET id = %s, Name = %s, Faculty = %s, PhoneNo = %s, Email = %s
    WHERE id = %s
    """ )
    new_member = (newID.get(),newName.get(),newFac.get(), newPhone.get(),newEmail.get(), newID.get())
    mycursor.execute(input_query, new_member)
    mydb.commit()
    mydb.close()

#Calculate Fine

def fineAmt(memberID):
    pass


#Display Books on loan
def DisplayloanBooks():
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    select_query = "SELECT accNum, Title, Author1, Author2, Author3, isbn, publisher, PublicationYr FROM Books WHERE Books.accNum IN (SELECT borrowNum FROM BorrowReturn WHERE returnDate IS NULL)"
    mycursor.execute(select_query)
    onLoanBooks = mycursor.fetchall()
    return onLoanBooks

#print(DisplayloanBooks())


    


#Display books on Loan for a given MembershipID
def membersLoanBooks(memberID):
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    select_query = "SELECT accNum, Title, Author1, Author2, Author3, isbn, publisher, PublicationYr FROM Books WHERE accNum IN (SELECT accNum FROM Books WHERE Books.accNum IN (SELECT borrowNum FROM BorrowReturn WHERE returnDate IS NULL))"
    mycursor.execute(select_query)
    allBooks = mycursor.fetchall()
    return allBooks
#print(membersLoanBooks('A101A'))



#Books Borrowing
def borrowBook(borrowNum, memberID):
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    fineQuery =  FinedMembers()
    borrowQuery = membersLoanBooks(memberID)
    LoanBooks = DisplayloanBooks()
    borrowReturn_Query = "SELECT * FROM BorrowReturn WHERE borrowNum = %s"
    mycursor.execute(borrowReturn_Query, (borrowNum,))
    borrowReturn = mycursor.fetchall()
    #dueDate = borrowReturn[0][-2]
    #Check for Fine, or borrow quota
    for i in fineQuery:
        if borrowError_Fine():
            borrowError_Fine()#Prompt - "Error! Member has outstanding fines."
    if len(borrowQuery) > 2:
        borrowError_loanQuota()
        return False #Prompt - "Error! Member Loan quota exceeded"
    for i in borrowQuery:
        if borrowNum in i:
            borrowError_BookOnLoan(borrowNum)
            return  False #Prompt Error
    #Else, borrow Book successful
    borrowDate = date.today() #it will be today's date
    #end_date = borrowDate + date.timedelta(days=14)
    borrowSucess_Query = ("INSERT INTO BorrowReturn "
                        "(borrowID, borrowNum, borrowedDate, dueDate, returnDate) "
                        "VALUES (%s, %s, %s, %s, %s)")
    updateNewBook = (memberID, borrowNum, borrowDate,None, None)
    mycursor.execute(borrowSucess_Query, updateNewBook)
    libraryDB.commit()
    successPopupBorrowBook()
    return borrowReturn


#Books Returning
def returnBook(returnNum):
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    todayDate = date.today()
    fineList = FinedMembers()
    loanBook = DisplayloanBooks()
    select_query = "SELECT * FROM (SELECT * FROM BorrowReturn WHERE returnDate is NULL) AS b WHERE b.borrowNum = %s"
    mycursor.execute(select_query, (returnNum,))
    borrowReturn = mycursor.fetchall()
    #return type(todayDate)
    if todayDate > borrowReturn[0][3]:  #if todayDate > dueDate : means got fine to play.
        update_query = "UPDATE BorrowReturn SET returnDate = %s WHERE returnDate is NULL and borrowNum = %s"
        data = (todayDate, returnNum)
        mycursor.execute(update_query, data)
        # [('A601F', 'A50', datetime.date(2021, 2, 1), datetime.date(2021, 2, 15), None)]
        returnBook_SuccessButHasFine()
        #return "Error! Book returned successfully but has fines"
    

#Book Search

def BookSearch(title,authors, publisher,publicationyr,isbn):
    # String manipulation to get the first word only if key in multiple word #
    # titleArray = title.split()
    # if not len(titleArray):
    #     title = titleArray[0]
    # authorsArray = authors.split()
    # if not len(authorsArray):
    #     authors = authorsArray[0]
    # isbnArray = isbn.split()
    # if not len(isbnArray):
    #     isbn = isbnArray[0]
    # publisherArray = publisher.split()
    # if not len(publisherArray):
    #     publisher = publisherArray[0]
    # publicationyrArray = publicationyr.split()
    # if not len(publicationyrArray):
    #     publicationyr = publicationyrArray[0]
    # String manipulation to get the first word only if key in multiple word #
    # SELECT_END = "SELECT * FROM Books WHERE Title LIKE 
    SELECT_START = "SELECT * FROM Books WHERE Title LIKE '%s '"
    SELECT_WHOLE = "SELECT * FROM Books WHERE Title LIKE '" + title + "'"
    #print (SELECT_WHOLE)
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    searchAll = "SELECT DISTINCT * FROM Books WHERE Title LIKE '" + title + "' OR Author1 LIKE '" + authors + "' OR Author2 LIKE '" + authors + "' OR Author3 LIKE '" + authors + "' OR Publisher LIKE '" + publisher + "' OR PublicationYr LIKE '" + publicationyr + "' OR isbn LIKE '" + isbn + "'"
    mycursor.execute(searchAll)
    result = mycursor.fetchall()
    return result

#print(BookSearch("","George Orwell","","",""))



# todayDate = datetime.date.today()
    # #todayDate = datetime.strptime(todayDate, '%Y-%m-%d')
    # libraryDB = mysql.connector.connect(host = "localhost",database = 'LIB_ALS',
    # user = "root",
    # password = "Jokt8989")
    # mycursor = libraryDB.cursor()
    # #onLoanBooks = DisplayloanBooks()
    # returnDate = datetime.today().strftime('%Y-%m-%d')
    # select_query = "SELECT borrowID, borrowNum,borrowedDate FROM BorrowReturn WHERE returnDate IS NULL"
    # mycursor.execute(select_query)
    # loanList = mycursor.fetchall()
    # totalDays = 0
    # for i in loanList:
    #     #diff = todayDate - datetime.strptime(i[2], '%Y-%m-%d')
    #     #totalDays += diff
    #     pass
    # return type(todayDate)
#Book Acquisitions

def acquireBook(newAcc, newTitle, newAuthor1, newAuthor2, newAuthor3, newIsbn, newPublisher, newPublicationYr):
    #allfields = (newAcc, newTitle, newAuthor1, newAuthor2, newAuthor3, newIsbn, newPublisher, newPublicationYr)
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    allBooks_query = "SELECT * FROM Books"
    mycursor.execute(allBooks_query)
    allBooks = mycursor.fetchall()
    for books in allBooks:
        if newAcc in books or newTitle in books or newAuthor1 in books or newAuthor2 in books or newAuthor3 in books or newIsbn in books or newPublisher in books or newPublicationYr in books:
            acquireBookError_Fine()
            return "Prompt Error"
    insert_query  = ("INSERT INTO Books " 
                 "(accNum, title, Author1, Author2, Author3, isbn, publisher, PublicationYr) " 
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    new_book = (newAcc, newTitle, newAuthor1, newAuthor2, newAuthor3, newIsbn, newPublisher, newPublicationYr)
    mycursor.execute(insert_query, new_book)
    libraryDB.commit()



#Display Books on reservation
def reservedBooks():  #accNum, title, id, Name
    #left_join_query = "SELECT m.Name, r.resID, r.resNum FROM Reserve r LEFT JOIN Members m on r.resID = m.ID"
    join_query = "SELECT r.resNum, b.Title, r.resID, m.Name FROM Reserve r LEFT JOIN Members m on r.resID = m.ID LEFT JOIN Books b on r.resNum = b.accNum"
    mycursor.execute(join_query)
    reservation = mycursor.fetchall()
    return reservation
#print(reservedBooks())

#Membership Deletion
def MembershipDeletion(del_ID):
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    finedList = FinedMembers()
    loanList = membersLoanBooks(del_ID)
    reserveList = reservedBooks()
    for i in finedList:
        if del_ID in i:
            failedDeleteFine()
    for i in loanList:
        if del_ID in i:
            failedDeleteLoans()
    for i in reservedBooks():
        if del_ID in i:
            failedDeleteReservations()
    delete_query = "DELETE FROM Members WHERE id = %s"
    mycursor.execute(delete_query, (del_ID,))
    libraryDB.commit()


#MembershipDeletion("A301C")

#Create reservation
def CreateReservation(newNum, newID, newDate):
    membersFined_Query = "SELECT * FROM Fine WHERE fineID = %s"    #accNum, Name, Fac, phoneNo, email
    membersReservation_Query = "SELECT * FROM Reserve WHERE resID = %s"  #accNum, name, fac, phoneNo, email
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    mycursor.execute(membersFined_Query,(newID,))
    membersFined = mycursor.fetchall()
    mycursor.execute(membersReservation_Query, (newID,))
    membersReservation = mycursor.fetchall()
    #if member has fine
    if len(membersReservation) > 2:
        return "ERROR"
    #if already 2 reservations
    if len(membersFined) > 0:
        return "ERROR"
    #otherwise Update the Reserve Table
    insert_query  = ("INSERT INTO Reserve " 
                 "(resID, resNum, resDate) " 
                 "VALUES (%s, %s, %s)")
    data = (newNum, newID, newDate)
    mycursor.execute(insert_query,data)
    libraryDB.commit()

    
#CreateReservation("A401D", "A40",date.today())

#Cancel Reservation

# def cancelReservation(memberID,acc, cancelDate):
#     allLoanBook = DisplayloanBooks()
#     allResBook = reservedBooks()
#     loaned = False
#     reserved = False
#     for i in allLoanBook:
#         if i[0] == acc:
#             loaned = True
#     for i in allResBook:
#          if i[0] == acc and i[2] == memberID:
#              reserved = True
#     if loaned == False and reserved == False:
#         print('error')
#     else:
#         print("can delete")
        
        
        
#print(cancelReservation())





def withdrawBook(bookNum):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root", password="Jokt8989", database="LIB_ALS")
    mycursor = mydb.cursor()
    rBooks = reservedBooks()
    lBooks  = DisplayloanBooks()
    mycursor.execute("SELECT accNum FROM Books")
    allAccNum = mycursor.fetchall()
    exist = False
    for i in lBooks: #check if books on loan
        if bookNum in i:
            failPopupWithdrawBook_bookReserved()
            #return False #  "We need to prompt "Error! Book is currently on Loan"
    #Otherwise, we proceed to withdraw book
    for i in allAccNum:
        if bookNum in i:
            exist = True
    if exist == False:
        failPopupWithdrawBook_noBook()
        #return False #Prompt book dont exist
    successPopupWithdrawBook()

        
    #Step 1: Remove from Reservation first
    remove_query = "DELETE FROM Reserve WHERE Reserve.resNum = %s"
    mycursor.execute(remove_query, (bookNum,))
    mydb.commit()
    
#withdrawBook("A04")
#print(reservedBooks())
#print(DisplayloanBooks())
#print(withdrawBook("A50"))
    

#Fine Payment
# def finePayment(memberID, paymentDate, paymentAmt):
#     #If memberID not in FinedMembers(): ... Error Prompt
#     libraryDB = mysql.connector.connect(
#     host = "localhost",
#     database = 'LIB_ALS',
#     user = "root",
#     password = "Jokt8989")
#     mycursor = libraryDB.cursor()
#     update_settlePayment  = ("INSERT INTO SettlePayment" 
#                  "(payID, payAmt, payDate) " 
#                  "VALUES (%s, %s, %s)")
#     finePaid = (memberID, paymentAmt, paymentDate)
#     mycursor.execute(update_settlePayment, finePaid)
#     update_fine = "DELETE FROM Fine WHERE fineID = %s"
#     mycursor.execute(update_fine, (memberID,))
#     libraryDB.commit()

#Fine Payment
# def finePayment(memberID, paymentDate, paymentAmt):   
#     libraryDB = mysql.connector.connect(
#     host = "localhost",
#     database = 'LIB_ALS',
#     user = "root",
#     password = "Zymysql@1")
#     mycursor = libraryDB.cursor()
#     if memberID not in list(map(lambda x:x[0], FinedMembers())):
#         print("no fine") #promt error: member has no fine
#         paymentFailednofine()
#     #If memberID not in FinedMembers(): ... Error Prompt 
#     #check if paymentAmt == fineAmt correct
#     fine_amount_query = "SELECT * FROM Fine WHERE fineID = %s"
#     mycursor.execute(fine_amount_query, (memberID, ))
#     fineAmt = mycursor.fetchall()[0][1]
#     elif float(paymentAmt) != fineAmt:
#         print("wrong amt") #promt error:amount
#         paymentFailedAmt()
#     else:
#         paymentTry(memberID, paymentDate, paymentAmt)
        #popup confirmation
#finePayment("A101A", "2022-03-09", 4.00)
    
    


#Display the books on loan given membership id


#Reservation Cancellation
# def cancelReservation(memberID, acc, date):
#     #check if memberID and acc is in the same row of bookreservation, and
#     checker = (memberID, acc)
#     mydb = mysql.connector.connect(host="127.0.0.1",user="root",
#                             password="lozhihao", database="LIB_ALS")
#     new_deletionID = (acc.get(),)
#     input_query =  ("""
#     DELETE FROM Reserve
#     VWHERE accNum = %s;
#     """ )
#     if acc.get() in map(lambda x :x[0], DisplayloanBooks()) and checker in map(lambda x: (x[0],x[2]), reservedBooks()):
#         mycursor.execute(input_query, new_deletionID)
#         mydb.commit()
#         mydb.close()
    
#     else:
#         failedReservationCancellation() #popup fail
#         pass

        

'''
# navigating between frames 
def change_frame(oldframe, newframe):
    oldframe.forget()
    newframe.pack(fill="both", expand=1)

def popup(frame):
    frame = Toplevel(trial)
    frame.mainloop()

def successPopup():
        frame = Toplevel(trial)
        frame.configure(bg="lightgreen")
        title = Label(frame, text="Success", padx=20, pady=20)
        title.pack()
        contents = Label(frame, text="ALS Membership created", padx=10, pady=10)
        contents.pack()
        button = Button(frame, text="Back to Create Function", command=frame.destroy)
        button.pack()
        frame.mainloop()


# Opening TKinter

trial = Tk()
trial.title("Library-ALS")

# main

main = Frame(trial)
main.configure(bg="yellow")

title = Label(main, text=" ALS System: Please Select One to Proceed ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)   

membership = Button(main, text="Membership", width=50, pady=40, bg="lightblue", relief=RAISED, 
        command=lambda: change_frame(main, membership))
books = Button(main, text="Books", width=50, pady=40, bg="lightblue", relief=RAISED, 
        command=lambda: change_frame(main, books))
loans = Button(main, text="Loans", width=50, pady=40, bg="lightblue", relief=RAISED,
        command=lambda: change_frame(main, loans))
reservations = Button(main, text="Reservations", width=50, pady=40, bg="lightblue", relief=RAISED,
        command=lambda: change_frame(main, reservation))
fines = Button(main, text="Fines", width=50, pady=40, bg="lightblue", relief=RAISED,
        command=lambda: change_frame(main, fines))
reports = Button(main, text="Reports", width=50, pady=40, bg="lightblue", relief=RAISED,
        command=lambda: change_frame(main, report))

membership.grid(row=0, column=0, columnspan=1)
books.grid(row=0, column=1, columnspan=1)
loans.grid(row=0, column=2, columnspan=1)
title.grid(row=1, column=0, columnspan=3)
reservations.grid(row=2, column=0, columnspan=1)
fines.grid(row=2, column=1, columnspan=1)
reports.grid(row=2, column=2, columnspan=1)

main.pack(fill="both", expand=1)


#Membership

membership = Frame(trial)
membership.configure(bg="yellow")

title = Label(membership, text=" Membership ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)
selectOptions = Label(membership, text=" Select one of the Options below: ", width=150,
              pady=20, bg="lightblue", relief=RIDGE)
create = Label(membership, text=" 1.Create ", width=35, pady=30, bg="cornflowerblue",
               relief=GROOVE)
deletion = Label(membership, text=" 2.Deletion ", width=35, pady=30, bg="dodgerblue",
               relief=GROOVE)
update = Label(membership, text=" 3.Update ", width=35, pady=30, bg="deepskyblue",
               relief=GROOVE)
createtxt = Label(membership, text=" Membership Creation ", width=100, pady=30,
                 bg="black", fg="white",relief=GROOVE)
deletetxt = Label(membership, text=" Membership Deletion ", width=100, pady=30,
                 bg="black", fg="white",relief=GROOVE)
updatetxt = Label(membership, text=" Membership Update ", width=100, pady=30,
                 bg="black", fg="white",relief=GROOVE)

back = Button(membership, text=" Back to Main Menu ", width=150, pady=20,
              bg="lightblue", relief=RAISED, command=lambda: change_frame(membership, main))
create = Button(membership, text=" 1.Create ", width=50, pady=30, bg="cornflowerblue",
               relief=RAISED, command=lambda: change_frame(membership, create))
deletion = Button(membership, text=" 2.Deletion ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(membership, delete))
update = Button(membership, text=" 3.Update ", width=50, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(membership, update))

title.grid(row=0,column=0,columnspan=3)
selectOptions.grid(row=1,column=0, columnspan=3)
create.grid(row=2,column=0,columnspan=1)
createtxt.grid(row=2, column=1, columnspan=2)
deletetxt.grid(row=3, column=1, columnspan=2)
updatetxt.grid(row=4, column=1, columnspan=2)
deletion.grid(row=3,column=0,columnspan=1)
update.grid(row=4,column=0,columnspan=1)
back.grid(row=5, column=0, columnspan=3)

# Create Membership

create = Frame(trial)
create.configure(bg="yellow")

title = Label(create, text=" Please Enter Requested Information Below ", width=150, pady=20, 
  bg="lightgreen" ,relief=RIDGE)

IDtxt = Label(create, text="Membership ID",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
nametxt = Label(create, text="Name",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
facultytxt = Label(create, text="Faculty",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
phoneNotxt = Label(create, text="Phone Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
emailtxt = Label(create, text="Email Address",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

ID = Entry(create, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Membership ID")"""
name = Entry(create, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Name")"""
faculty = Entry(create, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Faculty")"""
phoneNo = Entry(create, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Phone Number")"""
email =  Entry(create, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Email Address")"""

createnew = Button(create, text=" Create Member ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=successPopup)
back = Button(create, text=" Back To Membership Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(create, membership))

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)
nametxt.grid(row=2,column=0,columnspan=1)
facultytxt.grid(row=3,column=0,columnspan=1)
phoneNotxt.grid(row=4,column=0,columnspan=1)
emailtxt.grid(row=5,column=0,columnspan=1)

ID.grid(row=1,column=1)
name.grid(row=2,column=1)
faculty.grid(row=3,column=1)
phoneNo.grid(row=4,column=1)
email.grid(row=5,column=1)

createnew.grid(row=6,column=0)
back.grid(row=6,column=1)

# Delete Membership


delete = Frame(trial)
delete.configure(bg="yellow")

title = Label(delete, text=" To Delete Member, Please Enter Membership ID ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(delete, text="Membership ID",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

deletenew = Button(delete, text=" Delete Member ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: successPopup)
back = Button(delete, text=" Back To Membership Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(delete, membership))

ID = Entry(delete, width=100, bg="cornflowerblue", justify="center")

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)

ID.grid(row=1,column=1)

deletenew.grid(row=2,column=0)
back.grid(row=2,column=1)


# Update membership 1

update = Frame(trial)
update.configure(bg="yellow")

title = Label(update, text=" To Update Member, Please Enter Membership ID ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(update, text="Membership ID",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

updatenew = Button(update, text=" Update Member ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(update, update2))
back = Button(update, text=" Back To Membership Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(update, membership))

ID = Entry(update, width=100, bg="cornflowerblue", justify="center")

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)

ID.grid(row=1,column=1)

updatenew.grid(row=2,column=0)
back.grid(row=2,column=1)

# Update membership 2

update2 = Frame(trial)
update2.configure(bg="yellow")

title = Label(update2, text=" Please Enter Requested Information Below ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(update2, text="Membership ID",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
nametxt = Label(update2, text="Name",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
facultytxt = Label(update2, text="Faculty",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
phoneNotxt = Label(update2, text="Phone Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
emailtxt = Label(update2, text="Email Address",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

ID = Entry(update2, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Membership ID")"""
name = Entry(update2, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Name")"""
faculty = Entry(update2, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Faculty")"""
phoneNo = Entry(update2, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Phone Number")"""
email =  Entry(update2, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Email Address")"""

update2new = Button(update2, text=" Update Member ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=successPopup)
back = Button(update2, text=" Back To Membership Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(update2, update))

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)
nametxt.grid(row=2,column=0,columnspan=1)
facultytxt.grid(row=3,column=0,columnspan=1)
phoneNotxt.grid(row=4,column=0,columnspan=1)
emailtxt.grid(row=5,column=0,columnspan=1)

ID.grid(row=1,column=1)
name.grid(row=2,column=1)
faculty.grid(row=3,column=1)
phoneNo.grid(row=4,column=1)
email.grid(row=5,column=1)

update2new.grid(row=6,column=0)
back.grid(row=6,column=1)

# Books

books = Frame(trial)
books.configure(bg="yellow")

title = Label(books, text=" Books ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)
selectOptions = Label(books, text=" Select one of the Options below: ", width=150,
              pady=20, bg="lightblue", relief=RIDGE)

acquisitiontxt = Label(books, text=" Book Acquisition ", width=100, pady=30, bg="cornflowerblue",
               relief=GROOVE)
withdrawaltxt = Label(books, text=" Book Withdrawal ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)

back = Button(books, text=" Back to Main Menu ", width=150, pady=20,
              bg="lightblue", relief=RAISED, command=lambda: change_frame(books, main))
acquisition = Button(books, text=" 1.Acquisition ", width=50, pady=30, bg="cornflowerblue",
               relief=RAISED, command=lambda: change_frame(books, acquisition))
withdrawal = Button(books, text=" 2.Deletion ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(books, withdrawal))


title.grid(row=0,column=0,columnspan=3)
selectOptions.grid(row=1,column=0, columnspan=3)
acquisition.grid(row=2,column=0,columnspan=1)
acquisitiontxt.grid(row=2, column=1, columnspan=2)
withdrawaltxt.grid(row=3, column=1, columnspan=2)
withdrawal.grid(row=3,column=0,columnspan=1)
back.grid(row=4, column=0, columnspan=3)

# book acquisition

acquisition = Frame(trial)
acquisition.configure(bg="yellow")

title = Label(acquisition, text=" For New Book Acquisition, Please Enter Requested Information Below ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

accNumtxt = Label(acquisition, text="Accession Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
booktitletxt = Label(acquisition, text="Title",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
authortxt = Label(acquisition, text="Authors",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
ISBNtxt = Label(acquisition, text="ISBN",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
publishertxt = Label(acquisition, text="Publisher",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
publishYeartxt = Label(acquisition, text="Publish Year",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

accNum = Entry(acquisition, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Membership ID")"""
booktitle = Entry(acquisition, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Name")"""
author = Entry(acquisition, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Faculty")"""
ISBN = Entry(acquisition, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Phone Number")"""
publisher =  Entry(acquisition, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Email Address")"""
publishYear =  Entry(acquisition, width=100, bg="cornflowerblue", justify="center")

createnew = Button(acquisition, text=" Add New Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=successPopup)
back = Button(acquisition, text=" Back To Book Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(acquisition, books))

title.grid(row=0,column=0,columnspan=3)

accNumtxt.grid(row=1,column=0,columnspan=1)
booktitletxt.grid(row=2,column=0,columnspan=1)
authortxt.grid(row=3,column=0,columnspan=1)
ISBNtxt.grid(row=4,column=0,columnspan=1)
publishertxt.grid(row=5,column=0,columnspan=1)
publishYeartxt.grid(row=6,column=0,columnspan=1)

accNum.grid(row=1,column=1)
booktitle.grid(row=2,column=1)
author.grid(row=3,column=1)
ISBN.grid(row=4,column=1)
publisher.grid(row=5,column=1)
publishYear.grid(row=6,column=1)

createnew.grid(row=7,column=0)
back.grid(row=7,column=1)

# Book withdrawal

withdrawal = Frame(trial)
withdrawal.configure(bg="yellow")

title = Label(withdrawal, text=" To Remove Outdated Books From System, Please Enter Required Information Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(withdrawal, text="Accession Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

deletenew = Button(withdrawal, text=" Withdraw Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=successPopup)
back = Button(withdrawal, text=" Back To Books Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(withdrawal, books))

ID = Entry(withdrawal, width=100, bg="cornflowerblue", justify="center")

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)

ID.grid(row=1,column=1)

deletenew.grid(row=2,column=0)
back.grid(row=2,column=1)

# Loans

loans = Frame(trial)
loans.configure(bg="yellow")

title = Label(loans, text=" Loans ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)
selectOptions = Label(loans, text=" Select one of the Options below: ", width=150,
              pady=20, bg="lightblue", relief=RIDGE)

acquisitiontxt = Label(loans, text=" Book Borrowing ", width=100, pady=30, bg="cornflowerblue",
               relief=GROOVE)
withdrawaltxt = Label(loans, text=" Book Returning ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)

back = Button(loans, text=" Back to Main Menu ", width=150, pady=20,
              bg="lightblue", relief=RAISED, command=lambda: change_frame(loans, main))
acquisition = Button(loans, text=" 1.Borrow ", width=50, pady=30, bg="cornflowerblue",
               relief=RAISED, command=lambda: change_frame(loans, borrow))
withdrawal = Button(loans, text=" 2.Return ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(loans, bookReturn))


title.grid(row=0,column=0,columnspan=3)
selectOptions.grid(row=1,column=0, columnspan=3)
acquisition.grid(row=2,column=0,columnspan=1)
acquisitiontxt.grid(row=2, column=1, columnspan=2)
withdrawaltxt.grid(row=3, column=1, columnspan=2)
withdrawal.grid(row=3,column=0,columnspan=1)
back.grid(row=4, column=0, columnspan=3)

# loan borrowing

borrow = Frame(trial)
borrow.configure(bg="yellow")

title = Label(borrow, text=" To Borrow a Book, Please Enter Required Information Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(borrow, text="Accession Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
memberIDtxt = Label(borrow, text="MembershipID ",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

deletenew = Button(borrow, text=" Borrow Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=successPopup)
back = Button(borrow, text=" Back To Loans Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(borrow, loans))

ID = Entry(borrow, width=100, bg="cornflowerblue", justify="center")
memberID = Entry(borrow, width=100, bg="cornflowerblue", justify="center")

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)
memberIDtxt.grid(row=2,column=0,columnspan=1)

ID.grid(row=1,column=1)
memberID.grid(row=2,column=1)

deletenew.grid(row=3,column=0)
back.grid(row=3,column=1)

# loan returning 

bookReturn = Frame(trial)
bookReturn.configure(bg="yellow")

title = Label(bookReturn, text=" To Return a Book, Please Enter Required Information Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(bookReturn, text="Accession Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
datetxt = Label(bookReturn, text="Return Date",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

deletenew = Button(bookReturn, text=" Return Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=successPopup)
back = Button(bookReturn, text=" Back To Loans Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(bookReturn, loans))

ID = Entry(bookReturn, width=100, bg="cornflowerblue", justify="center")
date = Entry(bookReturn, width=100, bg="cornflowerblue", justify="center")

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)
datetxt.grid(row=2,column=0,columnspan=1)

ID.grid(row=1,column=1)
date.grid(row=2,column=1)

deletenew.grid(row=3,column=0)
back.grid(row=3,column=1)


# reservation

reservation = Frame(trial)
reservation.configure(bg="yellow")

title = Label(reservation, text=" Reservation ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)
selectOptions = Label(reservation, text=" Select one of the Options below: ", width=150,
              pady=20, bg="lightblue", relief=RIDGE)

acquisitiontxt = Label(reservation, text=" Reserve a Book ", width=100, pady=30, bg="cornflowerblue",
               relief=GROOVE)
withdrawaltxt = Label(reservation, text=" Cancel Reservation ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)

back = Button(reservation, text=" Back to Main Menu ", width=150, pady=20,
              bg="lightblue", relief=RAISED, command=lambda: change_frame(reservation, main))
acquisition = Button(reservation, text=" 1.Reserve a Book ", width=50, pady=30, bg="cornflowerblue",
               relief=RAISED, command=lambda: change_frame(reservation, reserve))
withdrawal = Button(reservation, text=" 2.Cancel Reservation ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(reservation, cancel))


title.grid(row=0,column=0,columnspan=3)
selectOptions.grid(row=1,column=0, columnspan=3)
acquisition.grid(row=2,column=0,columnspan=1)
acquisitiontxt.grid(row=2, column=1, columnspan=2)
withdrawaltxt.grid(row=3, column=1, columnspan=2)
withdrawal.grid(row=3,column=0,columnspan=1)
back.grid(row=4, column=0, columnspan=3)

# make a reservation

reserve = Frame(trial)
reserve.configure(bg="yellow")

title = Label(reserve, text=" To Reserve a Book, Please Enter Required Information Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(reserve, text="Accession Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
memberIDtxt = Label(reserve, text="MembershipID ",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
datetxt = Label(reserve, text="Reserve Date ",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

deletenew = Button(reserve, text=" Reserve Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=successPopup)
back = Button(reserve, text=" Back To Reservation Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(reserve, reservation))

ID = Entry(reserve, width=100, bg="cornflowerblue", justify="center")
memberID = Entry(reserve, width=100, bg="cornflowerblue", justify="center")
date = Entry(reserve, width=100, bg="cornflowerblue", justify="center")

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)
memberIDtxt.grid(row=2,column=0,columnspan=1)
datetxt.grid(row=3,column=0,columnspan=1)

ID.grid(row=1,column=1)
memberID.grid(row=2,column=1)
date.grid(row=3,column=1)

deletenew.grid(row=4,column=0)
back.grid(row=4,column=1)

# cancel a reservation

cancel = Frame(trial)
cancel.configure(bg="yellow")

title = Label(cancel, text=" To Cancel a Reservation, Please Enter Required Information Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(cancel, text="Accession Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
memberIDtxt = Label(cancel, text="MembershipID ",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
datetxt = Label(cancel, text="Cancel Date ",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

deletenew = Button(cancel, text=" Cancel Reservation ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=successPopup)
back = Button(cancel, text=" Back To Reservation Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(cancel, reservation))

ID = Entry(cancel, width=100, bg="cornflowerblue", justify="center")
memberID = Entry(cancel, width=100, bg="cornflowerblue", justify="center")
date = Entry(cancel, width=100, bg="cornflowerblue", justify="center")

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)
memberIDtxt.grid(row=2,column=0,columnspan=1)
datetxt.grid(row=3,column=0,columnspan=1)

ID.grid(row=1,column=1)
memberID.grid(row=2,column=1)
date.grid(row=3,column=1)

deletenew.grid(row=4,column=0)
back.grid(row=4,column=1)

# fines

fines = Frame(trial)
fines.configure(bg="yellow")

title = Label(fines, text=" Fines ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)
selectOptions = Label(fines, text=" Select one of the Options below: ", width=150,
              pady=20, bg="lightblue", relief=RIDGE)

acquisitiontxt = Label(fines, text=" Payment ", width=100, pady=30, bg="cornflowerblue",
               relief=GROOVE)

back = Button(fines, text=" Back to Main Menu ", width=150, pady=20,
              bg="lightblue", relief=RAISED, command=lambda: change_frame(fines, main))
acquisition = Button(fines, text=" 1.Fine Payment ", width=50, pady=30, bg="cornflowerblue",
               relief=RAISED, command=lambda: change_frame(fines, payment))


title.grid(row=0,column=0,columnspan=3)
selectOptions.grid(row=1,column=0, columnspan=3)
acquisition.grid(row=2,column=0,columnspan=1)
acquisitiontxt.grid(row=2, column=1, columnspan=2)
back.grid(row=4, column=0, columnspan=3)

# Payment

payment = Frame(trial)
payment.configure(bg="yellow")

title = Label(payment, text=" To Pay a Fine, Please Enter Required Information Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

amounttxt = Label(payment, text="Payment Amount ",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
memberIDtxt = Label(payment, text="MembershipID ",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
datetxt = Label(payment, text="Payment Date",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

deletenew = Button(payment, text=" Pay Fine ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=successPopup)
back = Button(payment, text=" Back To Fines Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(payment, fines))

amount = Entry(payment, width=100, bg="cornflowerblue", justify="center")
memberID = Entry(payment, width=100, bg="cornflowerblue", justify="center")
date = Entry(payment, width=100, bg="cornflowerblue", justify="center")

title.grid(row=0,column=0,columnspan=3)

amounttxt.grid(row=1,column=0,columnspan=1)
memberIDtxt.grid(row=2,column=0,columnspan=1)
datetxt.grid(row=3,column=0,columnspan=1)

amount.grid(row=1,column=1)
memberID.grid(row=2,column=1)
date.grid(row=3,column=1)

deletenew.grid(row=4,column=0)
back.grid(row=4,column=1)

# Reports

report = Frame(trial)
report.configure(bg="yellow")

title = Label(report, text=" Reports ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)
selectOptions = Label(report, text=" Select one of the Options below: ", width=150,
              pady=20, bg="lightblue", relief=RIDGE)

booksearchtxt = Label(report, text=" Book Search ", width=100, pady=30, bg="cornflowerblue",
               relief=GROOVE)
bookonloantxt = Label(report, text=" Book On Loan ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)
bookonreservationtxt = Label(report, text=" Book On Reservation ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)
outstandingfinestxt = Label(report, text=" Outstanding Fines ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)
bookonloantomemberstxt = Label(report, text=" Book On Loan To Members ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)

back = Button(report, text=" Back to Main Menu ", width=150, pady=20,
              bg="lightblue", relief=RAISED, command=lambda: change_frame(report, main))

booksearch = Button(report, text=" 1.Book Search ", width=50, pady=30, bg="cornflowerblue",
               relief=RAISED, command=lambda: change_frame(report, search))
bookonloan = Button(report, text=" 2.Book On Loan ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(report, search))
bookonreservation = Button(report, text=" 3.Book On Reservation ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(report, search))
outstandingfines = Button(report, text=" 4.Outstanding Fines ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(report, search))
bookonloantomembers = Button(report, text=" 5.Book On Loan To Members ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(report, search))

title.grid(row=0,column=0,columnspan=3)
selectOptions.grid(row=1,column=0, columnspan=3)

booksearch.grid(row=2,column=0,columnspan=1)
booksearchtxt.grid(row=2, column=1, columnspan=2)

bookonloantxt.grid(row=3, column=1, columnspan=2)
bookonloan.grid(row=3, column=0, columnspan=1)

bookonreservation.grid(row=4, column=0, columnspan=1)
bookonreservationtxt.grid(row=4, column=1, columnspan=2)

outstandingfines.grid(row=5, column=0, columnspan=1)
outstandingfinestxt.grid(row=5, column=1, columnspan=2)

bookonloantomembers.grid(row=6, column=0, columnspan=1)
bookonloantomemberstxt.grid(row=6, column=1, columnspan=2)

back.grid(row=7, column=0, columnspan=3)

# Search Reports

search = Frame(trial)
search.configure(bg="yellow")

title = Label(search, text=" Search Based on One of the Categories Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

booktitletxt = Label(search, text="Title",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
authortxt = Label(search, text="Authors",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
ISBNtxt = Label(search, text="ISBN",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
publishertxt = Label(search, text="Publisher",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
publishYeartxt = Label(search, text="Publish Year",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

booktitle = Entry(search, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Name")"""
author = Entry(search, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Faculty")"""
ISBN = Entry(search, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Phone Number")"""
publisher =  Entry(search, width=100, bg="cornflowerblue", justify="center")
""".insert(0, "Enter your Email Address")"""
publishYear =  Entry(search, width=100, bg="cornflowerblue", justify="center")

createnew = Button(search, text=" Search Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED)
back = Button(search, text=" Back To Reports Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED)

title.grid(row=0,column=0,columnspan=3)

booktitletxt.grid(row=1,column=0,columnspan=1)
authortxt.grid(row=2,column=0,columnspan=1)
ISBNtxt.grid(row=3,column=0,columnspan=1)
publishertxt.grid(row=4,column=0,columnspan=1)
publishYeartxt.grid(row=5,column=0,columnspan=1)

booktitle.grid(row=1,column=1)
author.grid(row=2,column=1)
ISBN.grid(row=3,column=1)
publisher.grid(row=4,column=1)
publishYear.grid(row=5,column=1)

createnew.grid(row=6,column=0)
back.grid(row=6,column=1)

# Closing Tkinter

trial.mainloop()

'''

