import unittest

import final_web


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = final_web.app.test_client()

    def tearDown(self):
        pass

    def test_home_page(self):
        # Render the / path of the website
        rv = self.app.get('/')
        # Chech that the page contians the desired phrase
        assert b'Final Project Website' in rv.data 

if __name__ == '__main__':
    unittest.main()
