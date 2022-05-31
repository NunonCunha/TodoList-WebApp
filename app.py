import hashlib
import os
import random
import sqlite3 as sql
import string
from datetime import timedelta
from flask import Flask, redirect, render_template, request, session, url_for
from createDB import create_DB

#Variavel path para abstrair o server side da localização dos ficheiros
path = 'db_todoApp.db'

#Variavel bool que indica se o ficheiro existe
fileExist = os.path.exists(path)

#Valida o resultado da variavel, se for negativo, cria a basedados
if not fileExist:
    create_DB()

#Metodo para introduzir um novo utilizador na DB (Create)
def insertUser(fname,lname,mail,salt,psw,role):
    dbase = sql.connect("db_todoApp.db")
    cursor = dbase.cursor()
    cursor.execute("""INSERT INTO user(first_name, last_name, email, salt, password_hash, role)
    VALUES (?,?,?,?,?,?)""",(fname,lname,mail,salt,psw,role))
    dbase.commit()

#Metodo para retornar uma tupla da query (Read)
##Return tupla com a role da tabela user
def findrole():
    dbase = sql.connect("db_todoApp.db")
    cursor = dbase.cursor()
    cursor.execute("SELECT role FROM user")
    dado=cursor.fetchone()
    return dado

#Metodo para retornar um dicionario da query (Read)
##Return dicionario da tabela user
def getRegister():
    dbase = sql.connect("db_todoApp.db")
    dbase.row_factory=sql.Row
    cursor = dbase.cursor()
    cursor.execute("SELECT * FROM user")
    dado=cursor.fetchall()
    return dado

#Metodo para retornar um dicionario da query (Read)
##Return tupla da tabela user onde o argumento passado foi o mail
def findmail(mail):
    dbase = sql.connect("db_todoApp.db")
    cursor = dbase.cursor()
    cursor.execute("SELECT * FROM user WHERE email=?",(mail,))
    dado=cursor.fetchone()
    return dado

#Metodo para eliminar utilizador na DB (Delete)
def delete_user(id):
    dbase=sql.connect("db_todoApp.db")
    cursor=dbase.cursor()
    cursor.execute("DELETE FROM user WHERE id=?",(id,))
    dbase.commit()

#Metodo para verificar se a role do argumento passado é admin (Read)
##Return boolean
def isAdmin(mail):
    dbase = sql.connect("db_todoApp.db")
    cursor = dbase.cursor()
    cursor.execute("SELECT role FROM user WHERE email=?",(mail,))
    dado=cursor.fetchone()
    if "Admin" in dado:
        return True
    else:
        return False

#Metodo para retirar elementos necessarios da Db atravez do argumento passado (Read)
##Return tupla com nome do utilizador e mail
def getUname(mail):
    dbase = sql.connect("db_todoApp.db")
    cursor = dbase.cursor()
    cursor.execute("SELECT first_name , last_name FROM user WHERE email=?",(mail,))
    dado=cursor.fetchone()
    fullName = dado[0] + ' ' + dado[1]
    return fullName , mail

#Metodo para retirar o id da table da Db atravez do argumento passado (Read)
##Return int
def getId(mail):
    dbase = sql.connect("db_todoApp.db")
    cursor = dbase.cursor()
    cursor.execute("SELECT id FROM user WHERE email=?",(mail,))
    dado=cursor.fetchone()
    return dado[0]

#Metodo para introduzir um nova task na DB (Create)
def creatTodo(task,description,start,end,userId):
    dbase = sql.connect("db_todoApp.db")
    cursor = dbase.cursor()
    cursor.execute("""INSERT INTO todo(task, task_descrition, created_at, end_at, user_Id)
    VALUES (?,?,?,?,?)""",(task,description,start,end,userId))
    dbase.commit()

#Metodo para retornar um dicionario da query (Read)
##Return dicionario da tabela todo pelo id do user da sessão
def gettodobyId(id):
    dbase = sql.connect("db_todoApp.db")
    dbase.row_factory=sql.Row
    cursor = dbase.cursor()
    cursor.execute("SELECT * FROM todo WHERE user_Id=?",(id,))
    dado=cursor.fetchall()
    return dado

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

#Metodo para gerar um salt aleatoriamente e gera um hash com a combinação da password e salt
#Retorna Tupla com strings
def securityProcess(password):
    salt = ''.join(rand())
    hash = hashlib.sha256((salt+password).encode())
    #Aplicada função hexdigest, para converter o hash em hexa para que a DB possa aceitar
    return salt,hash.hexdigest()

#Verifica de a DB tem um administrador, caso não tenha pede para introduzir dados para criar um administrador
mail = ""
psw = ""
while checkAdmin() == False:
    os.system('cls')
    print("###___Creating admin___###")
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    if len(mail) >= 6:
        if len(psw) >= 12:
            salt, hash256 = securityProcess(psw)
            role = "Admin"
            insertUser(fname,lname,mail,salt,hash256,role)
            os.system('cls')
        else:
            print("Choose a password with min 12 characters long")
            psw = input("Enter password: ")
    else:
        print("Choose a username with min 6 characters long")
        name = input("Enter username: ")

app = Flask(__name__)
app.secret_key=rand()

#Metodo para verificar a password passando o salt, hash e password
#Retorna boolean
def verificaPassword(salt, hash, password):
    hexa = (salt+password).encode()
    return (hashlib.sha256(hexa).hexdigest() == hash)

#Metodo para verifica se o utilizador introduziu as credenciais corretamente
#Retorna boolean
def verificaLogin(email, password):
    user = findmail(email)
    if user is None:
        return False
    elif email in user:
        check = verificaPassword(user[4], user[5],password)
        if check == True:
            return True
        else:
            return False
    else:
        False

#Metedo para verificar se o utilizador existe na DB
#Retorna boolean
def verificaMail(email):
    user = findmail(email)
    if user is None:
        return False
    elif email in user:
        return True
    else:
        return False

#Metodo para apagar utilizador da DB
#Retorna boolean
def apagarUser(email):
    user = findmail(email)
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
        if verificaLogin(request.form['email'],request.form['password']):
            session['name'] = getUname(request.form['email'])
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
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        role="Bussiness"
        if verificaMail(email) == False:
            salt, hash256 = securityProcess(password)
            insertUser(fname,lname,email,salt,hash256,role)
            session.clear()
            session['name'] = getUname(email)
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
    if 'name' in session:
        fullName = session['name'][0]
        mail=session['name'][1]
        new_User=request.args.get('new_User')
        todo = gettodobyId(getId(mail))
        if new_User == "True":
            return render_template('main.html', user = fullName, new_User = True)
        elif isAdmin(mail) == True:
            data = getRegister()
            if request.method == 'POST':
                user = request.form['deluser']
                adminDelete = apagarUser(user)
                data = getRegister()
                return render_template('main.html', user = fullName, data = data, adminDelete = adminDelete)
            else:
                return render_template('main.html', user = fullName, data = data)
        else:
            return render_template('main.html', user = fullName , todo = todo)
    else:
        return redirect(url_for('login'))

#Condições para a pagina principal
##Verifica o metodo do render
### Se não for post apresenta o html e passa o user da session como argumento
### Caso o metodo seja POST recolhe os elementos necessarios para criar task e dá feed back ao utilizador
@app.route("/todo",  methods=['GET', 'POST'])
def todoCreate():
    fullName = session['name'][0]
    mail=session['name'][1]
    if request.method == 'POST':
        task = request.form['todo']
        description = request.form['todoDescription']
        start = request.form['startAt']
        end = request.form['endAt']
        userId=getId(mail)
        creatTodo(task,description,start,end,userId)
        return render_template('todo.html', user = fullName , taskCreat = True)
    else:
        return render_template('todo.html', user = fullName)


### Aplicação corre com possibilidade de debug e em contexto de ssl com certificados locais
if __name__ == "__main__":
    app.run(debug=True, ssl_context=('cert.crt','cert.key'))
