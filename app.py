from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logindata'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class students(db.Model):
    id = db.Column('student_id', db.Integer)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50),primary_key = True)
    password = db.Column(db.String(200))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

db.create_all()

@app.route('/', methods = ['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('loginmail')
        passw = request.form.get('loginpass')
        stu = students.query.get(email)
        if stu != None:
            if stu.password == passw:
                session['pass_name'] = stu.name
                return redirect(url_for('home'))
            else:
                error = 'Incorrect Password'
        else:
            error = 'No such Account Exist'
    return render_template('login.html',error = error)

@app.route('/register', methods = ['POST','GET'])
def Register():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('Email')
        passw = request.form.get('Password')
        ss = students.query.get(email)
        print(ss.name)
        if ss == None :
            student = students(name, email, passw)

            db.session.add(student)
            db.session.commit()

            return redirect(url_for('login'))
        else:
            error = 'Email Already Exist'
    return render_template('register.html',error=error )

@app.route('/home')
def home():
    my_var = session.get('pass_name', None)
    return render_template('home.html',var = my_var)

if __name__ == '__main__':
    app.run(debug=True)