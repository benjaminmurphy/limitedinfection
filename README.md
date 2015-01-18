*Limited Infection v1.0*

Requirements: Python 3.4

Instructions:

* Creating users: Run `python infection.py --create number_of_users` (Or `-c`)
* If student A teaches student B: Run `python infection.py --link student_A_ID student_B_ID` (Or `-l`)
* To roll out a new version for a target number of students: Run `python infection.py --rollout number_of_students new_version_number` (Or `-r`) Note: The version number should be an integer.
* To see a print out of a user: Run `python infection.py --print user_ID` (Or `-p`)
* To reset the database: Run `python infection.py --reset`
* To run test cases: Run `python test.py`

Known issues:
* Data structure doesn't support multiple teachers.

Optimized for classrooms, where there is one teacher, and a large number of students. Rollout speed is inversely proportional to the number of student-teacher relationships.

Example:
    python infection.py --create 5
    python infection.py --link 0 1
    python infection.py --link 0 2
    python infection.py -l 2 3

    python infection.py --rollout 3 2
    python infection.py --print 0 # Should print (0, 2, 0, " 1 2", "")
    python infection.py --reset```
