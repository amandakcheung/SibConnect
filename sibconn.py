#Authors: SibConnect- Amanda Cheung, Bethany Costello, Rita Lyu, Dominique Nino
#Date: 11/17/2022

import cs304dbi as dbi

# ==========================================================
# The functions that do most of the work.


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

def login(conn, email):
    '''
    This methods checks user email and password and log them in
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT uid,hashed,first_name
                    FROM user
                    WHERE email = %s''',
                 [email])
    return curs.fetchone()



def new_seeking(category, description, title, conn):
    '''
    This method inserts a seeking post into the post database
    @param the tt, title, release date of the movie, connector for the database
    '''
    curs = dbi.dict_cursor(conn)
    sql = '''insert into post(pid, uid, title, type, category,description) 
    values (%s, %s, %s, 'seeking_post', %s, %s);'''
    #place holder uid
    curs.execute(sql, [None, 1, title, category, description])
    conn.commit()

def new_event(category, title, desc, location, date, length, recurring, capacity, skill, conn):
    '''
    This method inserts an event post into the post database
    @param the tt, title, release date of the movie, connector for the database
    '''
    curs = dbi.dict_cursor(conn)
    #place holder uid
    sql = '''
    insert into post(
        pid, uid, type, title, category, location, date_time, length, 
        recurring, capacity, skill, description)
    values (%s, %s, 'event_post', %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
    curs.execute(sql, [None, 1, title, category, 
    location, date, length, recurring, capacity, skill, desc])
    conn.commit()

def get_categories(conn):
    '''This method selects all the categories 
    '''
    curs = dbi.dict_cursor(conn)
    sql =  '''select * from category'''
    curs.execute(sql)
    return curs.fetchall()

def get_posts(conn, category):
    ''' This method gets all of the posts within a category'''
    curs = dbi.dict_cursor(conn)
    sql = '''select * from post where category = 
    (select cid from category where name = %s)'''
    curs.execute(sql,[category])
    return curs.fetchall()

def get_specific_post(conn, pid):
    '''This method gets the details for a specific post'''
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
    ''' This method gets the cid for a given name of category'''
    curs = dbi.dict_cursor(conn)
    sql = '''select max(pid) from post'''
    curs.execute(sql)
    return curs.fetchone()

def sort_recent_post(conn, category, ptype, sorto):
    '''This method sorts event posts from earliest to 
    latest or latest to earliest'''
    curs = dbi.dict_cursor(conn)
    sql = '''select * from post where category = (select cid from category where name = %s) and 
    type = %s
    order by %s'''
    curs.execute(sql, [category, ptype, sorto])
    return curs.fetchall()

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
    interests from user where uid = %s'''
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


def get_last_uid(conn):
    ''' Gets the last inserted uid'''
    curs = dbi.dict_cursor(conn)
    sql = '''select last_insert_id()'''
    curs.execute(sql)
    row = curs.fetchone()
    return row[0]

def update_profile(conn,uid, user):
    '''Updates the Profile with New Information '''
    curs = dbi.dict_cursor(conn)
    sql = '''update user set email=%s, first_name= %s, 
    last_name= %s, pronouns= %s, class_year= %s, interests= %s 
    where uid=%s'''
    curs.execute(sql, [user.get('email'), 
                      user.get('first_name'), 
                      user.get('last_name'), 
                      user.get('pronouns'), 
                      user.get('class_year'),
                      user.get('interests'),
                      uid])
    conn.commit()    

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

def upload(conn):
    ''' Uploads a profile photo'''
    try:
        uid = int(request.form['uid']) # may throw error
        f = request.files['pic']
        user_filename = f.filename
        ext = user_filename.split('.')[-1]
        filename = secure_filename('{}.{}'.format(uid,ext))
        pathname = os.path.join(app.config['UPLOADS'],filename)
        f.save(pathname)
        curs = dbi.dict_cursor(conn)
        curs.execute(
            '''insert into picfile(uid,filename) values (%s,%s)
                on duplicate key update filename = %s''',
            [uid, filename, filename])
        conn.commit()
        flash('Upload successful')
    except Exception as err:
        flash('Upload failed {why}'.format(why=err))
# testing

if __name__ == '__main__':
    dbi.cache_cnf()   # defaults to ~/.my.cnf
    dbi.use('sibconn_db')
    conn = dbi.connect()