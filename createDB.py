import sqlite3 as sql

def create_DB():

    con = sql.connect('db_web.db')

    #Cria o cursor para se fazer as queries SQL
    cur = con.cursor()

    #Cria a tabela utilizadores do zero.
    query = """CREATE TABLE utilizadores 
    ('Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'User' TEXT,
    'Salt' TEXT,
    'Password' TEXT ,
    'role' TEXT )"""
    
    cur.execute(query)

    #'Comita' as mudanças
    con.commit()

    con.close()

