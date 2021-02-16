import sqlite3
from tkinter import messagebox

class StockData:
    def __init__(self, table):
        self.con = sqlite3.connect("stocks.db")
        self.table = table
        self.cursor = self.con.cursor()

        if self.table == "user":
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_name VARCHAR(30),
                    user_password VARCHAR(30)
                )
                """)

        elif self.table == "stock":
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                name VARCHAR(20),
                description VARCHAR(30)
            )
            """)

        elif self.table == "record":
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    username VARCHAR(30),
                    stock_name VARCHAR(20),
                    quantity INT,
                    stock_price INT,
                    trade_type VARCHAR(1),
                    trade_date DATE,
                    trade_time INT,
                    start_time INT,
                    end_time INT,
                    FOREIGN KEY (username) REFERENCES users(user_name) ON DELETE SET NULL
                )
            """) 
        
    def save_information(self, username=None, password=None, name=None, description=None, quantity=0, stock_price=0, 
                                trade_type=None, trade_date=None, trade_time=None, start_time=None, end_time=None):
        if self.table == "stock":
            if name != None:
                self.cursor.execute("INSERT INTO stocks VALUES (:s_name, :s_description)", 
                {
                    "s_name": name,
                    "s_description": description
                }) 
                
        elif self.table == "user":
            if username != None and password != None:
                self.cursor.execute("INSERT INTO users VALUES (:_user, :_password)", 
                {
                    "_user": username,
                    "_password": password
                }) 
            else:
                messagebox.showerror(title="Empty field", message="نام کاربری یا پسورد وارد نشده است")

        elif self.table == "record":
            self.cursor.execute("INSERT INTO records VALUES (:_username, :_stock_name, :_quantity, \
                                                            :_stock_price, :_trade_type, :_trade_date, \
                                                            :_trade_time, :_start_time, :_end_time)",
                                {
                                    '_username': username,
                                    '_stock_name': name,
                                    '_quantity': quantity,
                                    '_stock_price': stock_price,
                                    '_trade_type': trade_type,
                                    '_trade_date': trade_date,
                                    '_trade_time': trade_time,
                                    '_start_time': start_time,
                                    '_end_time': end_time

                                })

        self.con.commit()
        self.con.close()

    def show(self):
        if self.table == "stock":
            self.cursor.execute("SELECT *, oid FROM stocks")
            self.stocks = self.cursor.fetchall()
            
            return self.stocks

        elif self.table == "user":
            self.cursor.execute("SELECT *, oid FROM users")
            self.user_pass = self.cursor.fetchall()
            
            return self.user_pass

        elif self.table == "record":
            self.cursor.execute("SELECT *, oid FROM records")
            self.records = self.cursor.fetchall()

            return self.records

        self.con.commit()
        self.con.close()

    def show_single_query(self, username=None, name=None):
        if self.table == "stock":
            try:
                self.cursor.execute(f"SELECT *, oid FROM stocks WHERE name = '{name}'")
                self.stock = self.cursor.fetchall()
                self.con.commit()

                return self.stock
            except sqlite3.OperationalError:
                messagebox.showerror(title="Stock Pk", message="You haven't spcefied any primary key")
        
        elif self.table == "user":
            try:
                self.cursor.execute(f"SELECT *, oid FROM users WHERE user_name = '{username}'")
                self.user_names = self.cursor.fetchall()
                self.con.commit()

                return self.user_names
            except sqlite3.OperationalError:
                messagebox.showerror(title="Stock Pk", message="You haven't spcefied any primary key")
        
        elif self.table == "record":
            try:
                self.cursor.execute(f"SELECT *, oid FROM records WHERE username = '{username}'")
                self.single_user_record = self.cursor.fetchall()
                self.con.commit()

                return self.single_user_record
            except sqlite3.OperationalError:
                messagebox.showerror(title="Stock Pk", message="You haven't spcefied any primary key")        

        self.con.close()


    def delete(self, name=None, username=None, pk=None):
        if self.table == "stock":
            self.cursor.execute(f"DELETE FROM stocks WHERE name = '{name}'")
            
        elif self.table == "user":
            self.cursor.execute(f"DELETE FROM users WHERE user_name = '{username}'")

        elif self.table == "record":
            if username:
                self.cursor.execute(f"DELETE FROM records WHERE username = '{username}'")
            elif pk:
                self.cursor.execute(f"DELETE FROM records WHERE oid = '{pk}'")                

        self.con.commit()
        self.con.close()
       
    def update(self, name=None, description=None, username=None, password=None, pk=None):
        if self.table == "stock":
            self.cursor.execute(f"UPDATE stocks SET name = :s_name, description = :s_description WHERE oid = '{pk}'", {
                "s_name": name,
                "s_description": description
            })
        
        elif self.table == "user":
            self.cursor.execute(f"UPDATE users SET user_name = :_user, user_password = :_password WHERE oid = '{pk}'", {
                '_user': username,
                '_password': password
            })

        # TODO: we may probably wants to create update

        self.con.commit()
        self.con.close()                       




