#Authors: SibConnect- Amanda Cheung, Bethany Costello, Rita Lyu, Dominique Nino
#Date: 11/17/2022

import cs304dbi as dbi

# ==========================================================
# The functions that do most of the work.

def create_profile(conn, user_name, email, pronouns, class_year, interests):
    '''
    This method inserts a new user profile into the 
    '''
    sql = '''insert into user (uid, name, email, pronouns, class_year, interests)
    values (%s, %s, %s, %s, %s, %s);'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql, [None, user_name, email, pronouns, class_year, interests])
    conn.commit()

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

# testing

if __name__ == '__main__':
    dbi.cache_cnf()   # defaults to ~/.my.cnf
    dbi.use('sibconn_db')
    conn = dbi.connect()