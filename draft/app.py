#Authors: SibConnect- Amanda Cheung, Bethany Costello, Rita Lyu, Dominique Nino
#Date: 11/17/2022
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
#import sibconn.py
import sibconn
# import cs304dbi_sqlite3 as dbi

import random

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True


@app.route('/')
def index():
    '''
    This method is for the main page to display base.html at the url '/'
    @return the template for base.html will be displayed
    '''
    return render_template('base.html')

@app.route('/home/')
def home():
    '''
    This method is for the main page to display base.html at the url '/'
    @return the template for base.html will be displayed
    '''
    return render_template('home.html')

@app.route('/login/', methods=["GET", "POST"])
def log_in():
    '''
    Upload the data that users filled out with the log-in form to the database
    generate a unique userid
    '''
    conn = dbi.connect()
    #gets the blank log in form 
    if request.method == 'GET':
        return render_template('log-in.html')
    elif request.method == "POST":
        #gets the information from the form
        info = request.form
        print("Debugging for login")
        print(info)
        user_name = info.get('user name')
        email = info.get('email')
        pronouns = info.get('pronouns')
        interests = info.get('interests')
        class_year = info.get('class year')
        sibconn.create_profile(
            conn, user_name, email, pronouns, class_year, interests)
        return redirect(url_for('home'))


@app.route('/seeking/', methods=["GET","POST"])
def seeking():
    '''
    This processes the form for users who are seeking a specific event.
    '''
    conn = dbi.connect()
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
            sibconn.new_seeking(cid, desc, title, conn)
            pid = sibconn.get_last_pid(conn)
            pid = pid.get('max(pid)')
            #return redirect(url_for('category', category= category))
            return redirect(url_for('display_post', pid=pid))

@app.route('/event/', methods=["GET", "POST"])
def event():
    '''
    This processes the form for users who are posting a specific event.
    '''
    conn = dbi.connect()
    if request.method == 'GET':
        categories = sibconn.get_categories(conn)
        return render_template('event-form.html', categories= categories)
    elif request.method == "POST":
        #gets the information from the form
        info = request.form
        print(info)
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
            cid = sibconn.get_category(conn,category)
            cid = cid.get('cid')
            sibconn.new_event(
                cid, title, desc, location, date, length,
                recurring, capacity, skill, conn)
            pid = sibconn.get_last_pid(conn)
            pid = pid.get('max(pid)')
            return redirect(url_for('display_post', pid=pid))

@app.route('/<category>/',methods= ['GET','POST'])
def category(category):
    ''' This methods displays the category's posts'''
    conn = dbi.connect()
    if request.method == "GET":
        all_posts = sibconn.get_posts(conn,category)
        return render_template('posts.html', category=category, 
        all_posts=all_posts)

@app.route('/post/<pid>/', methods= ['GET','POST'])
def display_post(pid):
    '''This method displays the post details'''
    conn = dbi.connect()
    if request.method == "GET":
        full_post = sibconn.get_specific_post(conn, pid)
        cid = full_post.get('category')
        category = sibconn.get_category_name(conn,cid)
        print('full post')
        print(full_post)
        if full_post.get('type') == 'event_post':
            return render_template('display_event_post.html', 
            post= full_post, category= category)
        else:
            return render_template('display_seeking_post.html', 
            post= full_post, category= category)

#end of 11/20


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
