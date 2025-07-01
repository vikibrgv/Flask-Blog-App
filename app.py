from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"{self.email} - {self.password}"

class Blogdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    des = db.Column(db.String(500), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Blogdata {self.id} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/home')
        else:
            return render_template('loginpage.html', current_page='/', error="Invalid credentials")
    
    return render_template('loginpage.html', current_page='/')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('index.html', current_page='/home')

@app.route('/create_blog', methods=['GET', 'POST'])
def create_blog():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        des = request.form['des']
        new_blog = Blogdata(title=title, des=des)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/showblogs')
    return render_template('create_blog.html', current_page='/create_blog')

@app.route('/showblogs')
def display():
    allblogs = Blogdata.query.all()
    return render_template('showblogs.html', blogs=allblogs, current_page='/showblogs')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/create', methods=['GET', 'POST'])
def createPage():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']

        new_user = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            city=city,
            state=state,
            zip_code=zip_code
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

    return render_template('createAcc.html', current_page='/create')

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

if __name__ == "__main__":
    app.run(debug=True, port=9000)
