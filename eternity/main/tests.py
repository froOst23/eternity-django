from django.test import TestCase, Client
from main.models import User, Profile, Post
from django.contrib.auth import get_user_model

# Create your tests here.
class CreateUserTest(TestCase):
    def setUp(self):
        User = get_user_model()
        # создаем тестового пользователя - 1
        testUser1 = User.objects.create(is_superuser=False,
                            password='p@ssw0rd',
                            username='testUser1',
                            email='testUser@gmail.com',
                            first_name='userFirstName',
                            last_name='userLastName')
        # создаем тестового пользователя - 2
        testUser2 = User.objects.create(is_superuser=False,
                            password='p@ssw0rd',
                            username='testUser2',
                            email='testUser@gmail.com',
                            first_name='userFirstName',
                            last_name='userLastName')

        testPost = Post.objects.create(author=testUser1, title='testPostTitle', tag='testTag', content='testContent')


    def testUserParam(self):
        # выполняем проверку тестового пользователя - 1
        testUser1 = User.objects.get(username='testUser1')
        self.assertEquals(testUser1.username, 'testUser1')
        self.assertEquals(testUser1.password, 'p@ssw0rd')
        self.assertEquals(testUser1.email, 'testUser@gmail.com')
        self.assertEquals(testUser1.first_name, 'userFirstName')
        self.assertEquals(testUser1.last_name, 'userLastName')
        # выполняем проверку расширенной модели тестового пользователя - 1
        testUserExtended1 = Profile.objects.get(user=testUser1)
        testUserExtended1.bio = 'testUserBio'
        self.assertEquals(testUserExtended1.bio, 'testUserBio')
        
        # выполняем проверку тестового пользователя - 2
        testUser2 = User.objects.get(username='testUser2')
        self.assertEquals(testUser2.username, 'testUser2')
        self.assertEquals(testUser2.password, 'p@ssw0rd')
        self.assertEquals(testUser2.email, 'testUser@gmail.com')
        self.assertEquals(testUser2.first_name, 'userFirstName')
        self.assertEquals(testUser2.last_name, 'userLastName')
        # выполняем проверку расширенной модели тестового пользователя - 2
        testUserExtended2 = Profile.objects.get(user=testUser2)
        testUserExtended2.bio = 'testUserBio'
        self.assertEquals(testUserExtended2.bio, 'testUserBio')
