import sqlite3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'Classes'))
from Group import Group

import Zermelo

list_of_groups = Zermelo.get_groups()

print("Number of groups: ", len(list_of_groups))
# Create a connection to the database
conn = sqlite3.connect('./database.db')
c = conn.cursor()



c.execute("DROP TABLE IF EXISTS GROUPS")
table = """ CREATE TABLE GROUPS (
    id INTEGER PRIMARY KEY,
    isMainGroup BOOLEAN,
    isMentorGroup BOOLEAN,
    departmentOfBranch INTEGER,
    name TEXT,
    extendedName TEXT
        ); """
c.execute(table)

for group in list_of_groups:
    groupObject = Group(group)
    c.execute("INSERT INTO GROUPS VALUES (?, ?, ?, ?, ?, ?)", groupObject.to_tuple())
    print(groupObject)

conn.commit()
conn.close()