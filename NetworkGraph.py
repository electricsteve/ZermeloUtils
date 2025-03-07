from cProfile import label

import plotly.offline

from Classes import Utils
from dash import Dash, html, callback, Input, Output
import dash_cytoscape as cyto

from Classes.Student import Student

cyto.load_extra_layouts()

groups = Utils.getGroups()

groupList = ["redacted"]

groupsIWant = []
for group in groups:
    if group.departmentOfBranch == "redacted":
        groupsIWant.append(group)

students = []
for group in groupsIWant:
    students += Utils.getStudentsInGroup(group.id)

studentNodeData = [(student.student, student.fullName, student.mainGroup) for student in students]

studentNodes = [
    {
        'data': {'id': short, 'label': label, 'parent': str(mainGroup)},
        'classes': 'student'
    }
    for short, label, mainGroup in studentNodeData
]

mainGroups = set()

for student in students:
    mainGroups.add([group for group in groups if group.id == student.mainGroup][0])

mainGroupNodes = [
    {
        'data': {'id': str(group.id), 'label': group.extendedName}
    }
    for group in mainGroups
]

groupsIWant = [group for group in groupsIWant if group not in mainGroups]

groupNodes = [
    {
        'data': {'id': str(group.id), 'label': group.extendedName},
        'classes': 'group'
    }
    for group in groupsIWant
]

groupEdgeData = [(str(group.id), student.student) for student in students for group in groupsIWant if group.id in student.groupInDepartments]

edges = [
    {
        'data': {'source': edge[0], 'target': edge[1]}
    }
    for edge in groupEdgeData
]

elements = studentNodes + groupNodes + edges + mainGroupNodes

defaultStyleSheet = [
    {
        'selector': 'node',
        'style': {'content': 'data(label)'}
    },
    {
        'selector': '.group',
        'style': {
            'label': 'data(label)',
            'background-color': '#0024FF'
        }
    },
    {
        'selector': '.student',
        'style': {
            'label': 'data(label)',
            'background-color': '#FF0000'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': 'rgb(150, 150, 150)',
            'line-opacity': 0.05
        }
    },
    {
        'selector': ':selected',
        'style': {
            'background-color': '#FFD500',
            'line-color': '#FFD500'
        }
    }
]

app = Dash()

app.layout = html.Div([
    cyto.Cytoscape(
        id='studentGraph',
        layout={
            'name': 'cose-bilkent',
            'quality': 'proof',
            'nodeDimensionsIncludeLabels': True,
            'fit': True,
            'idealEdgeLength': 100,
            'edgeElasticity': 0.001,
            'padding': 20,
            # 'animate': False,
            # 'random': True,
            # 'fit': False,
            # 'gravity': 0.5,
            # 'nodeRepulsion': 400000,
            # 'edgeElasticity': 1000,
            # 'idealEdgeLength': 100,
            # 'initialTemp': 20,
            # 'nodeOverlap': 20,
        },
        style={'width': '100vw', 'height': '100vh'},
        elements=elements,
        stylesheet=defaultStyleSheet
    )
])


if __name__ == '__main__':
    app.run(debug=True)
