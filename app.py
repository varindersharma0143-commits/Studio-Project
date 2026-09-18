from flask import Flask, render_template, request, redirect,flash,url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = "mytodo-secret-key-123"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
 
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
 

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':     
        title = request.form['title']
        desc = request.form['desc']     
      
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
       
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)




@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()   
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
   # print(allTodo)
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # SQLite database se user find karo
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return redirect('/admin')

        else:
            flash('Invalid Username or Password', 'danger')
            return redirect('/login')

    return render_template('login.html')

class UserOld(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
   # name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == 'POST':
       # name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Password does not match", "danger")
            return redirect('/register')

        user = UserOld(
           #name=name,
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful", "success")
        return redirect('/login')

    return render_template('register.html')

@app.route('/index1')
def index1():   
    return render_template('index1.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/photoshop')
def photoshop():
    return render_template('photoshop.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')



class Booking(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    package = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.String(20), nullable=False)
    event_time = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    message = db.Column(db.String(500))
    status = db.Column(db.String(20), default="Pending")
    created_date = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"{self.sno} - {self.name}"

@app.route('/booking', methods=['GET', 'POST'])
def booking():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        service = request.form['service']
        package = request.form['package']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        location = request.form['location']
        message = request.form.get('message', '')

        new_booking = Booking(
            name=name,
            phone=phone,
            email=email,
            service=service,
            package=package,
            event_date=event_date,
            event_time=event_time,
            location=location,
            message=message
        )

        db.session.add(new_booking)
        db.session.commit()

        # Booking number
        booking_no = new_booking.sno

        print("BOOKING SAVED SUCCESSFULLY")
        print("Booking ID:", booking_no)

        # Success message
        flash(
            f"Booking Successful! Your Booking No. is #{booking_no}",
            "success"
        )

        return redirect(url_for('booking'))

    return render_template('booking.html')

 # ContactMessage save db

class ContactMessage(db.Model):

    sno = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    service = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(1000), nullable=False)

    status = db.Column(db.String(20), default="New")

    created_date = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"{self.sno} - {self.name}"

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        service = request.form['service']
        message = request.form['message']

        # Contact message create
        new_message = ContactMessage(
            name=name,
            phone=phone,
            email=email,
            service=service,
            message=message,
            status="New"
        )

        # Database mein save
        db.session.add(new_message)
        db.session.commit()

        # Message number
        message_no = new_message.sno

        print("CONTACT MESSAGE SAVED")
        print("Message No:", message_no)

        flash(
            f"Message Sent Successfully! Your Message No. is #{message_no}",
            "success"
        )

        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/admin')
def admin():

    if not session.get('admin_logged_in'):
        flash(
            "Please login as administrator first.",
            "danger"
        )
        return redirect(url_for('admin_login'))

    page = request.args.get('page', 1, type=int)

    pagination = Booking.query.order_by(
        Booking.sno.desc()
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    bookings = pagination.items

    messages = ContactMessage.query.order_by(
        ContactMessage.sno.desc()
    ).all()

    pending_count = Booking.query.filter_by(
        status="Pending"
    ).count()

    successful_count = Booking.query.filter_by(
        status="Successful"
    ).count()

    return render_template(
        'admin.html',
        bookings=bookings,
        pagination=pagination,
        messages=messages,
        pending_count=pending_count,
        successful_count=successful_count
    )

@app.route('/booking/status/<int:sno>')
def update_booking_status(sno):
    booking = Booking.query.filter_by(sno=sno).first()
    if booking:
        booking.status = "Successful"
        db.session.commit()
        flash(
            f"Booking #{sno} status updated successfully!",
            "success"
        )
    return redirect(url_for('admin'))



class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column( db.String(100),nullable=False,unique=True)

    email = db.Column(db.String(100),nullable=False)

    password = db.Column(db.String(100),nullable=False)

    role = db.Column(db.String(20),nullable=False,default="User")

    def __repr__(self):
        return f"{self.sno} - {self.username}"

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # SQLite database se user find karo
        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.password == password and user.role == "Admin":

            session['admin_logged_in'] = True
            session['admin_username'] = user.username
            session['admin_user_id'] = user.sno

            flash(
                "Admin login successful!",
                "success"
            )

            return redirect(url_for('admin'))

        else:

            flash(
                "Invalid Admin Username or Password!",
                "danger"
            )

            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')


# Admin User
@app.route('/admin/users')
def admin_users():

    if not session.get('admin_logged_in'):
        flash("Please login as administrator first.", "danger")
        return redirect(url_for('admin_login'))

    users = User.query.order_by(User.sno.desc()).all()

    return render_template(
        'admin_users.html',
        users=users
    )

@app.route('/admin/users/delete/<int:sno>')
def delete_user(sno):

    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    user = User.query.filter_by(sno=sno).first()

    if user:

        # Current admin ko delete nahi karne dena
        if user.sno == session.get('admin_user_id'):
            flash("You cannot delete your current admin account!", "danger")
            return redirect(url_for('admin_users'))

        db.session.delete(user)
        db.session.commit()

        flash("User deleted successfully!", "success")

    return redirect(url_for('admin_users'))

# Add User
@app.route('/admin/users/add', methods=['GET', 'POST'])
def add_user():

    if not session.get('admin_logged_in'):
        flash("Please login as administrator first.", "danger")
        return redirect(url_for('admin_login'))

    if request.method == 'POST':

        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        role = request.form['role']

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            flash("Username already exists!", "danger")
            return redirect(url_for('add_user'))

        user = User(
            username=username,
            email=email,
            password=password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        flash("User added successfully!", "success")

        return redirect(url_for('admin_users'))

    return render_template('add_user.html')

@app.route('/admin/users/edit/<int:sno>', methods=['GET', 'POST'])
def edit_user(sno):

    if not session.get('admin_logged_in'):
        flash("Please login as administrator first.", "danger")
        return redirect(url_for('admin_login'))

    user = User.query.filter_by(sno=sno).first()

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for('admin_users'))

    if request.method == 'POST':

        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        role = request.form['role']

        # Check duplicate username
        existing_user = User.query.filter(
            User.username == username,
            User.sno != sno
        ).first()

        if existing_user:
            flash("Username already exists!", "danger")
            return redirect(url_for('edit_user', sno=sno))

        user.username = username
        user.email = email
        user.role = role

        # Password blank hai to old password rahega
        if password.strip():
            user.password = password

        db.session.commit()

        flash("User updated successfully!", "success")

        return redirect(url_for('admin_users'))

    return render_template(
        'edit_user.html',
        user=user
    )

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
       app.run(debug=True, port=8001, use_reloader=False)