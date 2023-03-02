from datetime import datetime
from wsgiref.validate import validator
from flask import Flask, flash, redirect, render_template, session, request, url_for
from flask_bootstrap import Bootstrap4
from flask_moment import Moment
import pytz
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, DateField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap4(app)
moment = Moment(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # check it out, this exists in a different table as a foreign key
    # should name the variable the same as the __tablename__ of the other table
    # 1st parameter is the class name of the child (ie: User)
    # 2nd parameter is the class name of the parent (ie: role)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # check it out, a foreign key
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    dob = db.Column(db.String(64))
    nationality = db.Column(db.String(64))
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))

    def __repr__(self):
        return '<Account %r>' % self.name
class Gender(db.Model):
    __tablename__ = 'genders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    accounts = db.relationship('Account', backref='gender')

    def __repr__(self):
        return '<Gender %r>' % self.name

class NameForm2(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    # the validators Email() does not work, but EmailField does
    email = EmailField('What is your email?', validators=[DataRequired()])
    password = PasswordField("Input your password:", validators=[DataRequired()])
    dob = DateField("Input your Date of Birth", validators=[DataRequired()])
    nationality = StringField("What is your nationality?", validators=[DataRequired()])
    # gender = SelectField("Select:", choices=[(0, "male"), (1, "female"), (2, "none")], validate_choice=True)
    gender = SelectField("Select:", choices=[], validate_choice=True)

    submit = SubmitField('Submit')


# inhert the FlaskForm, in the html file you just need to call {{ render_form(form) }}
# it will call this NameForm cause (1) it was inhert, (2) the "/" route return the NameForm
class NameForm(FlaskForm):
    # define what field is needed in the form
    # validators=[DataRequired()] is to have data b4 submit, will be checked by form.validate_on_submit()
    # there are also other validators: Email, Length,... check the slide for more
    name = StringField('What is your name?', validators=[DataRequired()])
    # you can add more field to this
    # petname = StringField('What is your petname?', validators=[DataRequired()])
    # the submit button
    submit = SubmitField('Submit')


# the "/" route has 2 http methods "get" and "post" (it is "get" by default)
@app.route("/", methods=['GET', 'POST'])
def index():
    # return "<h1>Hello World</h1>"
    # current_time = datetime.utcnow()
    # return render_template("index.html", current_time=current_time)

    # name = None
    # petname = None
    # # create new instance of the form via call NameForm()
    # form = NameForm()
    # # remember validators=[DataRequired()], this is were they linked up
    # if form.validate_on_submit():
    #     # need to have defined name variable in the NameForm first
    #     # append the data from form.name.data to name variable
    #     name = form.name.data
    #     # remember flash in nodejs, it retains the value of this field after submit, this is the same
    #     # technically, you dont need this, it will automatically append to that field in the form
    #     form.name.data = name
    #     # you can also do this, it will erase after submit
    #     # form.name.data = None
    #     petname = form.petname.data
    #     form.petname.name = None
    # # at last, return the form, why?, remember the GET method, it will load (with and without data)
    # return render_template('index.html', form=form, name=name, petname=petname, current_time=datetime.utcnow())

    form = NameForm()
    # validate information 1st
    if form.validate_on_submit():
        # get the current user from the field form
        current_user = User.query.filter_by(username=form.name.data).first()
        # if user does not exist, add them to db
        if current_user is None:
            print("empty")
            current_user = User(username=form.name.data)
            db.session.add(current_user)
            db.session.commit()
            session['known'] = False
        # if user exist in db
        else:
            print("existed")
            session['known'] = True
        # implementation of flash message
        # in the base.html add a jinja template as well
        if session.get('name') is not None and session.get('name') != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        # finally redirect to the index page by calling function route index by provoke the url_for('index')
        return redirect(url_for('index'))
    # information validate failed then render_template (the form is empty of course)
    # or GET methods will return render_templates
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known'), current_time=datetime.utcnow())



@app.route("/user/<name>")
def user(name):
    # return "<h1>Hello, {}!<3</h1>".format(name)
    page = request.args.get('page')
    number = request.args.get('number')
    print("Page is: ", page, " - Number is: ", number)
    return render_template("user.html", name=name, page=page, number=number)


@app.route('/get-date-time/<string:region_code>/<string:city_code>')
def getdate(region_code, city_code):
    # current_time = datetime.utcnow()
    # print(current_time)
    time_string = region_code.title() + "/" + city_code.title()
    if time_string in pytz.all_timezones:
        current_time = datetime.now(pytz.timezone(time_string))
        print(True)
    else:
        current_time = datetime.utcnow()
        print(False)
    return render_template('ex4.html', number=4, current_time=current_time)


@app.route("/account", methods=["GET", "POST"])
def account():
    name = None
    email = None
    password = None
    dob = None
    nationality = None
    gender = None

    form = NameForm2()
    # remember this?, gender = SelectField("Select:", choices=[], validate_choice=True)
    form.gender.choices = [(c.id, c.name) for c in Gender.query.all()]
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        dob = form.dob.data
        nationality = form.nationality.data
        gender = form.gender.data
        if len(password) < 6:
            flash('Password is not long enough!')
            return render_template('register.html', form=form, current_time=datetime.utcnow())
        
        current_account = Account.query.filter_by(email=form.email.data).first()
        if current_account is None:
            print("empty account")
            current_account = Account(name=name, email=email, password=password, dob=dob, nationality=nationality, gender_id=gender)
            # db.session.commit()

            current_user = User.query.filter_by(username=form.name.data).first()
            if current_user is None:
                user_role = Role(name='User')
                current_user = User(username=form.name.data, role_id=1)
                
                db.session.add(current_account)
                db.session.add(current_user)
                db.session.commit()
                session['known'] = False
            else:
                flash('Looks like you existed!')
                session['known'] = True
        else:
            print("existed")
            flash('Looks like you existed!')
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    # print(name, email, password, dob, nationality, gender)
    # GET methods will return render_templates
    return render_template('register.html', form=form, current_time=datetime.utcnow())

# ------------------------------------------------------------------------------------------------


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(505)
def internal_server_error(e):
    return render_template("505.html"), 505

