*Limited Infection v1.0*

Requirements: Python 3.4

Instructions:

* Creating users: Run `python infection.py --create *number_of_users*`
* If student A teaches student B: Run `python infection.py --link` *student_A_ID* *student_B_ID*
* To roll out a new version for a target number of students: Run `python infection.py --rollout` *number_of_students* *new_version_number* Note: The version number should be an integer.
* To see a print out of a user: Run `python infection.py --print` *user_ID*
* To reset the database: Run `python infection.py --reset`
* To run test cases: Run `python test.py`

Known issues:
* Data structure doesn't support multiple teachers.

Optimized for classrooms, where there is one teacher, and a large number of students. Rollout speed is inversely proportional to the number of student-teacher relationships.
