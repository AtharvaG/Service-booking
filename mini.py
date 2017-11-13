from flask import Flask 
from flaskext.mysql import MySQL
import mysql.connector
from mysql.connector.errors import Error 
from flask import render_template
from flask import request, redirect, url_for, session, flash, jsonify
from functools import wraps
from datetime import timedelta, datetime as dt 
import matplotlib.pyplot as plot
import base64
import StringIO

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gomya'
app.config['MYSQL_DATABASE_DB'] = 'mini'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
 
app.secret_key = "my precious"		



def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('you need to login first')
			return redirect(url_for('login'))
	return wrap

@app.route("/")
def index():
	return render_template('index.html')


@app.route('/login', methods =['POST', 'GET'])
def login():
	error = None 
	if request.method == 'POST':
		mail = request.form['username'] 
		session['id'] = mail 
		password = request.form['password']
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT cid from customer where mail = %s AND mobile = %s ", (mail,password))
		dMail = cursor.fetchall()

		# cursor.execute("SELECT hid from helper where mail = %s AND mobile = %s")

		
		if not dMail:
			error = 'Invalid Credentials'
		else:
			session['logged_in'] = True
			flash('logged in')
			return redirect(url_for('index'))
	return render_template('login.html', error = error)

@app.route('/dashboard', methods = ['POST', 'GET'])
@login_required
def dashboard():

	return render_template('dashboard.html')



@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	session.pop('hid', None)
	return redirect(url_for('index'))


@app.route('/registered', methods = ['GET', 'POST'])
def registered():
	message = None
	if request.method == 'POST':
		try:
			con = mysql.connect()
			cursor = con.cursor()
			name = request.form['name']
			phone = request.form['phone']
			address  = request.form['address']
			mail = request.form['mail']
			password = request.form['password']
			query = ("""
				INSERT INTO customer (name,mobile,mail,adress)
				values (%s, %s, %s, %s)""")
			cursor.execute(query, (name,phone,mail,address))
			con.commit() 
			message = 'Registration Successful'
		except Exception as err :
			message = 'Mail exists'
			return render_template('registered.html', message = message)

	return render_template('registered.html', message = message )

@app.route('/electrician', methods = ['GET', 'POST'])
@login_required
def electrician():
	a = None
	price = 0
	# cid = 0
	if request.method == 'POST':
		con = mysql.connect()
		cursor = con.cursor()
		mail1 = session['id']
		args = [mail1]
		# cursor.execute("SELECT cid from customer where mail = %s", (mail1))
		cursor.callproc('getid', args )
		datacid = cursor.fetchall()



		for data in datacid:
			cid = datacid[0]
		print str(cid) + "shreyas" 

		date = request.form['date']
		time = request.form['time']
		duration = request.form['duration']

		date_str= date + ' ' + time 
		date_obj = dt.strptime(date_str, '%m/%d/%Y %H:%M%p')
		dateTime = dt.strftime(date_obj, '%Y/%m/%d %H:%M:%S')
		dateTime = dt.strptime(dateTime, '%Y/%m/%d %H:%M:%S')

		duration = int(duration)
		dateTimeEnd = dateTime + timedelta(hours = duration)

		cursor.execute ("SELECT hid from helper where sid = 1")
		helperdata = cursor.fetchall()

		hid = []
		for data in helperdata:
			hid.append(data[0])

		print hid 

		if duration <= 1:
			price  = duration * 199
		elif duration > 1 and duration <= 3:
			price = 199 + (duration -1) *100 
		elif time > 3: 
			price = 399 + (time-3) *50 
					
		list_len = len(hid)
		print str(hid[1]) + "testing"
		for n in range(0,list_len):
			print str(n) + "hari"
			flag = 99
			cursor.execute("SELECT hid, startTime, endTime from booked where hid = %s  and sid = 1 ",  hid[n-1] ) 
			# cursor.execute("SELECT * from booked where startTime < {0}".format( dateTime))
			dataall = cursor.fetchall()

			startTime = []
			endTime = []
			hid1 = []
			print dataall 
			for data in dataall:
				hid1.append(data[0])
				startTime.append(data[1]) 
				endTime.append(data[2])

			if not dataall:
				cursor.execute("INSERT INTO booked (cid,hid,noHrs,finalAmount,startTime, endTime, sid) values (%s, %s, %s, %s, %s, %s, 1)"
					, (cid[0],hid[n-1],duration,price,dateTime, dateTimeEnd))
				con.commit()
				print "hello1"
				return redirect(url_for('dispElec'))
				break

			print hid[n]
			for s, e in zip(startTime, endTime) :
				if (dateTime > s and dateTime < e)  or (dateTimeEnd > s and dateTimeEnd < e): 
					flag =1
					break
				
				else :
					flag =0
					pass 

			if flag == 0: 
				cursor.execute("INSERT INTO booked (cid,hid,noHrs,finalAmount,startTime, endTime, sid) values (%s, %s, %s, %s, %s, %s, 1)"
					, (cid[0],hid[n-1],duration,price,dateTime, dateTimeEnd,))
				con.commit()
				print "hello"
				return redirect(url_for('dispElec'))	
				break			
				

	return render_template('s1.html')

@app.route('/dispElec', methods = ['POST', 'GET'])
@login_required
def dispElec():
	con = mysql.connect()
	cursor = con.cursor()
	mail = session['id']

	cursor.execute("""
		SELECT helper.name, customer.name, booked.startTime, booked.noHrs, booked.finalAmount
		from helper, booked, customer
		where helper.hid = booked.hid and booked.cid = customer.cid order by bid desc limit 1
		""")
	datadisp = cursor.fetchall()
	
	for data in datadisp:
		helperid = datadisp[0]


	return render_template ('od1.html', datadisp = datadisp)

@app.route('/bookings', methods = ['POST', 'GET'])
def bookings():
	con = mysql.connect()
	cursor = con.cursor()
	print session['hid']

	cursor.execute ("""SELECT customer.name, customer.mobile, customer.adress, booked.noHrs, booked.bid from  booked, customer"""
		""" where customer.cid = booked.cid and status = 0 and hid = (select hid from helper where mobile = %s)""", (session['hid']) )
	dataall = cursor.fetchall()
	print dataall
	if request.method == 'POST':
		my_id = request.form.get("my_id", "")
		my_id = int(my_id)
		time  = request.form['timedial'] 
		time = int(time)
		a =1 
		print time
		if time <= 1:
			price  = time * 199
		elif time > 1 and time <= 3:
			price = 199 + (time -1) *100 
		elif time > 3: 
			price = 399 + (time-3) *50 

		cursor.execute("""
			UPDATE booked 
			set noHrs = %s, status = %s, finalAmount = %s
			where bid = %s 
			""", (time,a,price,my_id))
		con.commit()

	return render_template ('bookings.html', dataall = dataall)


@app.route('/plumber', methods = ['GET', 'POST'])
@login_required
def plumber():
	a = None
	price = 0
	# cid = 0
	if request.method == 'POST':
		con = mysql.connect()
		cursor = con.cursor()
		mail1 = session['id']
		args = [mail1]
		# cursor.execute("SELECT cid from customer where mail = %s", (mail1))
		cursor.callproc('getid', args )

		datacid = cursor.fetchall()

		for data in datacid:
			cid = datacid[0]

		date = request.form['date']
		time = request.form['time']
		duration = request.form['duration']

		date_str= date + ' ' + time 
		date_obj = dt.strptime(date_str, '%m/%d/%Y %H:%M%p')
		dateTime = dt.strftime(date_obj, '%Y/%m/%d %H:%M:%S')
		dateTime = dt.strptime(dateTime, '%Y/%m/%d %H:%M:%S')

		duration = int(duration)
		dateTimeEnd = dateTime + timedelta(hours = duration)

		cursor.execute ("SELECT hid from helper where sid = 2")
		helperdata = cursor.fetchall()

		hid = []
		for data in helperdata:
			hid.append(data[0])

		print hid 

		if duration <= 1:
			price  = duration * 199
		elif duration > 1 and duration <= 3:
			price = 199 + (duration -1) *100 
		elif time > 3: 
			price = 399 + (time-3) *50 

		list_len = len(hid)
		for n in range(0,list_len):
			flag = 99
			cursor.execute("SELECT hid, startTime, endTime from booked where hid = %s and sid = 2 ",  hid[n-1] ) 
			# cursor.execute("SELECT * from booked where startTime < {0}".format( dateTime))
			dataall = cursor.fetchall()

			startTime = []
			endTime = []
			hid1 = []
			print dataall 
			for data in dataall:
				hid1.append(data[0])
				startTime.append(data[1]) 
				endTime.append(data[2])

			if not dataall:
				cursor.execute("INSERT INTO booked (cid,hid,noHrs,finalAmount,startTime, endTime, sid) values (%s, %s, %s, %s, %s, %s, 2)"
					, (cid[0],hid[n-1],duration,price,dateTime, dateTimeEnd))
				con.commit()
				print "hello1"
				return redirect(url_for('dispPlumber'))
				break

			print hid[n-1]
			for s, e in zip(startTime, endTime) :
				if (dateTime > s and dateTime < e)  or (dateTimeEnd > s and dateTimeEnd < e): 
					flag =1
					break
				
				else :
					flag =0
					pass 

			if flag == 0: 
				cursor.execute("INSERT INTO booked (cid,hid,noHrs,finalAmount,startTime, endTime, sid) values (%s, %s, %s, %s, %s, %s, 2)"
					, (cid[0],hid[n-1],duration,price,dateTime, dateTimeEnd))
				con.commit()
				print "hello"
				return redirect(url_for('dispPlumber'))	
				break			
				

	return render_template('s11.html')

@app.route('/dispPlumber', methods = ['POST', 'GET'])
@login_required
def dispPlumber():
	con = mysql.connect()
	cursor = con.cursor()
	mail = session['id']

	cursor.execute("""
		SELECT helper.name, customer.name, booked.startTime, booked.noHrs, booked.finalAmount
		from helper, booked, customer
		where helper.hid = booked.hid and booked.cid = customer.cid order by bid desc limit 1
		""")
	datadisp = cursor.fetchall()
	
	for data in datadisp:
		helperid = datadisp[0]


	return render_template ('od1.html', datadisp = datadisp)

@app.route('/cleaning', methods = ['POST', 'GET'])
@login_required
def cleaning():
	con = mysql.connect()
	cursor = con.cursor()
	if request.method == 'POST':

		mail = session['id']
		cursor.execute("""
			SELECT cid from customer
			where mail = %s""", (mail))
		datacid = cursor.fetchall()

		for data in datacid:
			cid = data[0]

		shirt = int(request.form['shirt'])
		pant = int(request.form['pant'])
		woolen = int(request.form['woolen'])
		items = int(request.form['items'])
		print shirt
		print pant
		print woolen
		print items

		price = ((shirt+pant)*20) + (woolen*35) + (items*25)
		print price

		now = dt.now()
		print type (now)

		cursor.execute("""
			INSERT into cleaning(cid,noShirt, noPant, nowoolen, noItem, finalAmount, serviceDate) values (%s,%s,%s,%s,%s,%s,%s)""",
			(cid, shirt, pant, woolen,items,price,now ))
		con.commit()

		if price > 0:
			return redirect(url_for('dispCleaning'))

	return render_template ('Dry Cleaning.html')

@app.route('/dispCleaning', methods = ['POST', 'GET'])
@login_required
def dispCleaning():
	con = mysql.connect()
	cursor = con.cursor()
	# mail = session['id']
	print "hello"

	cursor.execute("""
		SELECT customer.name, cleaning.noShirt, cleaning.noPant, cleaning.nowoolen, cleaning.noItem, cleaning.finalAmount FROM cleaning, customer
		where cleaning.cid = customer.cid 
		order by clid desc limit 1 """)
	datall = cursor.fetchall()
	print datall

	return render_template('nextCleaning.html', datall = datall)

@app.route('/spending', methods = ['POST', 'GET'])
@login_required
def spending():
	con = mysql.connect()
	cursor = con.cursor()
	img = StringIO.StringIO()
	mail = session['id']

	fig = plot.figure(figsize=(4,4))
	ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

	cursor.execute("""
		SELECT service.category, sum(finalAmount) from booked, service 
		where service.sid = booked.sid and 
		cid = (select cid from customer where mail = %s) and status  =  1 group by booked.sid 
		""", (mail)) 
	datall = cursor.fetchall()
	
	fracs=[]
	labels= []
	for data in datall:
		fracs.append(data[1])
		labels.append(data[0])

	print fracs
	print labels

	pie_chart = ax.pie(fracs, labels = labels, startangle = 90, autopct = '%1.1f%%')
	fig.savefig(img, format = 'png')
	img.seek(0)
	plot_url = base64.b64encode(img.getvalue()).decode()

	return render_template('mspent.html', plot_url = plot_url)


@app.route('/helperLogin', methods = ['POST', 'GET'])
def helperLogin():
	con = mysql.connect()
	cursor = con.cursor()	
	if request.method == 'POST':
		phone  = request.form['username'] 
		print phone

		cursor.execute("SELECT * from helper where mobile  = %s ", (phone))
		phonedata = cursor.fetchall()

		if not phonedata :
			return redirect(url_for('helperLogin'))
		else :
			session['hid'] = True
			session['hid'] = phone
			return redirect(url_for('bookings'))

	return render_template('loginforhelper.html')

@app.route('/admin')
def admin():
    plot_url=rendergraph1()
    # plot_url2=rendergraph2()
    return render_template('graphs.html', plot_url=plot_url )

def rendergraph1():
    cursor.execute("SELECT category,count(*) from project_info group by category")
    dataall=cursor.fetchall()
    img = StringIO.StringIO()
    category,index,count =[],[],[]
    i=0
    for data in dataall:
        category.append(data[0])
        index.append(i)
        count.append(data[1])
        i=i+1
    print index, count
    plt.bar(index, count, color = 'r')
    plt.xticks(index, category, rotation=25)
    plt.yticks(range(min(count), max(count)+1))
    plt.rcParams['xtick.major.pad']='5'
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

@app.route('/pastbookingsc', methods = ['POST', 'GET'])
@login_required
def pastbookingsc():
	con = mysql.connect()
	cursor = con.cursor()

	cursor.execute("""
		SELECT customer.name, helper.name, helper.mobile, service.category, booked.noHrs, booked.finalAmount from  booked, customer,
		service, helper 
		where customer.cid = booked.cid and helper.hid = booked.hid and service.sid = booked.sid and
		status = 1 and booked.cid = (select cid from customer where mail = %s)
		""",(session['id']))
	dataall = cursor.fetchall()   

	return render_template('pastbookingsc.html', dataall= dataall )

@app.route('/ongoing', methods = ['POST', 'GET'])
@login_required
def ongoing():
	con = mysql.connect()
	cursor = con.cursor()

	cursor.execute("""
		SELECT customer.name, helper.name, helper.mobile, service.category, booked.noHrs, booked.finalAmount from  booked, customer,
		service, helper 
		where customer.cid = booked.cid and helper.hid = booked.hid and service.sid = booked.sid and
		status = 0 and booked.cid = (select cid from customer where mail = %s)
		""",(session['id']))
	dataall = cursor.fetchall()   

	return render_template('ongoing.html', dataall= dataall )

@app.route('/pastbookingsh', methods = ['POST', 'GET'])
def pastbookingsh():
	con = mysql.connect()
	cursor = con.cursor()
	print session['hid']

	cursor.execute("""
		SELECT customer.name, customer.mobile, customer.adress , booked.noHrs, booked.finalAmount from  booked, customer 
		where customer.cid = booked.cid and 
		status = 1 and booked.hid = (select hid from helper where mobile = %s)
		""",(session['hid']))
	dataall = cursor.fetchall()   

	return render_template('pastbookingsh.html', dataall= dataall )



if __name__ =="__main__":
	app.run(debug = True)
 
