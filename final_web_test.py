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
    
    def test_my_topic(self):
        # Replace '/' with the page path you want to make
        rv = self.app.get('/practice')  
        # Replace UNH698 Website with the text you expect to see on you topi$
        assert b'YOGA PRACTICE' in rv.data 

    def test_poses(self):
        # Replace '/' with the page path you want to make
        rv = self.app.get('/poses')  
        # Replace UNH698 Website with the text you expect to see on you topi$
        assert b'bandha techniques' in rv.data 

if __name__ == '__main__':
    unittest.main()
