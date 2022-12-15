#Authors: SibConnect- Amanda Cheung, Bethany Costello, Rita Lyu, Dominique Nino
#Date: 11/17/2022
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
import sibconn
# import cs304dbi_sqlite3 as dbi

import random
import bcrypt

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# new for file upload
app.config['UPLOADS'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10*1024*1024 # 1 MB


@app.route('/')
def home():
    '''
    This method is for the main page to display base.html at the url '/'
    @return the template for base.html will be displayed
    '''
    return render_template('home.html')

@app.route('/create_profile/', methods=["GET", "POST"])
def create_profile():
    '''
    Upload the data that users filled out with the log-in form to the database
    generate a unique userid
    '''
    conn = dbi.connect()
    #gets the blank create profile form 
    if request.method == 'GET':
        return render_template('create-profile.html')
    elif request.method == "POST":
        #gets the user input from the form
        info = request.form
        email = info.get('email')
        #checks if email exists already
        if sibconn.get_uid(conn,email):
            flash('email already has an account')
            return render_template('create-profile.html')
        first = info.get('first_name')
        last = info.get('last_name')
        passwd = info.get('password')
        print("print passwd for profile creating")
        print(passwd)
        #create hashing for password
        hashed = bcrypt.hashpw(passwd.encode('utf-8'),
                           bcrypt.gensalt())
        stored = hashed.decode('utf-8')
        print('debugging for hash')
        print(passwd, type(passwd), hashed, stored)
        pronouns = info.get('pronouns')
        interests = info.get('interests')
        class_year = info.get('class_year')
        print("print class year for profile creating")
        print(class_year)
        sibconn.create_profile(conn, email, first, last, hashed, pronouns, class_year, interests)
        print("print email for profile creating")
        print(email)
        email = str(email)
        uid = sibconn.get_uid(conn,email)
        uid = uid.get('uid')
        print("print uid for profile creating")
        print(uid)
        session['uid'] = uid
        return redirect(url_for('display_user'))

@app.route('/login/', methods=["GET", "POST"])
def login():
    '''this method allows users to log in'''
    #gets the blank create profile form 
    if request.method == 'GET':
        return render_template('log-in.html')
    #gets the information from the form
    elif request.method == "POST":
        conn = dbi.connect()
        email = request.form.get('email')
        uid = sibconn.get_uid(conn, email)
        passwd = request.form.get('password')
        row = sibconn.login(conn, email)
        session['uid'] = uid
        print('debugging for login-row')
        print(row)
        if row is None:
            #redirect user to create profile
            flash("You don't have a profile yet, create a profile.")
            return redirect( url_for('create_profile'))
        stored = row['hashed']
        first = row['first_name']
        print('database has stored: {} {}'.format(stored,type(stored)))
        print('form supplied passwd: {} {}'.format(passwd,type(passwd)))
        hashed2 = bcrypt.hashpw(passwd.encode('utf-8'),
                                stored.encode('utf-8'))
        hashed2_str = hashed2.decode('utf-8')
        print('rehash is: {} {}'.format(hashed2_str,type(hashed2_str)))
        if hashed2_str == stored:
            print('they match!')
            flash('Welcome '+ first + '!')
            session['email'] = email
            session['first_name'] = first
            session['uid'] = row['uid']
            session['logged_in'] = True
            session['visits'] = 1
            return redirect(url_for('display_user'))
        else: 
            flash('Password is incorrect. Try again.')
            return redirect( url_for('login'))

@app.route('/logout/')
def logout():
    '''this method allows users to log out'''
    if 'email' in session:
        email = session['email']
        first = session['first_name']
        session.pop('email')
        session.pop('first_name')
        session.pop('uid')
        session.pop('logged_in')
        flash('You are logged out')
        return redirect(url_for('login'))
    else:
        flash('you are not logged in. Please login or join')
        return redirect( url_for('login') )


@app.route('/seeking/', methods=["GET","POST"])
def seeking():
    '''
    This processes the form for users who are seeking a specific event.
    '''
    conn = dbi.connect()
    uid = session.get('uid','')
    if uid == '':
        flash("you haven't log in yet")
        return redirect (url_for('home'))
    if request.method == 'GET':
        categories = sibconn.get_categories(conn)
        return render_template('seeking-form.html', categories = categories)
    elif request.method == "POST":
        #gets the information from the form
        info = request.form
        title= info.get('title')
        category = info.get('category-list')
        desc = info.get('description')
        print('info')
        print(info)
        #forces the user to resubmit the form if any of the above are missing
        if not category or not desc or not title:
            print(category)
            print(desc)
            flash('please fill out all parts of the form')
            return redirect(url_for('seeking'))
        #returns to the detailed post that's posted
        else:
            category = sibconn.get_category(conn,category)
            cid = category.get('cid')
            sibconn.new_seeking(cid, desc, title, conn,uid)
            pid = sibconn.get_last_pid(conn)
            return redirect(url_for('display_post', pid=pid))

@app.route('/event/', methods=["GET", "POST"])
def event():
    '''
    This processes the form for users who are posting a specific event.
    '''
    conn = dbi.connect()
    uid = session.get('uid','')
    if uid == '':
        flash("you haven't log in yet")
        return redirect (url_for('home'))
    if request.method == 'GET':
        categories = sibconn.get_categories(conn)
        return render_template('event-form.html', categories= categories)
    elif request.method == "POST":
        #gets the information from the form
        info = request.form
        print('hello', info)
        title = info.get('title')
        category = info.get('category-list')
        desc = info.get('description')
        location = info.get('location')   
        date= info.get('date_time')     
        length= info.get('length')
        recurring= info.get('recurring')
        capacity= info.get('capacity')
        skill= info.get('skill')
        #forces the user to resubmit the form if any of the above are missing
        if not category or not desc or not location or (
            not date or not length or not recurring or not capacity or (
                not skill or not title)):
            flash('please fill out all parts of the form')
            return redirect(url_for('event'))
        #create a new event and redirect url to the event page 
        else:
            print("succeessfully recorded the entry")
            cid_dict = sibconn.get_category(conn,category)
            cid = cid_dict.get('cid')
            sibconn.new_event(
                cid, title, desc, location, date, length,
                recurring, capacity, skill, conn, uid)
            pid = sibconn.get_last_pid(conn)
            pid = pid.get('last_insert_id()')
            return redirect(url_for('display_post', pid=pid))

@app.route('/<category>/<sort>',methods= ['GET','POST'])
def category(category, sort):
    ''' This methods displays the category's posts'''
    conn = dbi.connect()
    if request.method == "GET":
        if sort == 'leastrecent':
            all_posts = sibconn.sort_recent_post(conn, category, 
            'event_post', 'pid, asc')
        elif sort == "mostrecent":
            all_posts = sibconn.sort_recent_post(conn, category, 
            'event_post', 'pid, desc')
        elif sort == "lowskill":
            all_posts = sibconn.sort_recent_post(conn, category, 
            'event_post', 'skill, asc')
        elif sort == "highskill":
            all_posts = sibconn.sort_recent_post(conn, category, 
            'event_post', 'skill, desc')
        elif sort == "recurring": #recurring is being weird
            all_posts = sibconn.sort_recent_post(conn, category, 
            'event_post', 'recurring, asc')
        elif sort == 'West Side':
            all_posts = sibconn.sort_by_dorm(conn,'Quint/ West Side',category)
        elif sort == 'Tower Court' or sort == \
                        'Stone Davis' or sort == 'New Dorms' or sort == \
                        'Branch (Lake House etc)':
            all_posts = sibconn.sort_by_dorm(conn,sort,category)
        elif sort == '1' or '0':
            all_posts = sibconn.sort_by_recurring(conn, sort, category)      
        else:
            all_posts = sibconn.get_posts(conn,category)
        print(all_posts)
        return render_template('posts.html', category=category, 
        all_posts=all_posts)

@app.route('/post/<pid>/', methods= ['GET','POST'])
def display_post(pid):
    '''This method displays the post details'''
    conn = dbi.connect()
    uid = session.get('uid')
    if request.method == "GET":
        full_post = sibconn.get_specific_post(conn, pid)
        cid = full_post.get('category')
        category = sibconn.get_category_name(conn,cid)
        comments= sibconn.grab_comments(conn,pid)
        if sibconn.check_interested(conn,uid,pid):
            print('pressed intersted uid', uid)
            interested='uninterested'
        else:
            print('need to press interested uid', uid)
            interested="interested"
        if full_post.get('type') == 'event_post':
            return render_template('display_event_post.html', 
            post= full_post, comments=comments,category= category, interested=interested)
        else:
            return render_template('display_seeking_post.html', 
            post= full_post, comments=comments,category= category, interested=interested)
    if request.method == "POST":
        if not uid:
            flash('you need to log in!')
            return redirect(url_for('display_post', pid=pid))
        else:
            info = request.form
            if info.get('submit') == "interested":
                flash('this post has been added to your interests')
                print('interested uid',uid)
                print('interested pid',pid)
                sibconn.add_interested(conn,uid,pid)
                return redirect(url_for('display_post',pid=pid))
            elif info.get('submit') == 'uninterested':
                flash('this post has been removed from your interests')
                sibconn.delete_interested(conn,uid,pid)
                return redirect(url_for('display_post',pid=pid))
            elif info.get('submit') == 'comment':
                commenttext= info.get('commenttext')
                sibconn.create_comment(conn,pid,uid,commenttext)
                return redirect(url_for('display_post',pid=pid))
            else:
                print('not working')

@app.route('/user/', methods= ['GET', 'POST'])
def display_user():
    ''' This method displays the user's profile information
    and what they are interested in'''
    conn = dbi.connect()
    uid = session.get('uid','')
    if uid == '':
        flash("you haven't log in yet")
        return redirect (url_for('home'))
    #src = url_for('pic',uid=uid)
    if request.method == "GET":
        user_posted = sibconn.find_user_posts(conn, uid)
        post_pids = sibconn.find_interested_posts(conn,uid)
        user_interested = []
        for pid in post_pids:
            pid = pid.get('pid')
            user_interested.append(sibconn.get_specific_post(conn,pid))
        user = sibconn.get_user_info(conn,uid)
        print('user', user)
        return render_template('profile_page.html', user = user, 
            user_posted = user_posted, user_interested=user_interested, src= url_for('pic',conn=conn,uid=uid))

@app.route('/search/', methods=['GET'])
def search():
    '''allows users to search the website'''
    conn = dbi.connect()
    if request.method == 'GET':
        phrase = request.args['search a post']
        post_pids = sibconn.search_post(conn,phrase)
        all_posts = []
        for pid in post_pids:
            pid = pid.get('pid')
            all_posts.append(sibconn.get_specific_post(conn,pid))
        return render_template('search.html',phrase = phrase, all_posts = all_posts)

@app.route('/user/update/',methods=["GET","POST"])
def update_profile():
    '''updates the profile after user changes something'''
    conn = dbi.connect()
    uid = session.get('uid')
    user = sibconn.get_user_info(conn,uid)
    src = url_for('pic',conn=conn,uid=uid)
    print("/user/update/")
    print(user)
    if request.method == "GET":
        #add a picture variable
        return render_template('update-profile.html', user = user, src= src)
    elif request.method == "POST":
        user = request.form
        print("/user/update/POST")
        print(user.get('email'))
        sibconn.update_profile(conn, uid, user=user)
        src = sibconn.upload(conn,request)
        return redirect(url_for("display_user"))

@app.route('/pic/<uid>/')
def pic(conn,uid):
    '''Selects the profile picture '''
    curs = dbi.dict_cursor(conn)
    numrows = curs.execute(
        '''select filename from picfile where uid = %s''',
        [uid])
    if numrows == 0:
        flash('No picture for {}'.format(uid))
        return redirect(url_for('index'))
    row = curs.fetchone()
    return send_from_directory(app.config['UPLOADS'],row['filename'])

@app.route('/all_posts/<sort>/', methods=['GET', 'POST'])
def all_posts(sort):
    '''displays all the posts'''
    conn = dbi.connect()
    uid = session.get('uid')
    if request.method == 'GET':
        if sort == 'everything':
            all_posts = sibconn.get_all_posts(conn)
            return render_template('all_posts.html', category = 'all', all_posts=all_posts)
        else:
            all_posts = sibconn.sort_by_type(conn, sort)
            return render_template('all_posts.html', category=category, 
            all_posts=all_posts) 


#use to make the database run
@app.before_first_request
def init_db():
    dbi.cache_cnf()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'sibconn_db' 
    dbi.use(db_to_use)
    print('will connect to {}'.format(db_to_use))

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
