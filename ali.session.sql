CREATE TABLE IF NOT EXISTS employee (
    emp_id INT PRIMARY KEY,
    first_name VARCHAR(40),
    last_name VARCHAR(40),
    birth_day DATE,
    sex VARCHAR(1),
    salary INT,
    super_id INT,
    branch_id INT
);

CREATE TABLE IF NOT EXISTS branch (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(40),
    mgr_id INT,
    mgr_start_date DATE,
    FOREIGN KEY (mgr_id) REFERENCES employee(emp_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS client (
    client_id INT PRIMARY KEY,
    client_name VARCHAR(40),
    branch_id INT,
    FOREIGN KEY(branch_id) REFERENCES branch(branch_id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS works_with (
    emp_id INT,
    client_id INT,
    total_sales INT,
    PRIMARY KEY (emp_id, client_id),
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS branch_supplier (
    branch_id INT,
    supplier_name VARCHAR(40),
    supply_type VARCHAR(40),
    PRIMARY KEY (branch_id, supplier_name),
    FOREIGN KEY(branch_id) REFERENCES branch(branch_id) ON DELETE CASCADE
);


ALTER TABLE employee
ADD FOREIGN KEY(branch_id)
REFERENCES branch(branch_id)
ON DELETE SET NULL;


 ALTER TABLE employee
ADD FOREIGN KEY (super_id)
REFERENCES employee(emp_id)
ON DELETE SET NULL;


-- INSERT INTO employee VALUES(100, 'David', 'Wallace', '1967-11-17', 'M', 250000, NULL, NULL);

-- INSERT INTO branch VALUES(1, 'Corporate', 100, '2006-02-09');

-- UPDATE employee
-- SET branch_id = 1
-- WHERE emp_id = 100;

-- INSERT INTO employee VALUES(101, 'Jan', 'Levinson', '1961-05-11', 'F', 110000, 100, 1);

INSERT INTO employee VALUES (102, 'Michael', 'Scott', '1964-03-15', 'M', 75000, 100, NULL);
INSERT INTO branch VALUES (2, 'Scranton', 102, '1992-04-06');

UPDATE employee
SET branch_id = 2
WHERE emp_id = 102;

INSERT INTO employee VALUES (103, 'Angela', 'Martin', '1971-06-25', 'F', 63000, 102, 2);
INSERT INTO employee VALUES (104, 'Kelly', 'Kapoor', '1980-02-05', 'F', 55000, 102, 2);
INSERT INTO employee VALUES (105, 'Stanely', 'Hudson', '1958-02-19', 'M', 69000, 102, 2 ); */


INSERT INTO employee VALUES(106, 'Josh', 'Porter', '1969-09-05', 'M', 78000, 100, NULL);
INSERT INTO branch VALUES(3, 'Stamford', 106, '1998-02-13');

UPDATE employee
SET branch_id = 3
WHERE emp_id = 106;

INSERT INTO employee VALUES(107, 'Andy', 'Bernard', '1973-07-22', 'M', 65000, 100, 3);
INSERT INTO employee VALUES(108, 'Jim', 'Halpert', '1978-10-01', 'M', 71000, 100, 3);



-- BRANCH SUPPLIER 

INSERT INTO branch_supplier VALUES (2, 'Hammer Mill', 'Paper');
INSERT INTO branch_supplier VALUES (2, 'Uni-ball', 'Writing Utensils');
INSERT INTO branch_supplier VALUES (3, 'Patriot Paper', 'Paper');
INSERT INTO branch_supplier VALUES (2, 'J.T. Forms & Labels', 'Custom Forms');
INSERT INTO branch_supplier VALUES (3, 'Uni-ball', 'Writing Utensils');
INSERT INTO branch_supplier VALUES (3, 'Hammer Mill', 'Paper');
INSERT INTO branch_supplier VALUES (3, 'Stamford Labels', 'Custom Forms');

-- CLIENT

INSERT INTO client VALUES (400, 'Dunmore Highschool', 2);
INSERT INTO client VALUES (401, 'Lackawana Country', 2);
INSERT INTO client VALUES (402, 'FedEx', 3);
INSERT INTO client VALUES (403, 'John Daly Law, LLC', 3);
INSERT INTO client VALUES (404, 'Scranton Whitepages', 2);
INSERT INTO client VALUES (405, 'Times Newspaper', 3);
INSERT INTO client VALUES (406, 'FedEx', 2);



-- WORKS WITH

INSERT INTO works_with VALUES (105, 400, 55000);
INSERT INTO works_with VALUES (102, 401, 267000);
INSERT INTO works_with VALUES (108, 402, 22500);
INSERT INTO works_with VALUES (107, 403, 5000);
INSERT INTO works_with VALUES (108, 403, 12000);
INSERT INTO works_with VALUES (105, 404, 33000);
INSERT INTO works_with VALUES (107, 405, 26000);
INSERT INTO works_with VALUES (102, 406, 15000);
INSERT INTO works_with VALUES (105, 406, 130000);

-- find diffrent values in particular column
 SELECT DISTINCT sex
FROM employee;

-- find the number of female employee born after 1970-01-01

SELECT COUNT(emp_id)
FROM employee
WHERE sex = 'F' AND birth_day > '1970-01-01';

-- AVG: average of column, SUM: sum of column

SELECT COUNT(sex), sex
FROM employee
GROUP BY sex;*/

SELECT SUM(total_sales), emp_id
FROM works_with
GROUP BY emp_id;
 

-- % = any # characters, _ = one character

SELECT *
FROM client
WHERE client_name LIKE '%school%';



-- Find a list of employee and branch names
-- UNION RULES:
-- 1- same amout of column, 2 - same data type
SELECT first_name AS Company_names
FROM employee
UNION
SELECT branch_name
FROM branch
UNION
SELECT client_name
FROM client;

 
SELECT client_name, client.branch_id
FROM client
UNION
SELECT supplier_name, branch_supplier.branch_id
FROM branch_supplier;

-- JOINs

-- INSERT INTO branch VALUES (4, 'Buffalo', NULL, NULL);
-- Find all branches and the names of their managers

-- Inner= JOIN, LEFT JOIN, RIGHT JOIN


SELECT employee.emp_id, employee.first_name, branch.branch_name
FROM employee
JOIN branch
ON employee.emp_id = branch.mgr_id;


-- NESTED QUERIS --

-- find names of all employees who have
-- sold over 30,000 to a single client

SELECT employee.first_name, employee.last_name
FROM employee
WHERE employee.emp_id IN (
    SELECT works_with.emp_id
    FROM works_with
    WHERE works_with.total_sales > 30000
);


-- find all clients who are handled by the branch
-- that Michael Scott manages
-- Assume you know Micheal's ID (i didn't)


SELECT client.client_name
FROM client
WHERE client.branch_id = (
    SELECT branch.branch_id
    FROM branch
    WHERE branch.mgr_id = (
        SELECT employee.emp_id
        FROM employee
        WHERE employee.first_name = 'Michael' AND employee.last_name = 'Scott'
        LIMIT 1
    )
);

CREATE TABLE trigger_test(
    _message VARCHAR(100)
);


-- DELIMITER is like semi-colon ';' to delemite the sql command
-- we use $$ to change delemiter at first then we end our delemiter
-- then we change our delemiter to normal semi-colon ';'
DELIMITER $$
CREATE 
    TRIGGER my_trigger BEFORE INSERT 
    ON employee
    FOR EACH ROW BEGIN 
        INSERT INTO trigger_test VALUES ('added new employee');
    END $$
DELIMITER ;        


DELIMITER $$
CREATE 
    TRIGGER  my_trigger1 BEFORE INSERT 
    ON employee
    FOR EACH ROW BEGIN 
        INSERT INTO trigger_test VALUES(NEW.first_name);
    END $$
DELIMITER ;    

-- trigger for update, insert, delete
-- befor <command> or after <commnad>
-- command = delete, insert, update
-- deleting trigger:
--          DROP TRIGGER <name_of_our_trigger>;

DELIMITER $$
CREATE 
    TRIGGER my_trigger2 AFTER INSERT 
    ON employee
    FOR EACH ROW BEGIN 
        IF NEW.sex = 'M' THEN
            INSERT INTO trigger_test VALUES('added male employee');
        ELSE IF NEW.sex = 'F' THEN
            INSERT INTO trigger_test VALUES('added female');
        ELSE
            INSERT INTO trigger_test VALUES('added other employee');
        END IF;
    END $$
DELIMITER ;

-- ER Diagrams

select * from trigger_test;

INSERT INTO employee
VALUES (112, 'Ali', 'Alavizadeh', '2002-08-15', 'M', 110000, 100, 2);







CREATE TABLE Account (
    AccName VARCHAR(100),
    _Password VARCHAR(100),
    LastSignedOn DATE,
    SbscrbrName VARCHAR(100),
    SbscrbrEmain VARCHAR (100),
    SbscrbrPhone VARCHAR(100),
    AccCreatedOn DATE,
    PRIMARY KEY (AccName)
);
ALTER TABLE Account
ADD COLUMN SbscrbrAddress VARCHAR(100) AFTER SbscrbrName;

CREATE TABLE Creep (
    CreepName VARCHAR(100),
    HitPoints VARCHAR(100),
    Mana VARCHAR(100),
    Attack VARCHAR(100),
    PRIMARY KEY (CreepName)
);

CREATE TABLE Region (
    RegionName VARCHAR(100),
    Climate VARCHAR(100),
    Precipitation VARCHAR(100),
    Follage VARCHAR(100) DEFAULT NULL ,
    PlayesIn INT,
    PRIMARY KEY (RegionName) 
);

CREATE TABLE _Character (
    CharName VARCHAR(100),
    MaxHitPoint INT,
    _Level INT,
    MaxMana INT,
    ExpPoints INT,
    CurrHitPoint INT,
    _Type VARCHAR (30),
    CurrMana INT,
    AccName VARCHAR (100),
    RegionName VARCHAR (100),
    FOREIGN KEY (AccName) REFERENCES Account(AccName) ON DELETE CASCADE,
    FOREIGN KEY (RegionName) REFERENCES Region(RegionName) ON DELETE SET NULL 
);

ALTER TABLE _character
ADD COLUMN Has_Account INT AFTER CurrMana;

ALTER TABLE _Character
ADD PRIMARY KEY (CharName);

INSERT INTO _character
VALUES ('kalsd', 80, 5, 30, 10, 110, 'Dragon', 20, 0, NULL, 'Alakida');

CREATE TABLE Has (
    AccName VARCHAR (100),
    LastPlayed DATE,
    CreatedON DATE,
    PRIMARY KEY (AccName),
    FOREIGN KEY (AccName) REFERENCES Account(AccName) ON DELETE CASCADE
);

CREATE TABLE RanInfo (
    CharName VARCHAR (100),
    CreepName VARCHAR (100),
    PRIMARY KEY (CharName, CreepName),
    FOREIGN KEY (CharName) REFERENCES _Character(CharName) ON DELETE CASCADE,
    FOREIGN KEY (CreepName) REFERENCES Creep(CreepName) ON DELETE CASCADE 
);

INSERT INTO raninfo
VALUES ('saaz', 'Assassins');


CREATE TABLE Creep_Instantiation (
    IDNum INT,
    CreepName VARCHAR (100),
    RegionName VARCHAR (100),
    PRIMARY KEY (IDNum),
    FOREIGN KEY (CreepName) REFERENCES Creep(CreepName) ON DELETE CASCADE,
    FOREIGN KEY (RegionName) REFERENCES Region(RegionName) ON DELETE CASCADE
);

INSERT INTO creep_instantiation
VALUES (1, 'Assassins', 'Alakida');

CREATE TABLE Item (
    ItemName VARCHAR (100),
    ItemType VARCHAR (100),
    ItemDamage INT,
    PRIMARY KEY (ItemName)
);
INSERT INTO item
VALUES ('blade', 'old', 50);


CREATE TABLE Item_Instantiation (
    IDNum INT,
    Modifier VARCHAR (50),
    CharName VARCHAR (100),
    _IDNum INT,
    ItemName VARCHAR (100),
    PRIMARY KEY (IDNum),
    FOREIGN KEY (ItemName) REFERENCES Item(ItemName) ON DELETE CASCADE,
    FOREIGN KEY (_IDNum) REFERENCES Creep_Instantiation(IDNum) ON DELETE SET NULL,
    FOREIGN KEY (CharName) REFERENCES _Character(CharName) ON DELETE SET NULL
);

INSERT INTO item_instantiation
VALUES (1, 'GUN', 'saaz', 1, 'blade');

CREATE TABLE IsType (
    ItemName VARCHAR (100) PRIMARY KEY,
    WhenCreated DATE,
    FOREIGN KEY (ItemName) REFERENCES Item(ItemName) ON DELETE CASCADE
);



INSERT INTO Account
VALUES ('SAAZ', '0926218867', '2020-09-15', 'Ali', 'USA', 'sadsd@gmail.com', '09156455409', '2020-10-25');

INSERT INTO Region
VALUES ('Alakida', 'Freezing', 'Hard', '54', 50);

INSERT INTO Creep
VALUES ('Assassins', 'High', 'FFKK', 'Front');

DELIMITER $$
CREATE
    TRIGGER add_has AFTER INSERT 
    ON _Character
    FOR EACH ROW BEGIN
        IF NEW.Has_Account = 1 THEN 
            INSERT INTO Has VALUES (New.AccName, '2020-02-13', '2020-10-15');
        END IF;
    END $$
DELIMITER ;

DELIMITER $$
CREATE 
    TRIGGER add_type AFTER INSERT 
    ON Item
    FOR EACH ROW BEGIN 
        INSERT INTO IsType VALUES (NEW.ItemName, NOW());
    END $$
DELIMITER ;



SELECT AccName
FROM account
WHERE account.AccName = _character.AccName;   










