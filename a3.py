import psycopg

def connect_to_db():
    connection = None

    try:
        print('Connecting to the database...')
        
        username = input("Enter username for database (default is 'postgres'): ")
        password = input("Enter password for database (default is 'password'): ")
        host = input("Enter host for database (default is 'localhost'): ")

        connection = psycopg.connect(f"dbname=a3q1_db user={username} password={password} host={host}")

    except psycopg.OperationalError as e:
        print(f"Error: {e}")

    print('Connection successful')
    return connection

def getAllStudents(connection):
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        
        for student in students:
            print(student)

        cursor.close()
    else:
        print('Connection failed')

def addStudent(first_name, last_name, email, enrollment_date, connection):
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);", (first_name, last_name, email, enrollment_date))
        connection.commit()
        
        print("Student added successfully")
        
        cursor.close()
    else:
        print('Connection failed')

def updateStudentEmail(student_id, new_email, connection):
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET email = %s WHERE student_id = %s;", (new_email, student_id))
        connection.commit()
        
        print("Student email updated successfully")
        
        cursor.close()
    else:
        print('Connection failed')

def deleteStudent(student_id, connection): 
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        connection.commit()
        
        print("Student deleted successfully")
        
        cursor.close()
    else:
        print('Connection failed')

if __name__ == '__main__':
    connection = connect_to_db()

    # Show current student directory
    print("Displaying current student directory:")
    getAllStudents(connection)

    # Register a new student to the database
    while True:
        print("Registering a new student...")

        try:
            firstName = input("Enter first name for new student: ")
            lastName = input("Enter last name for new student: ")
            email = input("Enter email for new student: ")
            enrollmentDate = input("Enter enrollment date for new student (YYYY-MM-DD): ")

            addStudent(firstName, lastName, email, enrollmentDate, connection)
            print(f"Registration complete: {firstName} {lastName}.")
            break
        except psycopg.Error as e:
            print(f"Error: {e}: Please try again.")
            connection.rollback()

    # Refresh and display the updated student directory
    print("Refreshing student directory...")
    getAllStudents(connection)

    # Apply email update to a student's record
    print("Initiating email update for a student...")

    while True:
        try:
            studentId = input("Enter ID for student to update the email of: ")
            newEmail = input("Enter new email for student: ")

            updateStudentEmail(studentId, newEmail, connection)
            print(f"Email update applied: Student {studentId} now has email {newEmail}.")
            break
        except psycopg.Error as e:
            print(f"Error: {e}: Please try again.")
            connection.rollback()

    # Re-display the student directory to reflect the email update
    print("Displaying updated student directory:")
    getAllStudents(connection)

    while True:
        try:
            # Proceed to remove a student from the database
            print("Removing a student from the database...")
            studentIdToRemove = input("Enter the ID of the student to be removed: ")
            deleteStudent(studentIdToRemove, connection)
            print(f"Removal successful: Student ID {studentIdToRemove}.")
            break
        except psycopg.Error as e:
            print(f"Error: {e}: Please try again.")
            connection.rollback()

    # Final display of student directory after removal
    print("Final view of the student directory:")
    getAllStudents(connection)

    connection.close()