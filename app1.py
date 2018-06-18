from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


app1 = Flask(__name__)
app1.config['SECRET_KEY'] = 'bhatgavhjjk'
app1.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:helloitsme@localhost:5432/azureDB'

db = SQLAlchemy(app1)
login_manager = LoginManager(app1)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please choose another')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Please choose another')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


posts = [
    {
        'author': 'Bhargav',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Pranav',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 20, 2018'
    }
]


@app1.route('/')
@app1.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app1.route('/about/')
def about():
    return render_template('about.html', title='About')


@app1.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app1.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check your email/password','danger')
    return render_template('login.html', title='Register', form=form)



if __name__ == '__main__':
    app1.run(debug=True)