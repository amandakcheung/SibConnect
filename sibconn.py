#Authors: SibConnect- Amanda Cheung, Bethany Costello, Rita Lyu, Dominique Nino
#Date: 11/17/2022

import cs304dbi as dbi

# ==========================================================
# The functions that do most of the work.

from flask import (flash, session, request, url_for)
from werkzeug.utils import secure_filename
import os
from app import app

def create_profile(conn, email, first, last, hashed, pronouns, class_year, interests):
    '''
    This method creates a user profile and stores the password for a new user
    '''
    curs = dbi.dict_cursor(conn)
    try: 
        sql = '''insert into user (uid, email, first_name, last_name, hashed, pronouns, class_year, interests)
                values (%s, %s, %s, %s, %s, %s, %s, %s);'''
        curs.execute(sql, [None, email, first, last, hashed, pronouns, class_year, interests])
        conn.commit()
    except Exception as err:
        print('something went wrong', repr(err))
    sql = '''select last_insert_id()'''
    curs.execute(sql)
    return curs.fetchone()

def login(conn, email):
    '''
    This method selects the log in information for a user and fetches it 
    from the database
    based on an email
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT uid,hashed,first_name
                    FROM user
                    WHERE email = %s''',
                 [email])
    return curs.fetchone()

def new_seeking(category, description, title, conn,uid):
    '''
    This method inserts a seeking post into the post database
    @param the tt, title, release date of the movie, connector for the database
    '''
    curs = dbi.dict_cursor(conn)
    sql = '''insert into post(pid, uid, title, type, category,description) 
    values (%s, %s, %s, 'seeking_post', %s, %s);'''
    curs.execute(sql, [None, uid, title, category, description])
    conn.commit()
    sql = '''select last_insert_id()'''
    curs.execute(sql)
    pid = curs.fetchone()
    return pid.get('last_insert_id()')

def new_event(category, title, desc, location, date, length, recurring, capacity, skill, conn, uid):
    '''
    This method inserts an event post into the post database
    @param category, title, desc, location, date, length, recurring, capacity, skill, uid, conn
    '''
    curs = dbi.dict_cursor(conn)
    sql = '''
    insert into post(
        pid, uid, type, title, category, location, date_time, length, 
        recurring, capacity, skill, description)
    values (%s, %s, 'event_post', %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
    curs.execute(sql, [None, uid, title, category, 
    location, date, length, recurring, capacity, skill, desc])
    conn.commit()
    sql = '''select last_insert_id()'''
    curs.execute(sql)
    pid = curs.fetchone()
    return pid.get('last_insert_id()')

def get_categories(conn):
    '''This method selects all the categories 
    '''
    curs = dbi.dict_cursor(conn)
    sql =  '''select cid, name from category'''
    curs.execute(sql)
    return curs.fetchall()

def get_posts(conn, category):
    ''' This method gets all of the posts within a category
    Returns every column for every post in a category'''
    curs = dbi.dict_cursor(conn)
    sql = '''select * from post where category = 
    (select cid from category where name = %s)'''
    curs.execute(sql,[category])
    return curs.fetchall()

def get_specific_post(conn, pid):
    '''This method gets the details for a specific post
    Returns all posts with its title, description, 
    pid, location, recurrence, skill level'''
    curs = dbi.dict_cursor(conn)
    sql = '''select * from post where pid= %s'''
    curs.execute(sql,[pid])
    return curs.fetchone()

def get_category(conn, name):
    ''' This method gets the cid for a given name of category'''
    curs = dbi.dict_cursor(conn)
    sql = '''select cid from category where name= %s'''
    curs.execute(sql,[name])
    return curs.fetchone()

def get_category_name(conn,cid):
    ''' This method gets the category name based on the cid'''
    curs = dbi.dict_cursor(conn)
    sql = '''select name from category where cid= %s'''
    curs.execute(sql,[cid])
    return curs.fetchone()    

def get_last_pid(conn):
    '''This method gets the most recent post'''
    curs = dbi.dict_cursor(conn)
    sql = '''select last_insert_id()'''
    curs.execute(sql)
    return curs.fetchone()

def find_user_posts(conn,uid):
    '''This method finds all posts that the user
    has created'''
    curs = dbi.dict_cursor(conn)
    sql = '''select * from post where uid =%s'''
    curs.execute(sql,[uid])
    return curs.fetchall()

def find_interested_posts(conn, uid):
    '''This method finds all posts that the user is interested in'''
    curs = dbi.dict_cursor(conn)
    sql = '''select pid from interested where uid = %s'''
    curs.execute(sql,[uid])
    return curs.fetchall()

def get_user_info(conn, uid):
    '''This method finds the name of a uid'''
    curs= dbi.dict_cursor(conn)
    sql = '''select first_name, last_name, email, pronouns, class_year, 
    interests, dorm from user where uid = %s'''
    curs.execute(sql,[uid])
    return curs.fetchone()

def get_uid(conn,email):
    '''This method finds the uid of a user
    based on their email'''
    curs= dbi.dict_cursor(conn)
    sql = '''select uid from user where email = %s'''
    curs.execute(sql,[email])
    return curs.fetchone()

def search_post(conn, phrase):
    ''' This method allows users to search
    must have direct words'''
    curs = dbi.dict_cursor(conn)
    sql = '''select pid from post where title like %s or 
    description like %s'''
    curs.execute(sql, ['%' + phrase + '%', '%' + phrase + '%'])
    info = curs.fetchall()
    return info

def update_profile(conn,uid, user):
    '''Updates the Profile with New Information '''
    curs = dbi.dict_cursor(conn)
    sql = '''update user set email=%s, first_name= %s, 
    last_name= %s, pronouns= %s, class_year= %s, interests= %s, dorm=%s
    where uid=%s'''
    curs.execute(sql, [user.get('email'), 
                      user.get('first_name'), 
                      user.get('last_name'), 
                      user.get('pronouns'), 
                      user.get('class_year'),
                      user.get('interests'),
                      user.get('dorm'),
                      uid])
    conn.commit()

def upload(conn, request):
    ''' Uploads a profile photo'''
    try:
        uid = int(session.get('uid')) # may throw error
        print(uid)
        f = request.files['pic']
        user_filename = f.filename
        ext = user_filename.split('.')[-1]
        filename = secure_filename('{}.{}'.format(uid,ext))
        pathname = os.path.join(app.config['UPLOADS'],filename)
        print('pathname',pathname)
        f.save(pathname)
        curs = dbi.dict_cursor(conn)
        curs.execute(
            '''insert into picfile(uid,filename) values (%s,%s)
                on duplicate key update filename = %s''',
            [uid, filename, filename])
        conn.commit()
        flash('Upload successful')
        src = url_for('pic',conn=conn,uid=uid)
        return src
    except Exception as err:
        flash('Upload failed {why}'.format(why=err))


def add_interested(conn, uid,pid):
    ''' adds the user and the pid to the interested table'''
    curs = dbi.dict_cursor(conn)
    sql = '''insert into interested(uid,pid) 
    values (%s, %s)'''
    curs.execute(sql,[uid,pid])
    conn.commit()


def count_interested(conn,pid):
    ''' counts how many likes the post receives'''
    curs = dbi.dict_cursor(conn)
    sql = ''' select count(*) from interested where pid=%s'''
    curs.execute(sql,[pid])
    return curs.fetchone()

def check_interested(conn,uid,pid):
    '''checks if the user and pid are already in the
    interested table'''
    curs = dbi.dict_cursor(conn)
    sql = '''select uid,pid from interested
    where uid = %s and pid = %s'''
    curs.execute(sql,[uid,pid])
    return curs.fetchone()

def delete_interested(conn,uid,pid):
    '''deletes a user, pid from interested table'''
    curs = dbi.dict_cursor(conn)
    sql = '''delete from interested where uid = %s and pid = %s'''
    curs.execute(sql,[uid,pid])
    conn.commit()
    
def create_comment(conn,pid,uid,commenttext):
    '''Inserts new comment into comment database'''
    curs = dbi.cursor(conn)
    curs.execute('''insert into comment (commentid,pid,uid,commenttext) values (%s,%s,%s,%s)'''
                 , [None,pid,uid,commenttext])
    conn.commit() 
    
def grab_comments(conn,pid):
    '''Finds all comments for a post'''
    curs = dbi.dict_cursor(conn)
    sql = ''' select comment.commenttext, user.first_name, user.last_name
    from comment inner join user using (uid)
    where pid = %s;'''
    curs.execute(sql,[pid])
    return curs.fetchall()

def filter_by_dorm(conn,dorm, category):
    '''Displays all the events happening in a dorm'''
    curs = dbi.dict_cursor(conn)
    sql = '''select pid, uid, type, title, category, location, 
    date_time, length, recurring, capacity, skill, description
    from post where location = %s and type = 'event_post' and 
    category = (select cid from category where name = %s)'''
    curs.execute(sql,[dorm,category])
    return curs.fetchall()

def filter_by_recurring(conn,num, category):
    '''Displays either recurring or not'''
    curs = dbi.dict_cursor(conn)
    sql = '''select pid, uid, type, title, category, location,
    date_time, length, recurring, capacity, skill, description
    from post where recurring = %s and type='event_post' and 
    category = (select cid from category where name = %s)'''
    curs.execute(sql,[num,category])
    return curs.fetchall()

def get_all_posts(conn):
    '''retrieves all posts'''
    curs = dbi.dict_cursor(conn)
    sql = '''select pid, uid, type, title, category, location,
    date_time, length, recurring, capacity, skill, description
    from post 
    order by pid desc'''
    curs.execute(sql)
    return curs.fetchall()

def filter_by_type(conn, sort):
    '''sorts the posts by seeking or event post'''
    curs = dbi.dict_cursor(conn)
    sql = '''select pid, uid, type, title, category, location,
    date_time, length, recurring, capacity, skill, description
    from post where type = %s'''
    curs.execute(sql,[sort])
    return curs.fetchall()

if __name__ == '__main__':
    dbi.cache_cnf()   # defaults to ~/.my.cnf
    dbi.use('sibconn_db')
    conn = dbi.connect()