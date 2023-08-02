from flask import Flask, render_template, request,flash,session,redirect,url_for
from flask_mysqldb import MySQL

app =Flask (__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'organic_food'
app.config['SESSION_TYPE'] = ''
app.config['SECRET_KEY'] = 'super secret key'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html");

@app.route('/logout',methods=['POST','GET'])
def logout():
    return render_template("index.html");

@app.route('/logoutuser',methods=['POST','GET'])
def logoutuser():
    session.pop('username', None)
    return render_template("index.html");

@app.route('/payment', methods=['POST','GET'])
def payment():
    status = True
    if request.method == "POST":
        details = request.form
        cno = details['cno']
        cname = details['cname']
        dateexp = details['dateexp']
        cvv = details['cvv']
        pprice = details['pprice']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO payment(cno, cname, expdate, cvv, price) VALUES (%s, %s, %s, %s, %s)",
                    (cno, cname, dateexp, cvv, pprice))
        mysql.connection.commit()
        cur.close()
        return render_template('user_view_booking.html');
    else:
        return render_template("payment.html");

@app.route('/adminlogin', methods=['POST','GET'])
def adminlogin():
    status = True
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("select * from adminlogin where username=%s and password=%s", (email, password))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True
            session['username1'] = email
            flash('Login Successfully', 'success')
            return redirect(url_for('enquery'))
            # return render_template('dashboard.html')
        else:
            flash('Invalid Login. Try Again', 'danger')
    return render_template("admin_login.html");

@app.route('/userlogin', methods=['POST','GET'])
def userlogin():
    status = True
    if request.method == 'POST':
        details=request.form
        email = details["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("select * from user_signup where email=%s and password=%s", (email, password))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True
            session['username'] = email

            flash('Login Successfully', 'success')
            return redirect(url_for('viewproduct'))
            # return render_template('dashboard.html')
        else:
            flash('Invalid Login. Try Again', 'danger')
    return render_template("user_login.html");


@app.route('/usersignup', methods=['POST','GET'])
def usersignup():
    status = True
    if request.method == 'POST':
        details=request.form
        email = details["email"]
        #password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("select * from user_signup where email=%s", ([email]))
        data = cur.fetchone()
        if data:
            return "<script>alert('Sorry user already exists')</script>"+render_template('user_signup.html');
        else:
            if request.method == "POST":
                details = request.form
                name = details['name']
                mobile_no = details['mobileno']
                email = details['email']
                password = details['password']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO user_signup(name, mobile_no, email, password) VALUES (%s, %s, %s, %s)",
                            (name, mobile_no, email, password))
                mysql.connection.commit()
                cur.close()
                return render_template('user_login.html');
            else:
                return render_template('user_signup.html');

    else:
        return render_template('user_signup.html');


@app.route('/addproduct',methods=['POST','GET'])
def addproduct():
    status=True
    if request.method == "POST":
            details = request.form
            pname = details['pname']
            file = 'static/images/'+details['file']
            date = details['date']
            ctype = details['ctype']
            pprice = details['pprice']

            cur = mysql.connection.cursor()

            cur.execute("INSERT INTO add_product(pname, file, date, ctype, pprice) VALUES (%s, %s, %s, %s, %s)", (pname, file, date, ctype, pprice))
            mysql.connection.commit()
            cur.close()
            return render_template('add_product.html  ');
    else:
     return render_template('add_product.html');

@app.route('/viewproduct')
def viewproduct():
    cur = mysql.connection.cursor()
    cur.execute("select * from add_product")
    data3 = cur.fetchall()
    return render_template("viewproduct.html", value=data3);

@app.route('/userbookings', methods=['POST','GET'])
def userbookings():
    status = True
    if request.method == "POST":
        details = request.form
        return render_template('user_booking.html', **details);
    else:
        return render_template('user_booking.html');

@app.route('/enquery', methods=['POST','GET'])
def enquery():
    cur = mysql.connection.cursor()
    cur.execute("select * from bookings")
    data = cur.fetchall()
    return render_template("enquery_order_list.html", value=data);

@app.route('/userviewbooking', methods=['POST','GET'])
def userviewbooking():
    cur = mysql.connection.cursor()
    cur.execute("select * from bookings where email=%s",[session['username']])
    data = cur.fetchall()
    return render_template("user_view_booking.html", value=data);

@app.route('/viewusers', methods=['POST','GET'])
def viewusers():

    cur = mysql.connection.cursor()
    cur.execute("select * from user_signup")
    data = cur.fetchall()
    return render_template("view_users.html", value=data);

@app.route('/viewproductlist', methods=['POST','GET'])
def viewproductlist():
    cur = mysql.connection.cursor()
    cur.execute("select * from add_product")
    data = cur.fetchall()
    return render_template("viewproductlist.html", value=data);

@app.route('/moredetails', methods=['POST','GET'])
def moredetails():
    return render_template("more_details.html");

@app.route('/booking', methods=['POST','GET'])
def booking():
    status = True
    if request.method == "POST":
        details = request.form
        cname = details['cname']
        contact = details['contact']
        address = details['address']
        pname = details['pname']
        pprice = details['pprice']
        qty = details['qty']
        tamount = details['tamount']
        email = details['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bookings(cust_name, contact, address, pname, price, qty, tamount, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(cname, contact, address, pname, pprice, qty,tamount, email))
        mysql.connection.commit()
        cur.close()
        flash('Data Added Successfully', 'success')
        return render_template('payment.html', **details);
    else:
        return render_template('user_booking.html');

if __name__ == '__main__':
    app.debug = True
    app.run()