# Limited Infection v1.0
# Benjamin Murphy
# benjaminmurphy on Github


import unittest, sqlite3

from infection import *

class TestSuite(unittest.TestCase):

    def setUp(self):
        conn = sqlite3.connect("unittest.db")
        curs = conn.cursor()
        setup(curs)

        self.curs = curs
        self.conn = conn

    def tearDown(self):
        self.conn.close()
        os.remove("unittest.db")
        self.conn = None
        self.curs = None

    def testCreate(self):
        createUser(20, self.curs)
        self.conn.commit()

        self.curs.execute("SELECT count(*) from USERS")
        size = int(self.curs.fetchone()[0])

        self.assertEqual(20, size)

        createUser(10, self.curs)
        self.conn.commit()

        self.curs.execute("SELECT count(*) from USERS")
        size = int(self.curs.fetchone()[0])

        self.assertEqual(30, size)

    def testLink(self):
        createUser(5, self.curs)

        link(0, 1, self.curs)
        link(0, 2, self.curs)
        link(0, 3, self.curs)
        link(3, 4, self.curs)

        self.conn.commit()

        userZero = getUser(0, self.curs)
        self.assertEqual(userZero, (0, 1, 0, " 1 2 3", ""))
        userThree = getUser(3, self.curs)
        self.assertEqual(userThree, (3, 1, 0, " 4", " 0"))

    def testRollout(self):
        createUser(10, self.curs)

        link(0, 1, self.curs)
        link(0, 2, self.curs)
        link(0, 3, self.curs)
        link(0, 4, self.curs)
        link(5, 6, self.curs)
        link(5, 7, self.curs)
        link(8, 9, self.curs)

        self.conn.commit()

        rollout(6, 2, self.curs) # Roll out version two to six users.

        userTwo = getUser(2, self.curs)
        self.assertEqual(userTwo, (2, 2, 0, "", " 0"))

        userEight = getUser(8, self.curs)
        self.assertEqual(userEight, (8, 2, 8, " 9", ""))

        userSix = getUser(6, self.curs)
        self.assertEqual(userSix, (6, 1, 5, "", " 5"))

if __name__ == "__main__":
    unittest.main()
