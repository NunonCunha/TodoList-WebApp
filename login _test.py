import hashlib
import os
import random
import sqlite3 as sql
import string
from datetime import timedelta
from flask import Flask, redirect, render_template, request, session, url_for
from createDB import create_DB

#Variavel path para abstrair o server side da localização dos ficheiros
path = 'db_web.db'

#Variavel bool que indica se o ficheiro existe
fileExist = os.path.exists(path)

#Valida o resultado da variavel, se for negativo, cria a basedados
if not fileExist:
    create_DB()

def insertUser(user,salt,psw,role):
    dbase = sql.connect("db_web.db")
    cursor = dbase.cursor()
    cursor.execute("INSERT INTO utilizadores(User,Salt,Password,role) VALUES (?,?,?,?)", (user, salt,psw,role))
    dbase.commit()

def findrole():
    dbase = sql.connect("db_web.db")
    cursor = dbase.cursor()
    cursor.execute("SELECT role FROM utilizadores")
    dado=cursor.fetchone()
    return dado

def getRegister():
    dbase = sql.connect("db_web.db")
    dbase.row_factory=sql.Row
    cursor = dbase.cursor()
    cursor.execute("SELECT * FROM utilizadores")
    dado=cursor.fetchall()
    return dado

def finduser(user):
    dbase = sql.connect("db_web.db")
    cursor = dbase.cursor()
    cursor.execute("SELECT * FROM utilizadores WHERE User=?",(user,))
    dado=cursor.fetchone()
    return dado

def delete_user(id):
    dbase=sql.connect("db_web.db")
    cursor=dbase.cursor()
    cursor.execute("DELETE FROM utilizadores WHERE Id=?",(id,))
    dbase.commit()

#Metodo random que retorna uma string aleatorio de 16 caracteres
def rand():
    chars = string.ascii_letters+string.digits+string.punctuation
    return random.choices(chars, k=16)

#Metodo para verificar se o servidor tem um administrador
#Retorna um boolean
def checkAdmin():
    Roles = findrole()
    if Roles is None:
        return False
    elif 'Admin' in Roles:
        return True
    else:
        return False

def isAdmin(user):
    dbase = sql.connect("db_web.db")
    cursor = dbase.cursor()
    cursor.execute("SELECT role FROM utilizadores WHERE User=?",(user,))
    dado=cursor.fetchone()
    if "Admin" in dado:
        return True
    else:
        return False

#Metodo para gerar um salt aleatoriamente e gera um hash com a combinação da password e salt
#Retorna Tupla com strings
def securityProcess(password):
    salt = ''.join(rand())
    hash = hashlib.sha256((salt+password).encode())
    #Aplicada função hexdigest, para converter o hash em hexa para que a DB possa aceitar
    return salt,hash.hexdigest()

#Verifica de a DB tem um administrador, caso não tenha pede para introduzir dados para criar um administrador
while checkAdmin() == False:
    print("Creating admin:")
    name = input("Enter username: ")
    psw = input("Enter password: ")
    salt, hash256 = securityProcess(psw)
    role = "Admin"
    insertUser(name,salt,hash256,role)
    os.system('cls')

app = Flask(__name__)
app.secret_key=rand()

#Metodo para verificar a password passando o salt, hash e password
#Retorna boolean
def verificaPassword(salt, hash, password):
    hexa = (salt+password).encode()
    return (hashlib.sha256(hexa).hexdigest() == hash)

#Metodo para verifica se o utilizador introduziu as credenciais corretamente
#Retorna boolean
def verificaLogin(username, password):
    user = finduser(username)
    if user is None:
        return False
    elif username in user:
        check = verificaPassword(user[2], user[3],password)
        if check == True:
            return True
        else:
            return False
    else:
        False

#Metedo para verificar se o utilizador existe na DB
#Retorna boolean
def verificaUser(username):
    user = finduser(username)
    if user is None:
        return False
    elif username in user:
        return True
    else:
        return False

#Metodo para apagar utilizador da DB
#Retorna boolean
def apagarUser(username):
    user = finduser(username)
    if user is None:
        return False
    elif 'Bussiness' in user :
        delete_user(user[0])
        return True
    else:
        return False

#Define um timeout antes da request ao servidor
@app.before_request
def session_timetout():
    app.permanent_session_lifetime = timedelta(minutes=5)

#Condições para pagina de login
##Sempre que a url seja só login sem nenhum metodo retorna o html do login
##Se o metodo da request for post, verifica o login
###Caso verdade redireciona para metodo Principal
###Caso mentira apresenta o template do login e retorna uma condição de erro ao template
@app.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        if verificaLogin(request.form['username'],request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('principal'))
        else:
            error = True
            return render_template('login.html', error=error)
    return render_template('login.html')

#Condições para a pagina de Registo
##Sempre que a url seja só login sem nenhum metodo retorna o html do registo
##Se o metodo da request for post, verifica o user existe na DB
###Caso mentira cria um novo utilizador com os dados introduzidos e redireciona para a pagina principal passando um argumento
###Caso verdade redireciona para metodo erro
@app.route("/registo", methods=['GET', 'POST'])
def registo():
    if request.method == 'POST':    
        username = request.form['username']
        password = request.form['password']
        role="Bussiness"
        if verificaUser(username) == False:
            salt, hash256 = securityProcess(password)
            insertUser(username,salt,hash256,role)
            session.clear()
            session['username'] = username
            return redirect(url_for('principal', new_User=True))
        else:
            return redirect(url_for('erro'))
    else:
        return render_template('registo.html')

#Quando o url é de erro apresenta o template de erro
@app.route("/registo/erro")
def erro():
    return render_template('erro.html')

#Condições para a pagina principal
##Verifica se existe um user na sessão
### Caso verdade verifica condições tais como "Novo utilizador" passa valor no html, utilizador é administrador apresenta DB e deixa apagar users, utilizador normal apresenta html
### Caso mentira redireciona para a pagina de login
@app.route("/",  methods=['GET', 'POST'])
def principal():
    if 'username' in session:
        new_User=request.args.get('new_User')
        if new_User == "True":
            return render_template('main.html', user = session['username'], new_User = True)
        elif isAdmin(session['username']) == True:
            data = getRegister()
            if request.method == 'POST':
                user = request.form['deluser']
                adminDelete = apagarUser(user)
                data = getRegister()
                return render_template('main.html', user = session['username'], data = data, adminDelete = adminDelete)
            else:
                return render_template('main.html', user = session['username'], data = data)
        else:
            return render_template('main.html', user = session['username'])
    else:
        return redirect(url_for('login'))

### Aplicação corre com possibilidade de debug e em contexto de ssl com certificados locais
if __name__ == "__main__":
    app.run(debug=True, ssl_context=('cert.crt','cert.key'))
