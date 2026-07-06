BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Attendance" (
	"attID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"enrollID"	INTEGER,
	"date"	TEXT,
	"status"	TEXT
);
CREATE TABLE IF NOT EXISTS "Scores" (
	"scoreID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"enrollID"	INTEGER,
	"score"	REAL,
	"result"	TEXT
);
CREATE TABLE IF NOT EXISTS "Enrollments" (
	"enrollID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"userID"	INTEGER,
	"courseID"	INTEGER,
	"date"	TEXT,
	"status"	TEXT
);
CREATE TABLE IF NOT EXISTS "Teachers" (
	"name"	TEXT NOT NULL,
	"phone"	INTEGER NOT NULL,
	"skill"	TEXT NOT NULL,
	"teacherID"	INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE IF NOT EXISTS "Courses" (
	"name"	TEXT NOT NULL,
	"langID"	INTEGER NOT NULL,
	"teacherID"	INTEGER NOT NULL,
	"sessions"	INTEGER NOT NULL,
	"price"	INTEGER NOT NULL,
	"courseID"	INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE IF NOT EXISTS "Invoice_item" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"lengID"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"invoice_id"	INTEGER NOT NULL,
	"price"	INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS "Invoices" (
	"invoicesID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"userID"	INTEGER NOT NULL,
	"total_price"	REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS "Lang" (
	"langID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	INTEGER NOT NULL UNIQUE,
	"price"	REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS "Users" (
	"userID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT NOT NULL,
	"phone"	INTEGER NOT NULL
);
INSERT INTO "Enrollments" ("enrollID","userID","courseID","date","status") VALUES (2,3,2,'1405.04.04','فعال'),
 (3,5,1,'1405.04.06','لغو شده');
INSERT INTO "Teachers" ("name","phone","skill","teacherID") VALUES ('بقايي فاطي',12345,'انگليسي ترکي',1),
 ('زهرا بقائي',4567,'فرانسوي',2),
 ('عاطفه بقائي',12345,'ترکي',3);
INSERT INTO "Courses" ("name","langID","teacherID","sessions","price","courseID") VALUES ('ترم تابستاني انگليسي',3,1,12,5600,1),
 ('ترم تابستانه ترکي',5,3,14,4800,2);
INSERT INTO "Invoice_item" ("id","lengID","quantity","invoice_id","price") VALUES (1,4,5,1,5555555555);
INSERT INTO "Invoices" ("invoicesID","userID","total_price") VALUES (1,4,5555555555.0);
INSERT INTO "Lang" ("langID","name","price") VALUES (3,'انگليسي',5700.0),
 (4,'فرانسوي',11000.0),
 (5,'ترکي استانبولي',10500.0),
 (6,'اسپانيايي',10700.0);
INSERT INTO "Users" ("userID","name","phone") VALUES (2,'baghaei',9331997166),
 (3,'fati',9133333333),
 (5,'زهرا',1234);
COMMIT;
