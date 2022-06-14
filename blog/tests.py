from django.test import TestCase
from .models import Post, Like
from last_active.models import LastActive
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import test, status
from datetime import date, timedelta, datetime
import json

client = test.APIClient()


# Test SEO settings, fields
class TestSEO(TestCase):

    def test_create_seo_fields(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='test_password')

        self.post = Post.objects.create(
            owner=self.user,
            title='Test post',
            content='Some content'
        )

        self.post.seo_object_type = 'object_type'
        self.post.seo_keywords = 'first, second, third'
        self.post.seo_img_height = 675
        self.post.seo_img_width = 250
        self.post.seo_index = 'seo_index'
        self.post.seo_follow = 'seo_follow'
        self.post.seo_canonical = 'seo_canonical'
        self.post.seo_title = 'seo_title'
        self.post.seo_og_title = 'seo_og_title'
        self.post.seo_description = 'seo_description'
        self.post.seo_h1 = 'seo_h1'
        self.post.seo_text = 'seo_text'
        self.post.seo_img_alt = 'seo_img_alt'

        self.assertEqual(self.post.seo_object_type, 'object_type')
        self.assertEqual(self.post.seo_keywords, 'first, second, third')
        self.assertEqual(self.post.seo_img_height, 675)
        self.assertNotEqual(self.post.seo_img_width, 200)
        self.assertEqual(self.post.seo_index, 'seo_index')
        self.assertNotEqual(self.post.seo_index, 'index')
        self.assertEqual(self.post.seo_follow, 'seo_follow')
        self.assertNotEqual(self.post.seo_canonical, 'canonical')
        self.assertEqual(self.post.seo_title, 'seo_title')
        self.assertEqual(self.post.seo_og_title, 'seo_og_title')
        self.assertEqual(self.post.seo_description, 'seo_description')
        self.assertEqual(self.post.seo_h1, 'seo_h1')
        self.assertEqual(self.post.seo_text, 'seo_text')
        self.assertEqual(self.post.seo_img_alt, 'seo_img_alt')


# Test all post properties and endpoints
class TestPost(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='test_password')

        client.force_authenticate(user=self.user)

        self.post = Post.objects.create(
            owner=self.user,
            title='Test post',
            content='Some content'
        )

        self.post2 = Post.objects.create(
            owner=self.user,
            title='Test post 2',
            content='More content'
        )

    # test different post fields
    def test_post_fields(self):
        posts = Post.objects.all()
        self.assertEqual(posts.count(), 2)
        self.assertNotEqual(Post.objects.get(title='Test post').title, 'First Test')
        self.assertEqual(Post.objects.first().owner, self.user)
        self.assertEqual(self.post.owner, self.post2.owner)

    # test endpoint which return list of all posts with pagination
    def test_get_all_posts(self):
        response = client.get(reverse('all-posts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_count'], 2)
        self.assertEqual(response.data['results'][0]['id'], 2)

    # test endpoint which return list a post by it ID
    def test_get_post(self):
        url = reverse('get-post', args=[self.post.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], 1)

    # test endpoint creation of post
    def test_create_post(self):
        self.assertEqual(Post.objects.all().count(), 2)
        data = {
            'owner': self.user.id,
            'title': 'new testing post title',
            'content': 'new post content'
        }
        response = client.post(reverse('create-post'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.all().count(), 3)


# Test like and unlike functionality
class TestLikePost(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='test_password')

        self.post = Post.objects.create(
            owner=self.user,
            title='Test post',
            content='Some content'
        )

        client.force_authenticate(user=self.user)

#  test post liking when functionality of like and dislike is different. Situation if post was not liked before
# Must be success status
    def test_like_post_success(self):
        self.assertEqual(Like.objects.all().count(), 0)
        url = reverse('like-post', args=[self.post.id])
        response = client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.all().count(), 1)

#  test post liking when functionality of like and dislike is different. Situation if post had already been liked
# Must be failure status
    def test_like_post_fail(self):
        url = reverse('like-post', args=[self.post.id])
        client.post(url, content_type='application/json')
        response = client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(Like.objects.all().count(), 1)

#  test post unliking when functionality of like and dislike is different. The situation when post was not
#  liked before. So must be failed status
    def test_unlike_post_fail(self):
        url = reverse('unlike-post', args=[self.post.id])
        response = client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

#  test post unliking when functionality of like and dislike is different. Must be successful status
    def test_unlike_post_success(self):
        url = reverse('like-post', args=[self.post.id])
        client.post(url, content_type='application/json')
        url = reverse('unlike-post', args=[self.post.id])
        response = client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# test like/unlike post if it the same button. Like
    def test_like_unlike_post_like(self):
        self.assertEqual(Like.objects.all().count(), 0)
        url = reverse('like-unlike-post', args=[self.post.id])
        response = client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.all().count(), 1)

# test like/unlike post if it the same button. Unlike
    def test_like_unlike_post_unlike(self):
        url = reverse('like-unlike-post', args=[self.post.id])
        client.post(url, content_type='application/json')
        url = reverse('like-unlike-post', args=[self.post.id])
        response = client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# test analytic endpoint for activity on two days
class TestAnalytic(TestCase):

    def test_analytic_for_two_days(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        url = reverse('analytic')
        url_ = f"{url}?date_from={yesterday}&date_to={today}"
        response = client.get(url_)
        self.assertEqual(response.status_code, 200)


class TestUserActivity(TestCase):
    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='test_password')

        LastActive.objects.create(
            user=self.user,
            site_id=1,
            last_active=datetime.now()
        )

# test user activity
    def test_user_activity(self):
        url = reverse('user-analytic', args=[self.user.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
