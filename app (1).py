from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField,SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import pandas as pd
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\\Users\\tejas\\Desktop\\tejack_pbl\\database.db'
app.config['SQLALCHEMY_BINDS'] = {'three': r'sqlite:///C:\\Users\\tejas\\Desktop\\tejack_pbl\\Medical.db',
                                  'two': r'sqlite:///C:\\Users\\tejas\\Desktop\\tejack_pbl\\Details.db',
                                  'one': r'sqlite:///C:\\Users\\tejas\\Desktop\\tejack_pbl\\database.db'}
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# DATABASE CONNECTION

# DATABASE CONNECTION

class User(UserMixin, db.Model):
    __bind_key__ ='one'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])



class Details(db.Model):
    __bind_key__ ='two'

    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(70))
    #Locality = db.Column(db.String(70))
    Course = db.Column(db.String(100))
    Fees = db.Column(db.Integer)
    Exam = db.Column(db.String(70))
    Affiliation = db.Column(db.String(70))
    New_locality = db.Column(db.String(70))
    
    

    def __reprc__(self):
        return '{}'.format(self.Name)

    def __reprl__(self):
        return '{}'.format(self.New_locality)

    def __reprco__(self):
        return '{}'.format(self.Course)

    def __repre__(self):
        return '{}'.format(self.Exam) 

def Details_query():
    return Details.query #to fire querry

class Mdetails(db.Model):
    __bind_key__ ='three'

    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(70))
    #Locality = db.Column(db.String(70))
    Course = db.Column(db.String(100))
    Fees = db.Column(db.Integer)
    Exam = db.Column(db.String(70))
    Affiliation = db.Column(db.String(70))
    New_locality = db.Column(db.String(70))
    
    

    def __reprc__(self):
        return '{}'.format(self.Name)

    def __reprl__(self):
        return '{}'.format(self.New_locality)

    def __reprco__(self):
        return '{}'.format(self.Course)

    def __repre__(self):
        return '{}'.format(self.Exam)

def Mdetails_query():
    return Mdetails.query


class ChoiceForm(FlaskForm):
   
    stream = SelectField(choices=[('Engineering','Engineering'),('Medical','Medical')] )
    college = QuerySelectField(query_factory=Details_query, allow_blank=True, get_label='Name')
    course = QuerySelectField(query_factory=Details_query, allow_blank=True, get_label='Course')
    locality = QuerySelectField(query_factory=Details_query, allow_blank=True, get_label='New_locality')
    exam = QuerySelectField(query_factory=Details_query, allow_blank=True, get_label='Exam')


class ChoiceForm2(FlaskForm):
   
    stream = SelectField(choices=[('Engineering','Engineering'),('Medical','Medical')] )
    college = QuerySelectField(query_factory=Mdetails_query, allow_blank=True, get_label='Name')
    course = QuerySelectField(query_factory=Mdetails_query, allow_blank=True, get_label='Course')
    locality = QuerySelectField(query_factory=Mdetails_query, allow_blank=True, get_label='New_locality')
    exam = QuerySelectField(query_factory=Mdetails_query, allow_blank=True, get_label='Exam')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('index.html')
        #return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    '''form = ChoiceForm()
   
    form.college.query = db.session.query(Details).distinct(Details.Name).group_by(Details.Name)
    form.locality.query = db.session.query(Details).distinct(Details.Locality).group_by(Details.Locality)
    form.course.query = db.session.query(Details).distinct(Details.Course).group_by(Details.Course)
    form.exam.query = db.session.query(Details).distinct(Details.Exam).group_by(Details.Exam)
    if form.validate_on_submit():
        return render_template('col_disp.html')'''
    return render_template('dashboard.html', name=current_user.username)



@app.route('/engineeringsubmit' ,methods=['GET', 'POST'])
def engineeringsubmit():
    form = ChoiceForm()


    if request.method=="POST":
            col=None
            loc=None
            loc=None
            examm=None
            cou=None
            
            if form.college.data!=None:
                col=form.college.data.__reprc__()
            if form.locality.data!=None:
                loc=form.locality.data.__reprl__()
            if form.exam.data!=None:
                examm=form.exam.data.__repre__()
            if form.course.data!=None:
                cou=form.course.data.__reprco__()
           
            conne = sqlite3.connect("C:\\Users\\tejas\\Desktop\\tejack_pbl\\Details.db")

            if col!=None:
                final = pd.read_sql_query("""Select * from Details where Name=='"""+col+"""'""",conne)
                #a=list(final.iloc[:,:])
                #College_Name=list(final['Name'])
                #College_Locality=list(final['Locality'])
                #College_Course=list(final['Course'])
                #College_Fees=list(final['Fees'])
                #College_Exam=list(final['Exam'])
                #College_Facilities=list(final['Facilities'])
                (n,m)=final.shape
                l=[]
                for i in range(n):
                    l.append(list(final.iloc[i]))
                return render_template('result.html', a=l)#College_Name=College_Name,College_Locality=College_Locality,College_Course=College_Course,College_Fees=College_Fees,College_Exam=College_Exam,College_Facilities=College_Facilities'<html><h1>{}</h1></html>'.format(final)
            elif (loc!=None and cou!=None ):
                final = pd.read_sql_query("""Select * from Details where New_locality LIKE '%"""+ loc+"""%' and Course LIKE'%"""+ cou +"""%'""",conne)
                #College_Name=list(final['Name'])
                #College_Locality=list(final['Locality'])
                #College_Course=list(final['Course'])
                #College_Fees=list(final['Fees'])
                #College_Exam=list(final['Exam'])
                #College_Facilities=list(final['Facilities'])
                (n,m)=final.shape
                l=[]
                for i in range(n):
                    l.append(list(final.iloc[i]))
                return render_template('result.html',a=l)#'<html><h1>{}</h1></html>'.format(final)
                #return '<html><h1>{}</h1></html>'.format(final)
            else:
                return '<html><h1>Please select either of option</h1></html>'
            conn.close()
            #return '<html><h1>{}</h1></html>'.format(final)
            #got user input and fired querry got result in data frame
            
    return render_template('index.html', form=form)

@app.route('/medicalsubmit' ,methods=['GET', 'POST'])
def medicalsubmit():
    form = ChoiceForm2()


    if request.method=="POST":
            col=None
            loc=None
            #loc=None
            #examm=None
            cou=None
            if form.college.data!=None:
                col=form.college.data.__reprc__()
            if form.locality.data!=None:
                loc=form.locality.data.__reprl__()
            '''if form.exam.data!=None:
                examm=form.exam.data.__repre__()'''
            if form.course.data!=None:
                cou=form.course.data.__reprco__()
           
            connm = sqlite3.connect("C:\\Users\\tejas\\Desktop\\tejack_pbl\\Medical.db")
            if col!=None:
                final = pd.read_sql_query("""Select * from Mdetails where Name=='"""+col+"""'""",connm)
                #College_Name=list(final['Name'])
                #College_Locality=list(final['Locality'])
                #College_Course=list(final['Course'])
                #College_Fees=list(final['Fees'])
                #College_Exam=list(final['Exam'])
                #College_Facilities=list(final['Facilities'])
                (n,m)=final.shape
                l=[]
                for i in range(n):
                    l.append(list(final.iloc[i]))
                return render_template('result.html', a=l)#'<html><h1>{}</h1></html>'.format(final)
                #return '<html><h1>{}</h1></html>'.format(final)
            elif (loc!=None and cou!=None ):
                final = pd.read_sql_query("""Select * from Mdetails where New_locality=='"""+loc+"""' and Course=='"""+cou+"""'""",connm)
                #College_Name=list(final['Name'])
                #College_Locality=list(final['Locality'])
                #College_Course=list(final['Course'])
                #College_Fees=list(final['Fees'])
                #College_Exam=list(final['Exam'])
                #College_Facilities=list(final['Facilities'])
                (n,m)=final.shape
                l=[]
                for i in range(n):
                    l.append(list(final.iloc[i]))
                return render_template('result.html', a=l)#'<html><h1>{}</h1></html>'.format(final)
                #return '<html><h1>{}</h1></html>'.format(final)
            else:
                return '<html><h1>Please select either of option</h1></html>'
            conn.close()
            #return '<html><h1>{}</h1></html>'.format(final)
            #got user input and fired querry got result in data frame
            
    return render_template('index.html', form=form)
   

@app.route('/engineeringcolleges', methods=['GET', 'POST'])
def engineeringcolleges():
    form = ChoiceForm()
    form.college.query = db.session.query(Details).distinct(Details.Name).group_by(Details.Name)
    form.locality.query = db.session.query(Details).distinct(Details.New_locality).group_by(Details.New_locality)
    form.course.query = db.session.query(Details).distinct(Details.Course).group_by(Details.Course)
    form.exam.query = db.session.query(Details).distinct(Details.Exam).group_by(Details.Exam)

    return render_template('col_disp.html', form=form)

@app.route('/medicalcolleges', methods=['GET', 'POST'])
def medicalcolleges():
    form = ChoiceForm2()
    form.college.query = db.session.query(Mdetails).distinct(Mdetails.Name).group_by(Mdetails.Name)
    form.locality.query = db.session.query(Mdetails).distinct(Mdetails.New_locality).group_by(Mdetails.New_locality)
    form.course.query = db.session.query(Mdetails).distinct(Mdetails.Course).group_by(Mdetails.Course)
    form.exam.query = db.session.query(Mdetails).distinct(Mdetails.Exam).group_by(Mdetails.Exam)

    return render_template('medical_disp.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)