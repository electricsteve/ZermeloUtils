import sqlite3
import sys
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
from Classes.Location import Location

import Zermelo

list_of_locations = Zermelo.get_locations()

print("Number of locations: ", len(list_of_locations))
# Create a connection to the database
conn = sqlite3.connect('../database.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS LOCATIONS")
# Types: id : int, name : string, parentteachernightCapacity : int, courseCapacity : int, supportsConcurrentAppointments : bool, allowMeetings : bool, branchOfSchool : int, secondaryBranches : list, schoolInSchoolYear : int
table = """ CREATE TABLE LOCATIONS (
    id integer PRIMARY KEY,
    name text NOT NULL,
    parentteachernightCapacity integer,
    courseCapacity integer,
    supportsConcurrentAppointments boolean,
    allowMeetings boolean,
    branchOfSchool integer,
    secondaryBranches text,
    schoolInSchoolYear integer
        ); """
c.execute(table)

for location in list_of_locations:
    locationObject = Location(location)
    c.execute("INSERT INTO LOCATIONS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", locationObject.to_tuple())
    print(locationObject)

conn.commit()
conn.close()