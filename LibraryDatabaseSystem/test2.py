from logging import root
from tkinter import *
from tkinter import ttk
from ctypes import LibraryLoader
from matplotlib.style import library
from numpy import roots
from sqlalchemy import create_engine
from datetime import date, datetime, timedelta
import mysql.connector
import csv
from functions import *

#Jason DB
# mydb = mysql.connector.connect(host="127.0.0.1",user="root",
#                                password="lozhihao", database="LIB_ALS")
#Jacky DB
mydb = mysql.connector.connect(host="127.0.0.1",user="root",
                               password="Jokt8989", database="LIB_ALS")

# print(mydb)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM members")
databases = mycursor.fetchall()
#print(databases)

mydb.commit()
mycursor.close()
mydb.close()


################### FUNCTIONS ##################################

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
    if len(borrowQuery) >= 2:
        borrowError_loanQuota()
    for i in borrowQuery:
        if borrowNum in i:
            borrowError_BookOnLoan(borrowNum)
    for i in fineQuery:
        if memberID in i:
           borrowError_Fine() #Prompt - "Error! Member has outstanding fines."
        #return False #Prompt - "Error! Member Loan quota exceeded"
            #return  False #Prompt Error
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
    #return borrowReturn


# navigating between frames 
def change_frame(oldframe, newframe):
    oldframe.forget()
    newframe.pack(fill="both", expand=1)

# navigating between frames 
def change_frame_destroy_old(oldframe, newframe):
    clearFrame(oldframe)
    newframe.pack(fill="both", expand=1)

def clearFrame(frame):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
       widget.destroy()
    
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    frame.forget()

# navigating between frames 
def change_frame_and_show_loanbooks_data(oldframe, newframe):
    oldframe.forget()
    newframe.pack(fill="both", expand=1)
    title = "Loaned Books"
    data = DisplayloanBooks()
    #print (data)
    headers = ('Accession Number', 'Title', 'Author1', 'Author2', 'Author3', 'isbn', 'Publisher', 'PublicationYr')
    newframe.pack(fill="both", expand=True)
    myTree = ttk.Treeview(newframe)
    myTree.pack(fill="both", expand=True)
    myTree['columns'] = headers

    # Setting the scroll
    scroll = ttk.Scrollbar(newframe, orient="vertical", command=myTree.yview)
    scroll.pack(side = 'right', fill = 'y')
    myTree.configure(yscrollcommand=scroll.set)

    # COLUMNS
    myTree.column("#0", width=0, stretch=NO)
    myTree.heading("#0",text="",anchor=CENTER)
    for i in headers:
        myTree.column(i, anchor=CENTER, stretch=NO)
        myTree.heading(i, text=i, anchor=CENTER)
    iidCount = 0
    for i in data:
        myTree.insert(parent='', index='end', iid=iidCount, text='', values=i)
        iidCount = iidCount + 1
    button = Button(newframe, text="Back to Reports", command=lambda: change_frame_destroy_old(newframe, report))
    button.pack()
    newframe.mainloop()

def change_frame_and_show_reservebooks_data(oldframe, newframe):
    oldframe.forget()
    newframe.pack(fill="both", expand=1)
    title = "Reserved Books"
    data = DisplayReserveBooks()
    #print (data)
    headers = ('Accession Number', 'Title', 'Membership ID', 'Name')
    newframe.pack(fill="both", expand=True)
    myTree = ttk.Treeview(newframe)
    myTree.pack(fill="both", expand=True)
    myTree['columns'] = headers

    # Setting the scroll
    scroll = ttk.Scrollbar(newframe, orient="vertical", command=myTree.yview)
    scroll.pack(side = 'right', fill = 'y')
    myTree.configure(yscrollcommand=scroll.set)

    # COLUMNS
    myTree.column("#0", width=0,  stretch=NO)
    myTree.heading("#0",text="",anchor=CENTER)
    for i in headers:
        myTree.column(i, anchor=CENTER, stretch=NO)
        myTree.heading(i, text=i, anchor=CENTER)
    iidCount = 0
    for i in data:
        myTree.insert(parent='', index='end', iid=iidCount, text='', values=i)
        iidCount = iidCount + 1
    # TODO: must fix this bro (i think its done?)
    button = Button(newframe, text="Back to Reports", command=lambda: change_frame_destroy_old(newframe, report))
    button.pack()
    newframe.mainloop()

def change_frame_and_show_members_with_outstanding_fines(oldframe, newframe):
    oldframe.forget()
    newframe.pack(fill="both", expand=1)
    title = "Members with Outstanding Fines"
    # [('A201B', 'Sherlock Holmes', 'Law', '44327676', 'elementarydrw@als.edu')]
    data = FinedMembers()
    headers = ('Accession Number', 'Name', 'Faculty', 'Phone Number', 'Email')
    newframe.pack(fill="both", expand=True)
    myTree = ttk.Treeview(newframe)
    myTree.pack(fill="both", expand=True)
    myTree['columns'] = headers

    # Setting the scroll
    scroll = ttk.Scrollbar(newframe, orient="vertical", command=myTree.yview)
    scroll.pack(side = 'right', fill = 'y')
    myTree.configure(yscrollcommand=scroll.set)
    # COLUMNS
    myTree.column("#0", width=0,  stretch=NO)
    myTree.heading("#0",text="",anchor=CENTER)
    for i in headers:
        myTree.column(i, anchor=CENTER, stretch=NO)
        myTree.heading(i, text=i, anchor=CENTER)
    iidCount = 0
    for i in data:
        myTree.insert(parent='', index='end', iid=iidCount, text='', values=i)
        iidCount = iidCount + 1
    button = Button(newframe, text="Back to Reports", command=lambda: change_frame_destroy_old(newframe, report))
    button.pack()
    newframe.mainloop()


def change_frame_and_show_book_search_output(oldframe, newframe, title, authors, isbn, publisher, publicationyr):
    oldframe.forget()
    newframe.pack(fill="both", expand=1)
    title = "Members with Outstanding Fines"
    # ('A01', 'A 1984 Story', 'George Orwell', None, None, '9790000000000', 'Intra S.r.l.s.', 2021)
    data = BookSearch(title, authors, isbn, publisher, publicationyr)
    headers = ('Accession Number', 'Title', 'Author1', 'Author2', 'Author3', 'ISBN', 'Publisher', 'Publisher Year')
    newframe.pack(fill="both", expand=True)
    myTree = ttk.Treeview(newframe)
    myTree.pack(fill="both", expand=True)
    myTree['columns'] = headers

    # Setting the scroll
    scroll = ttk.Scrollbar(newframe, orient="vertical", command=myTree.yview)
    scroll.pack(side = 'right', fill = 'y')
    myTree.configure(yscrollcommand=scroll.set)
    # COLUMNS
    myTree.column("#0", width=0,  stretch=NO)
    myTree.heading("#0",text="",anchor=CENTER)
    for i in headers:
        myTree.column(i, anchor=CENTER, stretch=NO)
        myTree.heading(i, text=i, anchor=CENTER)
    iidCount = 0
    for i in data:
        myTree.insert(parent='', index='end', iid=iidCount, text='', values=i)
        iidCount = iidCount + 1
    button = Button(newframe, text="Back to Reports", command=lambda: change_frame_destroy_old(newframe, report))
    button.pack()
    newframe.mainloop()

def change_frame_and_show_Book_On_Loan_To_Member(oldframe, newframe, sID):
    oldframe.forget()
    newframe.pack(fill="both", expand=1)
    title = "Books on Loan to Member"
    data = membersLoanBooks(sID)
    headers = ('Accession Number', 'Title', 'Author1', 'Author2', 'Author3', 'ISBN', 'Publisher', 'Publisher Year')
    newframe.pack(fill="both", expand=True)
    myTree = ttk.Treeview(newframe)
    myTree.pack(fill="both", expand=True)
    myTree['columns'] = headers

    # Setting the scroll
    scroll = ttk.Scrollbar(newframe, orient="vertical", command=myTree.yview)
    scroll.pack(side = 'right', fill = 'y')
    myTree.configure(yscrollcommand=scroll.set)
    # COLUMNS
    myTree.column("#0", width=0,  stretch=NO)
    myTree.heading("#0",text="",anchor=CENTER)
    for i in headers:
        myTree.column(i, anchor=CENTER, stretch=NO)
        myTree.heading(i, text=i, anchor=CENTER)
    iidCount = 0
    for i in data:
        myTree.insert(parent='', index='end', iid=iidCount, text='', values=i)
        iidCount = iidCount + 1
    button = Button(newframe, text="Back to Reports", command=lambda: change_frame_destroy_old(newframe, report))
    button.pack()
    newframe.mainloop()


# def delete_and_change_frame(oldframe, newframe, deleteID):
#     MembershipDeletion(deleteID)
#     change_frame_destroy_old(newframe, report)


def successPopupCreateMembership():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Success", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="ALS Membership created", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Create Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def returnBook_SuccessButHasFine():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Success", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Book returned successfully but has fine", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Create Function", command=frame.destroy)
    button.pack()
    frame.mainloop()    

def successPopupWithdrawBook():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Success", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Withdraw Book Success", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Create Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def failPopupWithdrawBook_noBook():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Fail", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Withdraw Book not exist", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Create Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def failPopupWithdrawBook_bookReserved():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Fail", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Withdraw Book is reserved ", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Create Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def successPopupBorrowBook():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Success", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Borrow Book Success", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Create Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def failedCreate():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failure", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Member already exist, missing fields", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Create Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def successPopupUpdateMembership():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Success", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="ALS Membership updated", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Update Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def successPopupDeletionMembership():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Success", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="ALS Membership deleted", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Update Function", command=frame.destroy)
    button.pack()
    frame.mainloop()       

def failedUpdate():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failure", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Missing or incomplete field", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Update Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def failedDeleteFine():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Error!", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Member still has outstanding Fine", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Delete Function", command=frame.destroy)
    button.pack()
    frame.mainloop()
    
def failedDeleteLoans():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Error!", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Member still has loans", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Delete Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def failedDeleteReservations():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Error!", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Member still has reservations", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Delete Function", command=frame.destroy)
    button.pack()
    frame.mainloop()


def updatePopUp(newID, newName, newFaculty, newPhoneNo, newEmail):
    frame = Toplevel()
    frame.configure(bg="lightgreen")

    title=Label(frame, text="Please confirm updated details to be correct")
    title.pack()

    memberID = Label(frame, text=newID.get())
    name = Label(frame, text=newName.get())
    faculty = Label(frame, text=newFaculty.get())
    phoneNo = Label(frame, text=newPhoneNo.get())
    email = Label(frame, text=newEmail.get())
    memberID.pack()
    name.pack()
    faculty.pack()
    phoneNo.pack()
    email.pack()

    backButton=Button(frame, text="Back to update function", command=frame.destroy)
    updateButton=Button(frame, text="update member", command=lambda: updateMembership(newID, newName, newFaculty, newPhoneNo, newEmail))

    backButton.pack()
    updateButton.pack()

    frame.mainloop()

def bookSuccessAcquisition():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Success", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="New Book added in Library", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Book Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def bookFailedAcquisition():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Book Already added, duplicated , missing or imcomplete field", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Book Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def bookFailedWithdrawal_Loan():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Book is currently on loan", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Book Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def bookFailedWithdrawal_Reserved():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Book is currently reserved", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Book Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def bookTryWithdrawal(newAcc):
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Please confirm details to be correct", padx=20, pady=20)
    title.pack()

    mydb = mysql.connector.connect(host="127.0.0.1",user="root",
        password="Jokt8989", database="LIB_ALS")
    mycursor = mydb.cursor()
    query = ("""SELECT *
                        FROM books
                        WHERE accNum = %s """)
    mycursor.execute(query, (newAcc.get(),))
    records = mycursor.fetchall()
    print(records)
    mydb.commit()
    mycursor.close()
    mydb.close()

    accNum = Label(frame, text=newAcc.get())
    title = Label(frame, text=records[0][1])
    author = Label(frame, text=(records[0][2] + str(records[0][3]) + str(records[0][4])))
    ISBN = Label(frame, text=records[0][5])
    publisher = Label(frame, text=records[0][6])
    publicationYr = Label(frame, text=records[0][7])

    accNum.pack()
    title.pack()
    author.pack()
    ISBN.pack()
    publisher.pack()
    publicationYr.pack()  
    
    backButton=Button(frame, text="Back to Withdraw function", command=frame.destroy)
    updateButton=Button(frame, text="Confirm withdrawal", command=lambda: withdrawBook(newAcc))

    backButton.pack()
    updateButton.pack()
    
    frame.mainloop()

def acquireBookError_Fine():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Cannot acquire Book", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to borrow Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def borrowError_Fine():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Member has outstanding fines.", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to borrow Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def borrowError_loanQuota():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Error! Member Loan quota exceeded", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to borrow Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def borrowError_BookOnLoan(borrowNum):
    # can change the 
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",
                               password="Jokt8989", database="LIB_ALS")
    mycursor = mydb.cursor()
    filter_query = "SELECT dueDate FROM borrowreturn WHERE borrowNum = %s;"
    mycursor.execute(filter_query, (borrowNum,))
    date = mycursor.fetchall()
    
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Error! Book currently on Loan until: " + date, padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to borrow Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def returnError_SuccessReturnWithFine():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Error! Returnbo successful but has fine", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to borrow Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def failedReservationBooks():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Error!", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Member currently has 2 Books on Reservation", padx=10, pady=10)
    contents.pack() #need to put fine value into X
    button = Button(frame, text="Back to Reserve Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def failedReservationFine():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Error!", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Member has Outstanding Fine of $X", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Reserve Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def failedReservation_noMember():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Error!", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="No such member", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Reserve Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def failedReservation_noBook():
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Error!", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="No such book", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Reserve Function", command=frame.destroy)
    button.pack()
    frame.mainloop()


def failedReservationCancellation():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Error!", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Member has no such reservation", padx=10, pady=10)
    contents.pack() #need to put fine value into X
    button = Button(frame, text="Back to Cancellation Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def paymentFailednofine():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Member has no fine", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Payment Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def paymentFailedAmt():
    frame = Toplevel(trial)
    frame.configure(bg="red")
    title = Label(frame, text="Failed", padx=20, pady=20)
    title.pack()
    contents = Label(frame, text="Incorrect fine payment amount", padx=10, pady=10)
    contents.pack()
    button = Button(frame, text="Back to Payment Function", command=frame.destroy)
    button.pack()
    frame.mainloop()

def paymentTry(memberID, paymentDate, paymentAmt):
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")
    title = Label(frame, text="Please confirm details to be correct", padx=20, pady=20)
    title.pack()

    mydb = mysql.connector.connect(host="127.0.0.1",user="root",
        password="Jokt8989", database="LIB_ALS")
    mycursor = mydb.cursor()
    update_fine = "DELETE FROM Fine WHERE fineID = %s"
    data = memberID.get()
    mycursor.execute(update_fine, (data,))
    
    update_settlePayment  = ("INSERT INTO SettlePayment" 
                     "(payID, payAmt, payDate) " 
                     "VALUES (%s, %s, %s)")
    finePaid = (memberID.get(), paymentAmt.get(), paymentDate.get())

    mycursor.execute(update_settlePayment, finePaid)
    mydb.commit()
    records = mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    mydb.close()

    memberIDlbl = Label(frame, text=memberID.get())
    paymentDatelbl = Label(frame, text=paymentDate.get())
    paymentAmtlbl = Label(frame, text=paymentAmt.get())


    memberIDlbl.pack()
    paymentDatelbl.pack()
    paymentAmtlbl.pack()
    
    backButton=Button(frame, text="Back to Payment function", command=frame.destroy)
    updateButton=Button(frame, text="Confirm Payment", command = frame.destroy)

    backButton.pack()
    updateButton.pack()
    
    frame.mainloop() 

def Book_On_Loan_To_Members(MemberID):
    lst_of_member = membersLoanBooks(memberID)
    frame = Toplevel(trial)
    frame.configure(bg="yellow")
    title = Label(frame, text="MEMBER WITH BOOK ON LOAN")
    title.pack()
    content = Label(frame, str(lst_of_member))
    content.pack()
    backButton = Button(frame, text="Back to function")
    backButton.pack()
    frame.mainloop()

# MYSQL failedReservationCancellationFunctions 
#########################################################################################################################
def createMembership(newID,newName,newFac, newPhone,newEmail):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",
                               password="Jokt8989", database="LIB_ALS")
    mycursor = mydb.cursor()
    filter_query = (""" SELECT * FROM members WHERE id = %s""")
    member_id = (newID.get(),)
    new_member = (newID.get(),newName.get(),newFac.get(), newPhone.get(),newEmail.get())
    print(new_member)
    mycursor.execute(filter_query, member_id)
    filter_result = mycursor.fetchall()
    # print(mydb)
    if filter_result != "" or ("" in (newID.get(),newName.get(),newFac.get(), newPhone.get(),newEmail.get())):
        failedCreate()
    else:
        input_query = ("""
    INSERT INTO Members(id, Name, Faculty, PhoneNo, Email)
    VALUES (%s, %s, %s, %s, %s);
    """ )
        mycursor.execute(input_query, new_member)
        mydb.commit()
        mydb.close()
        successPopupCreateMembership()

def FinedMembers():
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    fineID_query = "SELECT * FROM Members WHERE Members.id IN (SELECT fineID FROM Fine)"
    mycursor.execute(fineID_query)
    fineID = mycursor.fetchall()
    #fineID = list(map(lambda x: x.remove(','),fineID))
    return fineID

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

def reservedBooks():  #accNum, title, id, Name
    #left_join_query = "SELECT m.Name, r.resID, r.resNum FROM Reserve r LEFT JOIN Members m on r.resID = m.ID"
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    join_query = "SELECT r.resNum, b.Title, r.resID, m.Name FROM Reserve r LEFT JOIN Members m on r.resID = m.ID LEFT JOIN Books b on r.resNum = b.accNum"
    mycursor.execute(join_query)
    reservation = mycursor.fetchall()
    return reservation

def reservationPopUp(AccessionNum, ID, Date):
    frame = Toplevel(trial)
    frame.configure(bg="lightgreen")

    #print(AccessionNum.get(), ID, Date.get())

    title=Label(frame, text="Confirm Reservation Details To Be Correct")
    title.pack()

    mydb = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = mydb.cursor()

    bookTitle_query = "SELECT title FROM books WHERE accNum = %s"
    mycursor.execute(bookTitle_query, (AccessionNum,))
    bookTitle = mycursor.fetchall()
    print(bookTitle)
    #accessionNum = Label(frame, text=AccessionNum)
    #BookTitle = Label(frame, text=bookTitle[0][0])

    name_query = "SELECT Name FROM members WHERE id = %s"
    mycursor.execute(name_query, (ID,))
    Name = mycursor.fetchall()
    #print(Name)
    
    iD = Label(frame, text=ID)
    name = Label(frame, text=Name[0][0]) 
    date = Label(frame, text=Date)
    accessionNum = Label(frame, text=AccessionNum)
    BookTitle = Label(frame, text=bookTitle[0][0]) 
    accessionNum.pack()
    BookTitle.pack()
    iD.pack()
    name.pack()
    date.pack()

    backButton=Button(frame, text="Back to Reserve function", command=frame.destroy)
    updateButton=Button(frame, text="Confirm Reservation", command=lambda: CreateReservation(AccessionNum, ID, Date))
    #update reservation function  newDate = date.today()
    backButton.pack()
    updateButton.pack()

    frame.mainloop()

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
    if len(membersReservation) >= 2:
        failedReservationBooks()
    #if already 2 reservations
    if len(membersFined) > 0:
        failedReservationFine()
    #otherwise Update the Reserve Table
    insert_query  = ("INSERT INTO Reserve " 
                 "(resID, resNum, resDate) " 
                 "VALUES (%s, %s, %s)")
    data = (newID, newNum, newDate)
    mycursor.execute(insert_query,data)
    libraryDB.commit()  

def cancelReservation_Popup(ID, AccessionNumber, Date):
     frame = Toplevel(trial)
     frame.configure(bg="lightgreen")

     #print(AccessionNum.get(), ID, Date.get())

     title=Label(frame, text="Confirm Cancellation Details To Be Correct")
     title.pack()

     mydb = mysql.connector.connect(
     host = "localhost",
     database = 'LIB_ALS',
     user = "root",
     password = "Jokt8989")
     mycursor = mydb.cursor()

     bookTitle_query = "SELECT title FROM books WHERE accNum = %s"
     mycursor.execute(bookTitle_query, (AccessionNumber,))
     bookTitle = mycursor.fetchall()
     print(bookTitle)
     #accessionNum = Label(frame, text=AccessionNum)
     #BookTitle = Label(frame, text=bookTitle[0][0])

     name_query = "SELECT Name FROM members WHERE id = %s"
     mycursor.execute(name_query, (ID,))
     Name = mycursor.fetchall()
     #print(Name)
    
     iD = Label(frame, text=ID)
     name = Label(frame, text=Name[0][0])
     date = Label(frame, text=Date)
     accessionNum = Label(frame, text=AccessionNumber)
     BookTitle = Label(frame, text=bookTitle[0][0])
     accessionNum.pack()
     BookTitle.pack()
     iD.pack()
     name.pack()
     date.pack()    

     cancel_query= "DELETE FROM Reserve WHERE resNum = %s;"
     mycursor.execute(cancel_query, (AccessionNumber,))
     backButton=Button(frame, text="Back to Cancellation function", command=frame.destroy)
     updateButton=Button(frame, text="Confirm Cancellation", command=frame.destroy)
     #update reservation function  newDate = date.today()
     backButton.pack()
     updateButton.pack()
     frame.mainloop()
     

    
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
    successPopupDeletionMembership()
    
def updateMembership(newID,newName,newFac, newPhone,newEmail):
    mydb = mysql.connector.connect(host="127.0.0.1",user="root",
                               password="lozhihao", database="LIB_ALS")
    if "" in (newID.get(),newName.get(),newFac.get(), newPhone.get(),newEmail.get(), newID.get()):
        failedUpdate()
    else:
        mycursor = mydb.cursor()
        input_query = ("""
    UPDATE members
    SET id = %s, Name = %s, Faculty = %s, PhoneNo = %s, Email = %s
    WHERE id = %s
    """ )
        new_member = (newID.get(),newName.get(),newFac.get(), newPhone.get(),newEmail.get(), newID.get())
        mycursor.execute(input_query, new_member)
        mydb.commit()
        mydb.close()
        successPopupUpdateMembership()
    # print(mydb)

def acquireBook(newAcc, newTitle, newAuthor, newIsbn, newPublisher, newPublicationYr):
    libraryDB =mysql.connector.connect(host="127.0.0.1",user="root",
                               password="Jokt8989", database="LIB_ALS")
    mycursor = libraryDB.cursor()
    author_lst = newAuthor.get().split(",")
    filter_query = ("SELECT * FROM books WHERE accNum = %s")
    filter_accNum = (newAcc.get(),)
    mycursor.execute(filter_query, filter_accNum)
    filter_result = mycursor.fetchall()
    while len(author_lst) < 3:
        author_lst.append(None)
    print(author_lst)
    print(newAcc, newTitle, newAuthor, newIsbn, newPublisher, newPublicationYr)
    insert_query  = ("INSERT INTO Books " 
                 "(accNum, title, Author1, Author2, Author3, isbn, publisher, PublicationYr) " 
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    new_book = (newAcc.get(), newTitle.get(), author_lst[0], author_lst[1],author_lst[2], newIsbn.get(), newPublisher.get(), newPublicationYr.get())
    if filter_result != [] or ("" in (newAcc.get(), newTitle.get(), newAuthor.get(), newIsbn.get(), newPublisher.get(), newPublicationYr.get())):
        bookFailedAcquisition()
    else:
        mycursor.execute(insert_query, new_book)
        libraryDB.commit()
        bookSuccessAcquisition()

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

def cancelReservation(memberID, acc, cancelDate):
    allLoanBook = DisplayloanBooks()
    allResBook = reservedBooks()
    loaned = False
    reserved = False
    for i in allLoanBook:
        if i[0] == acc:
            loaned = True
    for i in allResBook:
         if i[0] == acc and i[2] == memberID:
             reserved = True
    if reserved == False:
        failedReservationCancellation()
    elif loaned == True and reserved == True:
        cancelReservation_Popup(memberID, acc, cancelDate)
    
        

# def withdrawBook(newAcc):
#     mydb = mysql.connector.connect(host="127.0.0.1",user="root",
#                                password="Jokt8989", database="LIB_ALS", port=3306)
#     # print(mydb)
#     mycursor = mydb.cursor()
#     input_query =  ("""
#     DELETE FROM Books
#     WHERE accNum = %s;
#     """ )
#     new_deletionID = (newAcc.get(),)
#     if newAcc.get() in map(lambda x :x[0], DisplayloanBooks()):
#         bookFailedWithdrawal_Reserved()
#     else: 
#         if newAcc.get() in map(lambda x:x[0], DisplayReserveBooks()):
#             # cancelReservation(newAcc)
#             bookFailedWithdrawal_Reserved()
#         else:
#             mycursor.execute(input_query, new_deletionID)
#             mydb.commit()
#             mydb.close()



#Fine Payment
def finePayment(memberID, paymentDate, paymentAmt):   
    libraryDB = mysql.connector.connect(host = "localhost",database = 'LIB_ALS',user = "root",password = "Jokt8989")
    mycursor = libraryDB.cursor()
    print(memberID.get())
    if memberID.get() not in list(map(lambda x:x[0], FinedMembers())):
        print("no fine") #promt error: member has no fine
        paymentFailednofine()
    #If memberID not in FinedMembers(): ... Error Prompt 
    #check if paymentAmt == fineAmt correct
    fine_amount_query = "SELECT * FROM Fine WHERE fineID = %s"
    data = memberID.get()
    mycursor.execute(fine_amount_query, (data,))
    

    fineAmt = mycursor.fetchall()[0][1]


    #paymentDate = date.today()
    if float(paymentAmt.get()) != float(fineAmt):
        print("wrong amt") #promt error:amount
        paymentFailedAmt()
    else:
        paymentTry(memberID, paymentDate, paymentAmt)
        #popup confirmation
                    
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

def DisplayReserveBooks():  #accNum, title, id, Name
    #left_join_query = "SELECT m.Name, r.resID, r.resNum FROM Reserve r LEFT JOIN Members m on r.resID = m.ID"
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    join_query = "SELECT r.resNum, b.Title, r.resID, m.Name FROM Reserve r LEFT JOIN Members m on r.resID = m.ID LEFT JOIN Books b on r.resNum = b.accNum"
    mycursor.execute(join_query)
    reservation = mycursor.fetchall()
    return reservation

def reservedBooks():  #accNum, title, id, Name (same as previous one)
    #left_join_query = "SELECT m.Name, r.resID, r.resNum FROM Reserve r LEFT JOIN Members m on r.resID = m.ID"
    mydb = mysql.connector.connect(host="127.0.0.1",user="root", password="Jokt8989", database="LIB_ALS")
    mycursor = mydb.cursor()
    join_query = "SELECT r.resNum, b.Title, r.resID, m.Name FROM Reserve r LEFT JOIN Members m on r.resID = m.ID LEFT JOIN Books b on r.resNum = b.accNum"
    mycursor.execute(join_query)
    reservation = mycursor.fetchall()
    return reservation

def CreateDataTable(data, headers, title, tk):
    tk.title(title)
    tk['bg'] = 'lightblue'

    myFrame = Frame(tk)
    myFrame.pack(fill="both", expand=True)

    myTree = ttk.Treeview(myFrame)
    myTree.pack(fill="both", expand=True)
    myTree['columns'] = headers

    # Setting the scroll
    scroll = ttk.Scrollbar(myFrame, orient="vertical", command=myTree.yview)
    scroll.pack(side = 'right', fill = 'y')
    myTree.configure(yscrollcommand=scroll.set)

    # COLUMNS
    myTree.column("#0", width=0,  stretch=NO)
    myTree.heading("#0",text="",anchor=CENTER)
    for i in headers:
        myTree.column(i, anchor=CENTER, stretch=NO)
        myTree.heading(i, text=i, anchor=CENTER)
    iidCount = 0
    for i in data:
        myTree.insert(parent='', index='end', iid=iidCount, text='', values=i)
        iidCount = iidCount + 1

    myTree.pack()

# def DisplayLoanBooksonFrame(frame, tk):
#     title = "Loaned Books"
#     data = [
#         ('A04', 'Crime and Punishment', 'A101A', 'Hermione Granger'),
#         ('A09', 'Great Expectations', 'A401D', 'Prinche Hamlet')
#     ]
#     headers = ('Accession Number', 'Title', 'MembershipID', 'Name')
#     ##frame = Toplevel(root)
#     frame.configure(bg="purple")
#     # contents = Label(frame, text="ALS Membership created", padx=10, pady=10)
#     # contents.pack()
#     CreateDataTable(data, headers, title, tk)
#     button = Button(frame, text="Back", command=frame.destroy)
#     button.pack()
#     frame.mainloop()

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
fine = Button(main, text="Fines", width=50, pady=40, bg="lightblue", relief=RAISED,
        command=lambda: change_frame(main, fines))
reports = Button(main, text="Reports", width=50, pady=40, bg="lightblue", relief=RAISED,
        command=lambda: change_frame(main, report))

membership.grid(row=0, column=0, columnspan=1)
books.grid(row=0, column=1, columnspan=1)
loans.grid(row=0, column=2, columnspan=1)
title.grid(row=1, column=0, columnspan=3)
reservations.grid(row=2, column=0, columnspan=1)
fine.grid(row=2, column=1, columnspan=1)
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

sCreateMemberID = StringVar()
ID = Entry(create, width=100, bg="cornflowerblue", justify="center", textvariable=sCreateMemberID)
sCreateMemberName = StringVar()
name = Entry(create, width=100, bg="cornflowerblue", justify="center", textvariable=sCreateMemberName)
sCreateMemberFaculty = StringVar()
faculty = Entry(create, width=100, bg="cornflowerblue", justify="center", textvariable=sCreateMemberFaculty)
sCreateMemberPhoneNo = StringVar()
phoneNo = Entry(create, width=100, bg="cornflowerblue", justify="center", textvariable=sCreateMemberPhoneNo)
sCreateMemberEmail = StringVar()
email =  Entry(create, width=100, bg="cornflowerblue", justify="center", textvariable=sCreateMemberEmail)

createnew = Button(create, text=" Create Member ", width=40, pady=30, bg="deepskyblue",
            relief=RAISED, command=lambda: MembershipCreation(sCreateMemberID.get(), sCreateMemberName.get(), sCreateMemberFaculty.get(), sCreateMemberPhoneNo.get(),sCreateMemberEmail.get()))
# lambda: createMembership(ID, name, faculty, phoneNo, email)
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

StringMemberDeleteID = StringVar()
ID = Entry(delete, width=100, bg="cornflowerblue", justify="center", textvariable=StringMemberDeleteID)

deletenew = Button(delete, text=" Delete Member ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: MembershipDeletion(StringMemberDeleteID.get()))

# deletenew = Button(delete, text=" Delete Member ", width=40, pady=30, bg="deepskyblue",
#                relief=RAISED, command=lambda: change_frame(membership, deleteConfirmationFrame))

back = Button(delete, text=" Back To Membership Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(delete, membership))

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)

ID.grid(row=1,column=1)

deletenew.grid(row=2,column=0)
back.grid(row=2,column=1)


# # Delete Confirmation Frame
# deleteConfirmationFrame = Frame(trial)
# deleteConfirmationFrame.configure(bg="yellow")

# deleteBtn = Button(deleteConfirmationFrame, text=" Confirm Deletion ", width=40, pady=30, bg="deepskyblue",
#                relief=RAISED, command=lambda: delete_and_change_frame(deleteConfirmationFrame, membership, StringMemberDeleteID))

# deleteConfirmationFrame.grid()


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

StringUpdateMemberID = StringVar()
ID = Entry(update2, width=100, bg="cornflowerblue", justify="center", textvariable=StringUpdateMemberID)
StringUpdateMemberName = StringVar()
name = Entry(update2, width=100, bg="cornflowerblue", justify="center", textvariable=StringUpdateMemberName)
StringUpdateMemberFaculty = StringVar()
faculty = Entry(update2, width=100, bg="cornflowerblue", justify="center", textvariable=StringUpdateMemberFaculty)
StringUpdateMemberPhoneNo = StringVar()
phoneNo = Entry(update2, width=100, bg="cornflowerblue", justify="center", textvariable=StringUpdateMemberPhoneNo)
StringUpdateMemberEmail = StringVar()
email =  Entry(update2, width=100, bg="cornflowerblue", justify="center", textvariable=StringUpdateMemberEmail)
""".insert(0, "Enter your Email Address")"""

update2new = Button(update2, text=" Update Member ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: updatePopUp(StringUpdateMemberID, StringUpdateMemberName, StringUpdateMemberFaculty, StringUpdateMemberPhoneNo, StringUpdateMemberEmail))
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
               relief=RAISED, command=lambda: change_frame(books, bookAcquisition))
withdrawal = Button(books, text=" 2.Deletion ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(books, bookWithdrawal))


title.grid(row=0,column=0,columnspan=3)
selectOptions.grid(row=1,column=0, columnspan=3)
acquisition.grid(row=2,column=0,columnspan=1)
acquisitiontxt.grid(row=2, column=1, columnspan=2)
withdrawaltxt.grid(row=3, column=1, columnspan=2)
withdrawal.grid(row=3,column=0,columnspan=1)
back.grid(row=4, column=0, columnspan=3)

# book acquisition

bookAcquisition = Frame(trial)
bookAcquisition.configure(bg="yellow")

title = Label(bookAcquisition, text=" For New Book Acquisition, Please Enter Requested Information Below ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

accNumtxt = Label(bookAcquisition, text="Accession Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
booktitletxt = Label(bookAcquisition, text="Title",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
authortxt = Label(bookAcquisition, text="Authors",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
ISBNtxt = Label(bookAcquisition, text="ISBN",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
publishertxt = Label(bookAcquisition, text="Publisher",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
publishYeartxt = Label(bookAcquisition, text="Publish Year",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

sBookAcquireAccNum = StringVar()
accNum = Entry(bookAcquisition, width=100, bg="cornflowerblue", justify="center", textvariable=sBookAcquireAccNum)
sBookAcquireBookTitle = StringVar()
booktitle = Entry(bookAcquisition, width=100, bg="cornflowerblue", justify="center", textvariable=sBookAcquireBookTitle )
sBookAcquireAuthor = StringVar()
author = Entry(bookAcquisition, width=100, bg="cornflowerblue", justify="center", textvariable=sBookAcquireAuthor)
sBookAcquireISBN = StringVar()
ISBN = Entry(bookAcquisition, width=100, bg="cornflowerblue", justify="center", textvariable=sBookAcquireISBN)
sBookAcquirePublisher = StringVar()
publisher =  Entry(bookAcquisition, width=100, bg="cornflowerblue", justify="center", textvariable=sBookAcquirePublisher)
sBookAcquirePublishYear = StringVar()
publishYear =  Entry(bookAcquisition, width=100, bg="cornflowerblue", justify="center", textvariable=sBookAcquirePublishYear)

createnew = Button(bookAcquisition, text=" Add New Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: acquireBook(sBookAcquireAccNum, sBookAcquireBookTitle, sBookAcquireAuthor, sBookAcquireISBN, sBookAcquirePublisher, sBookAcquirePublishYear))
back = Button(bookAcquisition, text=" Back To Book Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(bookAcquisition, books))

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

bookWithdrawal = Frame(trial)
bookWithdrawal.configure(bg="yellow")

title = Label(bookWithdrawal, text=" To Remove Outdated Books From System, Please Enter Required Information Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(bookWithdrawal, text="Accession Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

stringBookWithdrawAccNum = StringVar()
ID = Entry(bookWithdrawal, width=100, bg="cornflowerblue", justify="center", textvariable=stringBookWithdrawAccNum)

deletenew = Button(bookWithdrawal, text=" Withdraw Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: bookTryWithdrawal(stringBookWithdrawAccNum))
back = Button(bookWithdrawal, text=" Back To Books Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(bookWithdrawal, books))


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

sBorrowBookAccNuM = StringVar()
ID = Entry(borrow, width=100, bg="cornflowerblue", justify="center", textvariable=sBorrowBookAccNuM)
sBorrowBookmemberID = StringVar()
memberID = Entry(borrow, width=100, bg="cornflowerblue", justify="center", textvariable=sBorrowBookmemberID)

deletenew = Button(borrow, text=" Borrow Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: borrowBook(sBorrowBookAccNuM.get(), smemberID.get()))
back = Button(borrow, text=" Back To Loans Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(borrow, loans))

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)
memberIDtxt.grid(row=2,column=0,columnspan=1)

ID.grid(row=1,column=1)
memberID.grid(row=2,column=1)

deletenew.grid(row=3,column=0)
back.grid(row=3,column=1)

# loan returning 

#Books Returning
def returnBook(returnNum,returnDate):
    libraryDB = mysql.connector.connect(
    host = "localhost",
    database = 'LIB_ALS',
    user = "root",
    password = "Jokt8989")
    mycursor = libraryDB.cursor()
    #todayDate = date.today()
    fineList = FinedMembers()
    loanBook = DisplayloanBooks()
    select_query = "SELECT * FROM (SELECT * FROM BorrowReturn WHERE returnDate is NULL) AS b WHERE b.borrowNum = %s"
    mycursor.execute(select_query, (returnNum,))
    borrowReturn = mycursor.fetchall()
    #return type(todayDate)
    if returnDate > str(borrowReturn[0][3]):  #if todayDate > dueDate : means got fine to play.
        update_query = "UPDATE BorrowReturn SET returnDate = %s WHERE returnDate IS NULL and borrowNum = %s"
        data = (returnDate, returnNum)
        mycursor.execute(update_query, data)
        # [('A601F', 'A50', datetime.date(2021, 2, 1), datetime.date(2021, 2, 15), None)]
        returnBook_SuccessButHasFine()

bookReturn = Frame(trial)
bookReturn.configure(bg="yellow")

title = Label(bookReturn, text=" To Return a Book, Please Enter Required Information Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

IDtxt = Label(bookReturn, text="Accession Number",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
datetxt = Label(bookReturn, text="Return Date",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

sReturnBookAccID = StringVar()
returnAccID = Entry(bookReturn, width=100, bg="cornflowerblue", justify="center", textvariable=sReturnBookAccID)
sReturnBookDate = StringVar()
returnDate = Entry(bookReturn, width=100, bg="cornflowerblue", justify="center", textvariable=sReturnBookDate)

deletenew = Button(bookReturn, text=" Return Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: returnBook(sReturnBookAccID.get(), sReturnBookDate.get()))
back = Button(bookReturn, text=" Back To Loans Menu  ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(bookReturn, loans))

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)
datetxt.grid(row=2,column=0,columnspan=1)

returnAccID.grid(row=1,column=1)
returnDate.grid(row=2,column=1)

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

sReserveAccNumID = StringVar()
ID = Entry(reserve, width=100, bg="cornflowerblue", justify="center", textvariable=sReserveAccNumID)
sReserveMemberID = StringVar()
memberID = Entry(reserve, width=100, bg="cornflowerblue", justify="center", textvariable=sReserveMemberID)
sReserveDate = StringVar()
date = Entry(reserve, width=100, bg="cornflowerblue", justify="center", textvariable=sReserveDate)

deletenew = Button(reserve, text=" Reserve Book ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: reservationPopUp( sReserveAccNumID.get(), sReserveMemberID.get(), sReserveDate.get()))
back = Button(reserve, text=" Back To Reservation Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(reserve, reservation))



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

sMemberID = StringVar()
ID = Entry(cancel, width=100, bg="cornflowerblue", justify="center", textvariable=sMemberID)
sAccNum = StringVar()
memberID = Entry(cancel, width=100, bg="cornflowerblue", justify="center", textvariable=sAccNum)
sDate = StringVar()
cancelDate = Entry(cancel, width=100, bg="cornflowerblue", justify="center")

deletenew = Button(cancel, text=" Cancel Reservation ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: cancelReservation(sMemberID.get(), sAccNum.get(), sDate.get()))
back = Button(cancel, text=" Back To Reservation Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(cancel, reservation))

title.grid(row=0,column=0,columnspan=3)

IDtxt.grid(row=1,column=0,columnspan=1)
memberIDtxt.grid(row=2,column=0,columnspan=1)
datetxt.grid(row=3,column=0,columnspan=1)

ID.grid(row=1,column=1)
memberID.grid(row=2,column=1)
cancelDate.grid(row=3,column=1)

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

sAmount = StringVar()
amount = Entry(payment, width=100, bg="cornflowerblue", justify="center", textvariable=sAmount)
smemberID = StringVar()
memberID = Entry(payment, width=100, bg="cornflowerblue", justify="center", textvariable = smemberID)
sDate = StringVar()
date = Entry(payment, width=100, bg="cornflowerblue", justify="center", textvariable = sDate)
#date = Label(payment, text= str(date.today()),  width=100, bg = "cornflowerblue", justify = "center",relief=RAISED)

deletenew = Button(payment, text=" Pay Fine ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: finePayment(smemberID, sDate, sAmount))
back = Button(payment, text=" Back To Fines Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(payment, fines))

title.grid(row=0,column=0,columnspan=3)

amounttxt.grid(row=1,column=0,columnspan=1)
memberIDtxt.grid(row=2,column=0,columnspan=1)
datetxt.grid(row=3,column=0,columnspan=1)

amount.grid(row=1,column=1)
memberID.grid(row=2,column=1)
date.grid(row=3,column=1)

deletenew.grid(row=4,column=0)
back.grid(row=4,column=1)


#### Frames Object Declarations ####
LoanPage = Frame(trial)
LoanPage.configure(bg="yellow")

ReservationPage = Frame(trial)
ReservationPage.configure(bg="yellow")

OutstandingFinesPage = Frame(trial)
OutstandingFinesPage.configure(bg="yellow")

BookSearchQueryOutputPage = Frame(trial)
BookSearchQueryOutputPage.configure(bg="yellow")
#### Frames Object Declarations ####


# Reports
report = Frame(trial)
report.configure(bg="yellow")

title = Label(report, text=" Reports ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)
selectOptions = Label(report, text=" Select one of the Options below: ", width=150,
              pady=20, bg="lightblue", relief=RIDGE)

# Book Search UI After Reports
bookSearch = Frame(trial)
bookSearch.configure(bg="yellow")

title = Label(bookSearch, text=" Search Based on One of the Categories Below: ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

booktitletxt = Label(bookSearch, text="Title",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
authortxt = Label(bookSearch, text="Authors",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
ISBNtxt = Label(bookSearch, text="ISBN",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
publishertxt = Label(bookSearch, text="Publisher",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)
publishYeartxt = Label(bookSearch, text="Publish Year",  width=50, pady=10, bg="cornflowerblue",
               relief=RAISED)

sSearchBookBookTitle = StringVar().get()
booktitle = Entry(bookSearch, width=100, bg="cornflowerblue", justify="center", textvariable=sSearchBookBookTitle)

sSearchBookAuthors = StringVar().get()
authors = Entry(bookSearch, width=100, bg="cornflowerblue", justify="center", textvariable=sSearchBookAuthors)

sSearchBookISBN = StringVar().get()
ISBN = Entry(bookSearch, width=100, bg="cornflowerblue", justify="center", textvariable=sSearchBookISBN)

sSearchBookPublisher = StringVar().get()
publisher =  Entry(bookSearch, width=100, bg="cornflowerblue", justify="center", textvariable=sSearchBookPublisher)

sSearchBookPublisherYear = StringVar().get()
publishYear =  Entry(bookSearch, width=100, bg="cornflowerblue", justify="center", textvariable=sSearchBookPublisherYear)

bookSearchQueyBtn = Button(bookSearch, text="Search for Books", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame_and_show_book_search_output(bookSearch, BookSearchQueryOutputPage, sSearchBookBookTitle, sSearchBookAuthors, sSearchBookISBN, sSearchBookPublisher, sSearchBookPublisherYear))

back = Button(bookSearch, text=" Back To Reports Menu ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(bookSearch, report))

### Layout Grid for Search Book Frame ###
title.grid(row=0,column=0,columnspan=3)
booktitletxt.grid(row=1,column=0,columnspan=1)
authortxt.grid(row=2,column=0,columnspan=1)
ISBNtxt.grid(row=3,column=0,columnspan=1)
publishertxt.grid(row=4,column=0,columnspan=1)
publishYeartxt.grid(row=5,column=0,columnspan=1)
booktitle.grid(row=1,column=1)
authors.grid(row=2,column=1)
ISBN.grid(row=3,column=1)
publisher.grid(row=4,column=1)
publishYear.grid(row=5,column=1)
bookSearchQueyBtn.grid(row=6,column=0)
back.grid(row=6,column=1)
### Layout Grid for Search Book Frame ###

# Search for Books #
bookSearchBtnOnReports = Button(report, text=" 1.Search Book ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(report, bookSearch))
bookSearchBtnOnReportstxt = Label(report, text="Book Search Query", width=100, pady=30, bg="cornflowerblue",
               relief=GROOVE)

# Books On Loans #
bookonloan = Button(report, text=" 2.Book On Loan ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame_and_show_loanbooks_data(report, LoanPage))
bookonloanPage = Label(LoanPage, text="Books On Loan Report")
bookonloantxt = Label(report, text="Books On Loan Report", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)

# Books On Reservation
bookonreservation = Button(report, text=" 3.Book On Reservation ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame_and_show_reservebooks_data(report, ReservationPage))
bookonreservationPage = Label(ReservationPage, text="Books On Reservation Report")
bookonreservationtxt = Label(report, text=" Books on Reservation ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)

# Books On Reservation
bookonreservation = Button(report, text=" 3.Book On Reservation ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame_and_show_reservebooks_data(report, ReservationPage))
bookonreservationPage = Label(ReservationPage, text="Books On Reservation Report")
bookonreservationtxt = Label(report, text=" Books on Reservation ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)

# Show Members With Outstanding Fines
outstandingfines = Button(report, text=" 4.Outstanding Fines ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame_and_show_members_with_outstanding_fines(report, OutstandingFinesPage))
outstandingFinesPage = Label(OutstandingFinesPage, text="Show Members With Outstanding Fines")
outstandingfinestxt = Label(report, text=" Members With Outstanding Fines ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)

bookonloantomembers = Button(report, text=" 5.Book On Loan To Members ", width=50, pady=30, bg="dodgerblue",
               relief=RAISED, command=lambda: change_frame(report, bookOnLoanToMember))
bookonloantomemberstxt = Label(report, text=" Book On Loan To Members ", width=100, pady=30, bg="dodgerblue",
               relief=GROOVE)

back = Button(report, text=" Back to Main Menu ", width=150, pady=20,
              bg="lightblue", relief=RAISED, command=lambda: change_frame(report, main))


### Layout ###
title.grid(row=0,column=0,columnspan=3)
selectOptions.grid(row=1,column=0, columnspan=3)

bookSearchBtnOnReports.grid(row=2,column=0,columnspan=1)
bookSearchBtnOnReportstxt.grid(row=2, column=1, columnspan=2)

bookonloantxt.grid(row=3, column=1, columnspan=2)
bookonloan.grid(row=3, column=0, columnspan=1)

bookonreservation.grid(row=4, column=0, columnspan=1)
bookonreservationtxt.grid(row=4, column=1, columnspan=2)

outstandingfines.grid(row=5, column=0, columnspan=1)
outstandingfinestxt.grid(row=5, column=1, columnspan=2)

bookonloantomembers.grid(row=6, column=0, columnspan=1)
bookonloantomemberstxt.grid(row=6, column=1, columnspan=2)

back.grid(row=7, column=0, columnspan=3)


# book on loan to member

bookOnLoanToMember = Frame(trial)
bookOnLoanToMember.configure(bg="yellow")

bookOnLoanToMemberReportFrame = Frame(trial)
bookOnLoanToMemberReportFrame.configure(bg="yellow")

title = Label(bookOnLoanToMember, text=" Book On Loan To member ", width=150, pady=20, bg="lightgreen"
              ,relief=RIDGE)

memberIDtxt = Label(bookOnLoanToMember, text=" MembershipID ", width=50, pady=20, bg="lightgreen"
              ,relief=RIDGE)

sBookOnLoanMemberID = StringVar().get()
memberID = Entry(bookOnLoanToMember, text=" MembershipID ", width=100, bg="lightgreen"
              ,relief=RIDGE, textvariable=sBookOnLoanMemberID)

showMemberOnLoan = Button(bookOnLoanToMember, text=" Show Member ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame_and_show_Book_On_Loan_To_Member(bookOnLoanToMember, bookOnLoanToMemberReportFrame, sBookOnLoanMemberID))

backToReport = Button(bookOnLoanToMember, text=" Back To report ", width=40, pady=30, bg="deepskyblue",
               relief=RAISED, command=lambda: change_frame(bookOnLoanToMember, report))

title.grid(row=0, column=0, columnspan=3)
memberIDtxt.grid(row=1, column=0, columnspan=1)
memberID.grid(row=1, column=1, columnspan=2)
showMemberOnLoan.grid(row=2, column=1)
backToReport.grid(row=2, column=2)

# Closing Tkinter

trial.mainloop()
