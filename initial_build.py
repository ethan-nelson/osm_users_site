import psycopg2
import osmdt
import datetime


def convert_time(input_time):
    return datetime.datetime.strptime(input_time, '%Y-%m-%dT%H:%M:%SZ')


conn = psycopg2.connect("dbname='osm_users' host='localhost' user='osm_users' password='osm' options='-c log_min_messages=PANIC'")


for i in range(99999999):
    print 'Now starting file %i.' % (i)
    try:
        temp = osmdt.fetch(str(i), time='day')
    except:
        print 'Error with retrieving file %i.' % (i)
        break
    temp = osmdt.process(temp)
    users = osmdt.extract_users(temp)
    del temp

    for user in users:
        userid = users[user]['uid']
        username = user
        a_time = users[user]['timestamps'][-1]
        a_time = convert_time(a_time)
        
        cursor = conn.cursor()
        cursor.execute("""DO $do$ BEGIN IF EXISTS (SELECT 1 FROM users WHERE username = %s) THEN 
                          UPDATE users SET end_date = %s WHERE username = %s; ELSE
                          INSERT INTO users (userid, username, start_date, end_date)
                          VALUES (%s, %s, %s, %s); END IF; END $do$""",
                          (username, a_time, username, userid, username, a_time, a_time))
        conn.commit()

        cursor.close()
        del cursor

        with open('state.txt','w') as f:
            f.write(str(i))
            f.close()
