from flask import Flask, Response, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin , login_user,login_required, logout_user,current_user
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///file.db'
app.config['SECRET_KEY']='secret'
db=SQLAlchemy(app)
Bootstrap(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

class loginform(FlaskForm):
    username=StringField('Username',validators=[InputRequired(),Length(min=4,max=15)])
    password=PasswordField('Password',validators=[InputRequired(),Length(min=8,max=80)])
    remember=BooleanField('Remember me')

class signupform(FlaskForm):
    email=StringField('Email',validators=[InputRequired(),Email(message='Invalid Email'), Length(max=50)])
    username=StringField('Username',validators=[InputRequired(),Length(min=4,max=15)])
    password=PasswordField('Password',validators=[InputRequired(),Length(min=8,max=80)])
    remember=BooleanField('Remember me')



class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(80))
    file_store=db.relationship('File',backref='user')
    date_created=db.Column(db.DateTime,default=datetime.now)
        

class File(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    img=db.Column(db.Text)
    mimetype=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.now)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/login',methods=['POST','GET'])
def login():
    form=loginform()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user,remember=form.remember.data)
                return redirect('/file')
        flash("Invalid Username or Password")
        return redirect('/login')
    return render_template('login.html',form=form)




@app.route('/signup',methods=['POST','GET'])
def signup():
    form=signupform()
    if form.validate_on_submit():
        hash_pass=generate_password_hash(form.password.data,method='sha256')
        new_user=User(username=form.username.data,email=form.email.data,password=hash_pass)
        db.session.add(new_user)
        db.session.commit()
        flash("New User Created Successfully")

    return render_template('signup.html',form=form)


@app.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login')






@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method=="POST":
        pic=request.files['file']
        filename=secure_filename(pic.filename)
        mimetype=pic.mimetype
        img=File(img=pic.read(),mimetype=mimetype,name=filename,user=current_user)
        try:
            db.session.add(img)
            db.session.commit()
            flash("File Uploaded Successfully")
            return redirect('/file')
            
        except:
            return "ERROR IN UPLOADING"
    else:
        return render_template("storage.html")









@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    name_to_update=File.query.filter_by(id=id).first()
    if request.method=="POST":
        name_to_update.name=request.form['fname']
        try:
            db.session.commit()
            flash("File Name Successfully Updated to "+ name_to_update.name)
            return redirect('/file')
        except:
            flash("Error in renaming")
            return redirect('/file')
    else:
        return render_template("storage.html")

@app.route('/<int:id>')
def getimg(id):
    img=File.query.filter_by(id=id).first()
    if not img:
        return "No Image with that ID",404
    
    return Response(img.img,mimetype=img.mimetype)


     
@app.route('/delete/<int:id>',methods=['POST','GET'])
def delete(id):
    name_to_delete=File.query.get_or_404(id)
    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash("File Successfully Deleted")
        return redirect('/file')
    except:
        flash ("Error in Deleting")
        return redirect('/file')



@app.route('/share/<int:id>',methods=['POST','GET'])
def share(id):
     file_s=File.query.get_or_404(id)
     y=File.query.order_by(File.date_created)
     p=User.query.all()
     if request.method=="POST":
        k=request.form['name']
        t=User.query.filter_by(username=k).first()
        if t:
            db.session.add(File(img=file_s.img,mimetype=file_s.mimetype,name=file_s.name,user_id=t.id))
            db.session.commit()
            flash("File Shared Successfully with " + k)
            return redirect('/file')
        else:
            flash("No user present with this username")
            return redirect('/file')
     return render_template("storage.html")
    





@app.route('/file',methods=['POST','GET'])
@login_required
def file():
    files=File.query.order_by(File.date_created)
    return render_template("storage.html",files=files,name=current_user.username,user=current_user)



if __name__ == '__main__':
    app.run(debug=True)