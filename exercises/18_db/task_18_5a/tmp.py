from datetime import timedelta, datetime
from pprint import pprint
import sqlite3

def clear_week_data(conn):
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)

    #query = 'SELECT * FROM dhcp WHERE last_active < ?'
    query = 'DELETE FROM dhcp WHERE last_active < ?'


#cursor = conn.cursor()

#cursor.execute(query, (week_ago, ))

#result_p = cursor.fetchall()

#pprint(result_p)
    conn.execute(query, (week_ago, ))
    conn.commit()

#---------------------------------------------------
conn = sqlite3.connect('dhcp_snooping.db')
clear_week_data(conn)
conn.close()
