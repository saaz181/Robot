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
                    user_name VARCHAR(255),
                    user_password VARCHAR(255)
                )
                """)

        elif self.table == "stock":
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                name VARCHAR(255),
                description VARCHAR(255)
            )
            """)
        
    def save_information(self, username=None, password=None, name=None, description=None):
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
        
        self.con.close()

    def delete(self, name=None, username=None):
        if self.table == "stock":
            self.cursor.execute(f"DELETE FROM stocks WHERE name = '{name}'")
        
        elif self.table == "user":
            self.cursor.execute(f"DELETE FROM users WHERE user_name = '{username}'")
       
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
        self.con.commit()
        self.con.close()                       
            

