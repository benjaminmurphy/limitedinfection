# Limited Infection v1.0
# Benjamin Murphy
# benjaminmurphy on Github

import sqlite3, sys, os

DEFAULT = 1.0
DBNAME = "userbase.db"

def setup(curs):
    """Creates tables for a new database."""
    print("Creating database...")
    curs.execute("""CREATE TABLE USERS (ID INTEGER PRIMARY KEY, VERSION INTEGER,
        REPRESENTATIVE INTEGER, STUDENTS TEXT, COACHES TEXT);""")
    curs.execute("""CREATE TABLE REPRESENTATIVES (ID INTEGER PRIMARY KEY,
        SIZE INTEGER);""")

def createUser(num, curs):
    """Creates a number of users in the database."""
    curs.execute("SELECT count(*) from USERS")
    userId = int(curs.fetchone()[0])

    for _ in range(num):
        curs.execute("""INSERT INTO USERS (ID, VERSION, REPRESENTATIVE,
            STUDENTS, COACHES) VALUES (?, ?, ?, "", "");""",
            (userId, DEFAULT, userId))
        curs.execute("""INSERT INTO REPRESENTATIVES (ID, SIZE) VALUES
            (?, 1);""", (userId,))
        print("Created student {0}...".format(userId))
        userId += 1

def link(teacherId, studentId, curs):
    """Creates a teacher-student relationship given two ids."""
    teacher = getUser(teacherId, curs)
    student = getUser(studentId, curs)

    teacherRep = getRepresentative(teacher[2], curs)
    studentRep = getRepresentative(student[2], curs)

    curs.execute("UPDATE REPRESENTATIVES SET SIZE=? WHERE ID=?",
        (teacherRep[1] + studentRep[1], teacherRep[0]))

    curs.execute("DELETE FROM REPRESENTATIVES WHERE ID=?", (studentRep[0],))

    updateRepresentative(studentId, teacherRep[0], curs)

    newS = teacher[3] + " " + str(studentId)
    newC = student[4] + " " + str(teacherId)

    curs.execute("UPDATE USERS SET STUDENTS=? WHERE ID=?", (newS, teacherId))
    curs.execute("UPDATE USERS SET COACHES=? WHERE ID=?", (newC, studentId))

def updateRepresentative(oldRep, newRep, curs):
    """Updates a graph of users to a new representative."""
    curs.execute("UPDATE USERS SET REPRESENTATIVE=? WHERE REPRESENTATIVE=?",
        (newRep, oldRep))

def rollout(number, version, curs):
    """Updates a number of users to a version."""
    curs.execute("SELECT * FROM REPRESENTATIVES")
    repList = curs.fetchall()
    repList.sort(key = lambda rep: rep[1], reverse = True)
    convertedUsers = 0
    selectedRepresentatives = []

    while convertedUsers < 0.9 * number:
        for rep in repList:
            if convertedUsers + rep[1] < 1.1 * number:
                convertedUsers += rep[1]
                selectedRepresentatives.append(rep)
                repList.remove(rep)
                break
        else:
            convertedUsers += repList[-1][1]
            selectedRepresentatives.append(repList[-1])
            repList.remove(repList[-1])

    curs.executemany("UPDATE USERS SET VERSION=? WHERE REPRESENTATIVE=?",
        ([(version, rep[0]) for rep in selectedRepresentatives]))

def getUser(id, curs):
    """Returns the user with the given id."""
    curs.execute("SELECT * FROM USERS WHERE ID=?", (id,))
    return curs.fetchone()

def getRepresentative(id, curs):
    """Returns the representative with the given id."""
    curs.execute("SELECT * FROM REPRESENTATIVES WHERE ID=?", (id,))
    return curs.fetchone()

def printUser(id, curs):
    """Prints out the user with the given id."""
    u = getUser(id, curs)
    print("User {0} on {1}, Rep {2}, Students {3}, Coaches {4}".format(
        u[0], u[1], u[2], u[3], u[4]))

def main():
    arg = sys.argv[1:]
    setupNeeded = False

    if not os.path.isfile(DBNAME):
        setupNeeded = True

    conn = sqlite3.connect(DBNAME)
    curs = conn.cursor()

    if setupNeeded:
        setup(curs)

    while len(arg) > 0:
        if arg[0] in ("--create", "-c"):
            try:
                createUser(int(arg[1]), curs)
                conn.commit()
            except ValueError:
                conn.commit()
                conn.close()
                raise("--create must be followed by a number of users to create.")
            arg = arg[2:]

        elif arg[0] in ("--link", "-l"):
            try:
                link(int(arg[1]), int(arg[2]), curs)
                conn.commit()
            except ValueError:
                conn.commit()
                conn.close()
                raise("--create must be followed by two userIds.")
            arg = arg[3:]

        elif arg[0] in ("--rollout", "-r"):
            try:
                rollout(int(arg[1]), int(arg[2]), curs)
                conn.commit()
            except ValueError:
                conn.commit()
                conn.close()
                raise("--rollout must be followed by a number of users, and a new version.")
            arg = arg[3:]

        elif arg[0] in ("--print", "-p"):
            try:
                printUser(int(arg[1]), curs)
                conn.commit()
            except ValueError:
                conn.commit()
                conn.close()
                raise("--print must be followed by a userId.")
            arg = arg[2:]

        elif arg[0] == "--reset":
            os.remove(DBNAME)
            conn = sqlite3.connect(DBNAME)
            curs = conn.cursor()
            setup(curs)

        else:
            conn.commit()
            conn.close()
            raise("Unknown argument: %s", arg[0])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
