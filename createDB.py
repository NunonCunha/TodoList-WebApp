import sqlite3 as sql

def create_DB():

    #Cria o ficheiro da base dados e dá connect
    dBase = sql.connect('db_todoApp.db')

    #Cria o cursor para fazer queries SQL
    cursor = dBase.cursor()

    #Query para criar tabela user 
    qry_tableUser = """CREATE TABLE IF NOT EXISTS user 
    ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'first_name' TEXT,
    'last_name' TEXT,
    'email' TEXT UNIQUE NOT NULL,
    'salt' TEXT NOT NULL,
    'password_hash' TEXT NOT NULL,
    'role' TEXT NOT NULL)"""

    #Query para criar tabela todo 
    qry_tableTodo = """CREATE TABLE IF NOT EXISTS todo 
    ('todo_id' INTEGER PRIMARY KEY AUTOINCREMENT ,
    'task' TEXT NOT NULL,
    'task_descrition' TEXT NOT NULL,
    'created_at' DATE NOT NULL,
    'end_at' DATE NOT NULL,
    'user_Id' INTEGER NOT NULL,
    FOREIGN KEY ('user_id') REFERENCES user('Id'))"""
    
    #Criação de tabelas
    cursor.execute(qry_tableUser)
    cursor.execute(qry_tableTodo)
    #Ativação das FK
    cursor.execute('PRAGMA foreign_keys=ON')

    #Commit da DB
    dBase.commit()

    #Fechar a ligação da DB
    dBase.close()

