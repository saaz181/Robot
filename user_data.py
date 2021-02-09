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
        
    def save_stock(self, username=None, password=None, stock_name=None, stock_description=None):
        if self.table == "stock":
            self.cursor.execute("INSERT INTO stocks VALUES (:s_name, :s_description)", 
            {
                "s_name": stock_name,
                "s_description": stock_description
            }) 
            
        elif self.table == "user":
            self.cursor.execute("INSERT INTO users VALUES (:_user, :_password)", 
            {
                "_user": username,
                "_password": password
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

        self.con.commit()
        self.con.close()

    def show_single_query(self, pk):
        if self.table == "stock":
            try:
                self.cursor.execute(f"SELECT *, rowid FROM stocks WHERE rowid = {pk}")
                self.stock = self.cursor.fetchall()
                self.con.commit()

                return self.stock
            except sqlite3.OperationalError:
                messagebox.showerror(title="Stock Pk", message="You haven't spcefied any primary key")
        elif:

            try:
                self.cursor.execute(f"SELECT *, rowid FROM users WHERE rowid = {pk}")
                self.user_names = self.cursor.fetchall()
                self.con.commit()

                return self.user_names
            except sqlite3.OperationalError:
                messagebox.showerror(title="Stock Pk", message="You haven't spcefied any primary key")


    def delete(self, pk):
        if self.table == "stock":
            self.cursor.execute(f"DELETE FROM stocks WHERE rowid = {pk}")
        
        elif self.table == "user":
            self.cursor.execute(f"DELETE FROM users WHERE rowid = {pk}")
       
        self.con.commit()
        self.con.close()
       
    def update(self, name=None, description=None, username=None, password=None, pk):
        if self.table == "stock":
            self.cursor.execute("""UPDATE stocks SET name = :_name, description = :_description WHERE oid = :oid""", {
                '_name': name,
                '_description': description,
                'oid': pk
            })
        
        elif self.table == "user":
            self.cursor.execute("""UPDATE users SET user_name = :_user, user_password = :_password WHERE oid = :oid""", {
                '_user': username,
                '_password': password,
                'oid': pk
            })
        self.con.commit()
        self.con.close()                       
            

