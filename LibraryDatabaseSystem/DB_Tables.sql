USE LIB_ALS;
CREATE DATABASE LIB_ALS;

CREATE TABLE Members(
	id VARCHAR(10) NOT NULL UNIQUE,
    Name VARCHAR(30) NOT NULL,
    Faculty VARCHAR(15) NOT NULL,
    PhoneNo VARCHAR(15) NOT NULL,
    Email VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(id));
    

CREATE TABLE Books(
	accNum VARCHAR(15) NOT NULL UNIQUE,
    title VARCHAR(150) NOT NULL,
    Author1 VARCHAR(100) NOT NULL,
    Author2 VARCHAR(100),
	Author3 VARCHAR(100),
    isbn VARCHAR(20) NOT NULL,
    publisher VARCHAR(50) NOT NULL,
    PublicationYr INT(4) NOT NULL,
    PRIMARY KEY(accNum));

CREATE TABLE Reserve(
	resID VARCHAR(10) NOT NULL,
	resNum VARCHAR(15) NOT NULL UNIQUE,
    resDate DATE NOT NULL,
    FOREIGN KEY(resID) references Members(id),
    FOREIGN KEY(resNum) references Books(accNum));
    
    
CREATE TABLE Fine(
	fineID VARCHAR(10) NOT NULL UNIQUE,
    fineAmt DECIMAL(20,2) NOT NULL,
    FOREIGN KEY(fineID) references Members(id) 
    );
    
CREATE TABLE SettlePayment(
	payID VARCHAR(10) NOT NULL UNIQUE,
    payAmt DECIMAL(20,2) NOT NULL,
    payDate DATE NOT NULL,
    FOREIGN KEY(payID) references Members(id) 
    );
    
CREATE TABLE BorrowReturn(
	borrowID VARCHAR(10) NOT NULL,
    borrowNum VARCHAR(15) NOT NULL,
    borrowedDate DATE NOT NULL, 
    dueDate DATE,
    returnDate DATE,
    FOREIGN KEY(borrowID) references Members(id),
    FOREIGN KEY(borrowNum) references Books(accNum));

SHOW GLOBAL VARIABLES LIKE 'FOREIGN_KEY_CHECKS';
SET FOREIGN_KEY_CHECKS = 0;
SET GLOBAL FOREIGN_KEY_CHECKS = 0;


    








	
