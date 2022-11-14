def new_seeking(category, description, conn):
    '''
    This method inserts a seeking post into the post database
    @param the tt, title, release date of the movie, connector for the database
    '''
    curs = dbi.dict_cursor(conn)
    sql = '''insert into post(pid, uid, type, category,description) 
    values (%s, %s, 'seeking_post', %s, %s);'''
    curs.execute(sql, [pid, uid, category, description])
    conn.commit()

def new_event(category, desc, location, date, length, recurring, capacity, skill, conn):
    '''
    This method inserts an event post into the post database
    @param the tt, title, release date of the movie, connector for the database
    '''
    curs = dbi.dict_cursor(conn)
    sql = '''insert into post(pid, uid, type, category,location, date_time, length, recurring, capacity, skill, description)
    values (%s, %s, 'event_post', %s, %s, %s, %s, %s, %s, %s, %s);'''
    curs.execute(sql, [pid, uid, category, location, date, length, recurring, capacity, skill, desc])
    conn.commit()