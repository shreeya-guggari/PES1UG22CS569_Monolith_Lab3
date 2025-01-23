import json
import os
import sqlite3

def connect(path):
    exists = os.path.exists(path)
    conn = sqlite3.connect(path)
    if not exists:
        create_tables(conn)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT,
            cost REAL
        )
    ''')
    conn.commit()

def get_cart(username: str) -> list:
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return eval(row['contents']) if row and row['contents'] else []

def add_to_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    contents = eval(row['contents']) if row and row['contents'] else []
    contents.append(product_id)
    cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                   (username, json.dumps(contents), 0))
    conn.commit()
    cursor.close()
    conn.close()

def remove_from_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row and row['contents']:
        contents = eval(row['contents'])
        if product_id in contents:
            contents.remove(product_id)
            cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                           (username, json.dumps(contents), 0))
            conn.commit()
    cursor.close()
    conn.close()

def delete_cart(username: str):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carts WHERE username = ?', (username,))
    conn.commit()
    cursor.close()
    conn.close()

