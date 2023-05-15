CREATE TABLE accounts (
  accountId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ownerName VARCHAR(45) NOT NULL,
  owner_ssn INT NOT NULL,
  balance DECIMAL(10,2) DEFAULT 0.00,
  account_status VARCHAR(45),
  UNIQUE (accountId)
);

CREATE TABLE IF NOT EXISTS Transactions (
  transactionId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  accountID INT NOT NULL,
  transactionType VARCHAR(45) NOT NULL,
  transactionAmount DECIMAL(10, 2) NOT NULL,
  UNIQUE (transactionId)
);

INSERT INTO accounts (ownerName, owner_ssn, balance, account_status)
VALUES ('Maria Jozef', 123456789, 10000.00, 'active'),
       ('Linda Jones', 987654321, 2600.00, 'inactive'),
       ('John McGrail', 222222222, 100.50, 'active'),
       ('Patty Luna', 111111111, 509.75, 'inactive');

INSERT INTO Transactions (accountID, transactionType, transactionAmount)
VALUES (1, 'deposit', 650.98),
       (3, 'withdraw', 899.87),
       (3, 'deposit', 350.00);

CREATE PROCEDURE accountTransactions (IN accountID INT)
BEGIN
  SELECT *
  FROM Transactions
  WHERE accountID = accountID;
END 


CREATE PROCEDURE deposit (IN p_accountID INT, IN p_amount DECIMAL(10,2))
BEGIN
  INSERT INTO Transactions (accountID, transactionType, transactionAmount)
  VALUES (p_accountID, 'deposit', p_amount);
  
  UPDATE accounts
  SET balance = balance + p_amount
  WHERE accountId = p_accountID;
END


CREATE PROCEDURE withdraw (IN p_accountID INT, IN p_amount DECIMAL(10,2))
BEGIN
  DECLARE current_balance DECIMAL(10,2);
  
  SELECT balance INTO current_balance
  FROM accounts
  WHERE accountId = p_accountID;
  
  IF current_balance >= p_amount THEN
    INSERT INTO Transactions (accountID, transactionType, transactionAmount)
    VALUES (p_accountID, 'withdraw', p_amount);
  
    UPDATE accounts
    SET balance = balance - p_amount
    WHERE accountId = p_accountID;
  ELSE
    SELECT 'Insufficient balance' AS error;
  END IF;
END 

