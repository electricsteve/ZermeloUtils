import ast

from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color
import sqlite3

from Classes.Group import Group
from Classes.Student import Student
from Classes.Teacher import Teacher
from Classes.Appointment import Appointment

appDbConn = sqlite3.connect('./appointments.db')
appDbCursor = appDbConn.cursor()

dbConn = sqlite3.connect('./database.db')
dbCursor = dbConn.cursor()

# Input variables
titleText = "Rooster voor week 69"
groupIds = ast.literal_eval(dbCursor.execute('SELECT groupInDepartments FROM STUDENTS WHERE student = \'[temp redacted]\' ').fetchone()[0])
groups = [Group.from_tuple(dbCursor.execute(f'SELECT * FROM GROUPS WHERE id = {groupId}').fetchone()) for groupId in groupIds]
appointments = []
for group in groups:
    appointments += appDbCursor.execute(f'SELECT * FROM \'45\' WHERE groupsInDepartments LIKE ?', (f"%{group.id}%",)).fetchall()
weekStartTimestamp = 1730674800

appointments = [Appointment.from_tuple(appointment) for appointment in appointments]
minTimeSlot = min([appointment.startTimeSlot for appointment in appointments])
maxTimeSlot = max([appointment.endTimeSlot for appointment in appointments])

print(minTimeSlot)
print(maxTimeSlot)

# Color Variables
titleColor = Color("white")
titleStrokeColor = Color("gray95")
titleTextColor = Color("black")
weekColor = Color("white")
weekStrokeColor = Color("gray95")
weekTextColor = Color("black")
dayColor = Color("gray90")
dayStrokeColor = Color("gray85")
dayTextColor = Color("black")
appointmentColor = Color("purple")
appointmentStrokeColor = Color("indigo")
appointmentTextColor = Color("black")

# Width and Height of the image
width = 1600
height = 1000

# Margins
appointmentMargin = 5
dayMargin = 5
weekMargin = 10
titleMarginTopBottom = 20
titleMarginLeftRight = 100

# Title Factor, how much of the image the title should take (including margin)
titleFactor = 0.15
titleFontSize = 50

# Calculate the height of the title
titleHeight = height * titleFactor

# Title

titleDrawing = Drawing()
titleDrawing.fill_color = titleColor
titleDrawing.stroke_color = titleStrokeColor

titleDrawing.rectangle(left=titleMarginLeftRight, top=titleMarginTopBottom, right=width - titleMarginLeftRight, bottom=titleHeight - titleMarginTopBottom, radius=10)

titleTextDrawing = Drawing()
titleTextDrawing.font_size = titleFontSize
titleTextDrawing.fill_color = titleTextColor
titleTextDrawing.text_alignment = "center"

titleTextDrawing.text(int(width / 2), int(titleHeight / 2 + titleFontSize / 3), titleText)

# Week

weekDrawing = Drawing()

weekDrawing.fill_color = weekColor
weekDrawing.stroke_color = weekStrokeColor

weekDrawing.rectangle(left=weekMargin, top=weekMargin + titleHeight, right=width-weekMargin, bottom=height-weekMargin, radius=10)

# Days
dayTitleSpace = 50
dayWidth = (width - 2 * weekMargin) / 5
dayHeight = height - titleHeight - 2 * weekMargin

appointmentHeight = (dayHeight - dayTitleSpace - 2 * dayMargin) / (maxTimeSlot - minTimeSlot + 1)

dayDrawing = Drawing()
dayDrawing.fill_color = dayColor
dayDrawing.stroke_color = dayStrokeColor

dayDrawingText = Drawing()
dayDrawingText.font_size = 20
dayDrawingText.fill_color = dayTextColor
dayDrawingText.text_alignment = "center"

appointmentDrawing = Drawing()
appointmentDrawing.fill_color = appointmentColor
appointmentDrawing.stroke_color = appointmentStrokeColor

appointmentTextDrawing = Drawing()
appointmentTextDrawing.font_size = 20
appointmentTextDrawing.fill_color = appointmentTextColor
appointmentTextDrawing.text_alignment = "center"

for i in range(5):
    dayStartTimestamp = weekStartTimestamp + i * 86400
    dayEndTimestamp = weekStartTimestamp + (i + 1) * 86400
    appointmentsOfDay = [appointment for appointment in appointments if dayStartTimestamp <= appointment.start < dayEndTimestamp]

    dayDrawing.rectangle(left=weekMargin + i * dayWidth + dayMargin, top=weekMargin + titleHeight + dayMargin, right=weekMargin + (i + 1) * dayWidth - dayMargin, bottom=height - weekMargin - dayMargin, radius=10)
    dayDrawingText.text(int(weekMargin + i * dayWidth + dayWidth / 2), int(weekMargin + titleHeight + dayMargin + dayTitleSpace / 2), "Day " + str(i + 1))

    for appointment in appointmentsOfDay:
        appointmentLocation = appointment.locationsOfBranch[0]
        appointmentLocationName = dbCursor.execute(f"SELECT name FROM LOCATIONS WHERE id = {appointmentLocation}").fetchone()[0]
        appointmentText = f"{str(appointment.startTimeSlot) + ((" - " + str(appointment.endTimeSlot)) if appointment.endTimeSlot != appointment.startTimeSlot else "")} - {appointment.subjects[0]} - {appointment.teachers[0]} - {appointmentLocationName} "
        appointmentStart = appointment.startTimeSlot
        appointmentEnd = appointment.endTimeSlot

        appointmentTop = titleHeight + weekMargin + dayMargin + dayTitleSpace + appointmentMargin + (appointmentStart - minTimeSlot) * appointmentHeight
        appointmentBottom = titleHeight + weekMargin + dayMargin + dayTitleSpace + (appointmentEnd - minTimeSlot + 1) * appointmentHeight - appointmentMargin

        appointmentDrawing.rectangle(left=weekMargin + i * dayWidth + dayMargin + appointmentMargin, top=appointmentTop, right=weekMargin + (i + 1) * dayWidth - dayMargin - appointmentMargin, bottom=appointmentBottom, radius=10)

        appointmentTextDrawing.text(int(weekMargin + i * dayWidth + dayWidth / 2), int(appointmentTop + (appointmentBottom - appointmentTop) / 2), appointmentText)

# Finalize

img = Image(width=width, height=height, format="png")
titleDrawing.draw(img)
titleTextDrawing.draw(img)
weekDrawing.draw(img)
dayDrawing.draw(img)
dayDrawingText.draw(img)
appointmentDrawing.draw(img)
appointmentTextDrawing.draw(img)
img.format = "PNG"
img.save(filename="schedule.png")
# display(img)