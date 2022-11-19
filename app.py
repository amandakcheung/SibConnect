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
        print("Debugging for class_year")
        print(class_year)
        sibconn.create_profile(conn, user_name, email, pronouns, class_year, interests)
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
        category = info.get('category-list')
        desc = info.get('description')        
        #forces the user to resubmit the form if any of the above are missing
        if not category or not desc:
            flash('please fill out all parts of the form')
            return redirect(url_for('seeking'))
        #checks if the tt already exists in the database
        else:
            sibconn.new_seeking(category, description, conn)
            return redirect(url_for('post', pid=pid))

@app.route('/event/', methods=["GET", "POST"])
def event():
    '''
    This processes the form for users who are posting a specific event.
    '''
    conn = dbi.connect()
    if request.method == 'GET':
        categories = sibconn.get_categories(conn)
        return render_template('event-form.html', categories = categories)
    elif request.method == "POST":
        #gets the information from the form
        info = request.form
        category = info.get('category-list')
        desc = info.get('description')
        location = info.get('location')   
        date= info.get('date_time')     
        length= info.get('length')
        recurring= info.get('recurring')
        capacity= info.get('capacity')
        skill= info.get('skill-list')
        #forces the user to resubmit the form if any of the above are missing
        if not category or not desc or not location or (
            not date or not length or not reoccuring or not capacity or not skill):
            flash('please fill out all parts of the form')
            return redirect(url_for('event'))
        #checks if the tt already exists in the database
        else:
            sibconn.new_event(category, desc, location, date, length, recurring, capacity, skill, conn)
            return redirect(url_for('post', pid=pid))

@app.route('/select/', methods= ["GET", 'POST'])
def select():
    '''
    This method processes the select form to allow users to choose
    what movie they want to look at given a dropdown.
    @return the update page for the tt selected
    '''
    conn = dbi.connect()
    if request.method == "GET":
        movie_list = crud.get_incomplete_movies(conn)
        return render_template('select.html', incomplete_movie=movie_list)
    if request.method == "POST":
        tt = request.form.get('menu-tt')
        #tt = crud.get_movie_tt(title, conn)
        print(tt)
        return redirect(url_for('update', tt=tt))

@app.route('/update/<tt>', methods=["GET", "POST"])
def update(tt):
    '''
    This method displays the update page for any given tt. 
    It will either update the page, or display it depending on
    the request. 
    @param the tt of the movie to be displayed
    @return the update.html template
    '''
    conn = dbi.connect()
    movie_dict = crud.find_movie(conn, tt)
    print('update restart- moviett')
    print(tt)
    print('update restart- movie_dict')
    print(movie_dict)
    if request.method == "GET":
        #movie_dict = crud.find_movie(conn, tt)
        #checks to put the director onto the form if exists
        if not crud.get_director(conn, movie_dict.get('director')):
            dname = 'None Specified'
        else:
            dname = crud.get_director(conn, movie_dict.get('director'))['name']
        return render_template('update.html',movie= movie_dict,director_name=dname)
    if request.method == "POST":
        info = request.form
        #if the submission was with the update button
        if info.get('submit') == 'update':
            #checks if the tt already exists (and is not the same as current one)
            matching_tt = (info.get('movie-tt') == tt)
            #checks if the tt's are the same
            if matching_tt:
                crud.update_movie(conn, info, tt)
                flash(info.get('movie-title') + ' was updated sucessfully')
                movie_dict= crud.find_movie(conn, info.get('movie-tt'))
                if not crud.get_director(conn, movie_dict.get('director')):
                    dname = 'None Specified'
                else:
                    dname = crud.get_director(conn, movie_dict.get('director'))['name']
                return render_template('update.html', movie=movie_dict, director_name=dname)
            if crud.check_if_not_exists(info.get('movie-tt'), conn):
                print('info for not exiting')
                print(info)
                crud.update_movie(conn, info, tt)
                flash(info.get('movie-title') + ' was updated sucessfully')
                #return render_template('update.html', movie=)
                return redirect(url_for('update', tt= info.get('movie-tt')))
            else:
                flash('movie with that id already exists. can not update')
                movie_dict = crud.find_movie(conn, tt)
                return render_template('update.html', movie=movie_dict, director_name=dname)
        #if the submission was for delete
        elif info.get('submit') == 'delete':
            crud.delete_movie(conn, info)
            flash('Movie (' +info.get('movie-title')+ ") was deleted successfully")
            return redirect(url_for('index'))

@app.route('/<category>/',methods= ['GET','POST'])
def category(category):
    ''' This methods displays the category's posts'''
    conn = dbi.connect()
    if request.method == "GET":
        all_posts = sibconn.get_posts(conn,category)
        return render_template('posts.html', category=category, all_posts=all_posts)

@app.route('/post/<pid>/', methods= ['GET','POST'])
def display_post(pid):
    '''This method displays the post details'''
    conn = dbi.connect()
    if request.method == "GET":
        full_post = sibconn.get_specific_post(conn, pid)
        return render_template('post.html', post= full_post)

@app.route('/search/')
def search():
    '''
    This method displays the search.html file
    @return the template for search.html is displayed
    '''
    return render_template('search.html')


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
