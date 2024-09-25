import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Zermelo Utils')

    envtype = parser.add_subparsers(dest='env-type', required=True, help='Environment type')
    dotenvParser = envtype.add_parser('dotenv', help='Use .env file')
    dotenvParser.add_argument('dotenv', type=str, help='Path to .env file')
    argParser = envtype.add_parser('args', help='Use arguments')
    argParser.add_argument('school', type=str, help='School name (see Readme for instuctions)')
    argParser.add_argument('schoolYear', type=str, help='School year (see Readme for instuctions)')
    argParser.add_argument('authorization', type=str, help='Authorization token (see Readme for instuctions)')

    exectype = parser.add_subparsers(dest='exec-type', required=True, help='Execution type')

    importParser = exectype.add_parser('import', help='Import data from Zermelo API')
    importType = importParser.add_subparsers(dest='import-type', required=True, help='Import type')
    importType.add_parser('groups', help='Import groups')
    importType.add_parser('teachers', help='Import teachers')
    importType.add_parser('students', help='Import students')
    importType.add_parser('locations', help='Import locations')
    appointmentParser = importType.add_parser('appointments', help='Import appointments')
    appointmentParser.add_argument('user', type=str, help='User')
    appointmentParser.add_argument('startWeek', type=int, help='Start week')
    appointmentParser.add_argument('endWeek', type=int, help='End week')
    massAppointmentParser = importType.add_parser('appointments-mass', help='Import appointments for a range of users')
    massAppointmentParser.add_argument('startUser', type=int, help='Start user')
    massAppointmentParser.add_argument('endUser', type=int, help='End user')
    massAppointmentParser.add_argument('startWeek', type=int, help='Start week')
    massAppointmentParser.add_argument('endWeek', type=int, help='End week')
    allAppointmentParser = importType.add_parser('appointments-all', help='Import appointments for all users')
    allAppointmentParser.add_argument('startWeek', type=int, help='Start week')
    allAppointmentParser.add_argument('endWeek', type=int, help='End week')

    args = parser.parse_args()