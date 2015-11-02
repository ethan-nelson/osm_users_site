import osmdt
import datetime
import osmhm
import time

osmhm.config.database_url = 'postgres://osm_users:osm@localhost/osm_users'


def convert_time(input_time):
    return datetime.datetime.strptime(input_time, '%Y-%m-%dT%H:%M:%SZ')


while True:
    sequence = osmhm.fetch.fetch_last_read()

    if not sequence:
        osmhm.fetch.fetch_next(time_type='hour', reset=True)
        sequence = osmhm.fetch.fetch_last_read()

    if sequence['read_flag'] is False:
        print "Processing sequence %s." % (sequence['sequencenumber'])

        data_stream = osmdt.fetch(sequence['sequencenumber'], time='hour')
        data_object = osmdt.process(data_stream)

        users = osmdt.extract_users(data_object)

        conn = osmhm.connect.connect()

        for user in users:
            userid = users[user]['uid']
            username = user
            a_time = users[user]['timestamps'][0]
            a_time = convert_time(a_time)
		    
            cursor =  conn.cursor()
            cursor.execute("""DO $do$ BEGIN IF EXISTS (SELECT 1 FROM users WHERE username = %s) THEN 
		                      UPDATE users SET end_date = %s WHERE username = %s; ELSE
		                      INSERT INTO users (userid, username, start_date, end_date)
		                      VALUES (%s, %s, %s, %s); END IF; END $do$""",
		                      (username, a_time, username, userid, username, a_time, a_time))
            conn.commit()

            cursor.close()
            del cursor

        osmhm.inserts.insert_file_read()
        print "Finished processing %s." % (sequence['sequencenumber'])

    next_time = convert_time(sequence['timestamp']) + datetime.timedelta(minutes=60)

    if datetime.datetime.utcnow() < next_time:
        sleep_time = (next_time - datetime.datetime.utcnow()).seconds + 60
        print "Waiting %2.1f seconds for the next file." % (sleep_time)
    else:
        sleep_time = 0

    time.sleep(sleep_time)

    count = 0
    while True:
        try:
            count += 1
            osmhm.fetch.fetch_next(sequence['sequencenumber'], time_type='hour')
            break
        except:
            if count == 5:
                msg = 'New state file not retrievable after five times.'
                raise Exception(msg)
            print "Waiting %2.1f more seconds..." % (extra_time)
            time.sleep(extra_time)
