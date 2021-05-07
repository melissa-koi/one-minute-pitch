import unittest
from app.models import Post

class Post(unittest.TestCase):

    def setUp(self):
        self.post = Post(10,'post','comment','interview pitch','author',1,1)

    def test_instance(self):
        self.assertTrue(isinstance(self.post,Post))