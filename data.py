import sqlite3
from tkinter import messagebox
import csv

def read_from_csv():
    with open('stock.txt') as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(row)
            line_count += 1
    
    print(f'Processed {line_count} lines.')




class StockData:
    def __init__(self):
        self.con = sqlite3.connect("stocks.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            name VARCHAR(255),
            description VARCHAR(255)
        )
        """)
    
    def save_stock(self, stock_name, stock_description):
        self.cursor.execute("INSERT INTO stocks VALUES (:s_name, :s_description)", 
        {
            "s_name": stock_name,
            "s_description": stock_description
        }) 
        self.con.commit()
        self.con.close()
        
    def show(self):
        self.cursor.execute("SELECT *, oid FROM stocks")
        self.stocks = self.cursor.fetchall()
        self.con.commit()
        self.con.close()

        return self.stocks
    
    def show_single_query(self, pk):
        try:
            self.cursor.execute(f"SELECT *, rowid FROM stocks WHERE rowid = {pk}")
            self.stock = self.cursor.fetchall()
            self.con.commit()

            return self.stock
        except sqlite3.OperationalError:
            messagebox.showerror(title="Stock Pk", message="You haven't spcefied any primary key")

    def delete(self, pk):
        self.cursor.execute(f"DELETE FROM stocks WHERE rowid = {pk}")
        self.con.commit()
        self.con.close()

    def update(self, name, description, pk):
        self.cursor.execute("""UPDATE stocks SET name = :_name, description = :_description WHERE oid = :oid""", {
            '_name': name,
            '_description': description,
            'oid': pk
        })
        self.con.commit()
        self.con.close()                       


