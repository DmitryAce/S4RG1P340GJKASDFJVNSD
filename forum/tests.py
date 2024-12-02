from django.test import TestCase

# Create your tests here.
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Forum, Post, Rating, GlobalRating
from rest_framework import status


User = get_user_model()

@pytest.fixture
def another_authenticated_client(db):
    user = User.objects.create_user(username="another_user", password="password")
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def authenticated_client(api_client, create_user):
    user = create_user(username="testuser", password="testpassword")
    api_client.login(username="testuser", password="testpassword")
    return api_client, user

@pytest.fixture
def forum():
    return Forum.objects.create(name="Test Forum", description="Test Description")

@pytest.fixture
def post(forum, create_user):
    user = create_user(username="postuser", password="testpassword")
    return Post.objects.create(forum=forum, title="Test Post", content="Test Content", author=user)

@pytest.fixture
def rating(post, create_user):
    user = create_user(username="ratinguser", password="testpassword")
    return Rating.objects.create(post=post, user=user, score=1)

@pytest.fixture
def global_rating(create_user):
    user = create_user(username="globaluser", password="testpassword")
    return GlobalRating.objects.create(user=user, rating=10)


### Тесты для форума
@pytest.mark.django_db
def test_forum_list(authenticated_client, forum):
    client, _ = authenticated_client
    response = client.get("/api/forums/")
    assert response.status_code == 200
    assert response.data[0]["name"] == forum.name

@pytest.mark.django_db
def test_forum_detail(authenticated_client, forum):
    client, _ = authenticated_client
    response = client.get(f"/api/forums/{forum.id}/")
    assert response.status_code == 200
    assert response.data["name"] == forum.name

@pytest.mark.django_db
def test_forum_create(authenticated_client):
    client, _ = authenticated_client
    data = {"name": "New Forum", "description": "New Description"}
    response = client.post("/api/forums/", data)
    assert response.status_code == 201
    assert response.data["name"] == "New Forum"

@pytest.mark.django_db
def test_forum_update(authenticated_client, forum):
    client, _ = authenticated_client
    data = {"name": "Updated Forum", "description": "Updated Description"}
    response = client.put(f"/api/forums/{forum.id}/", data)
    assert response.status_code == 200
    assert response.data["name"] == "Updated Forum"

@pytest.mark.django_db
def test_forum_delete(authenticated_client, forum):
    client, _ = authenticated_client
    response = client.delete(f"/api/forums/{forum.id}/")
    assert response.status_code == 204
    assert Forum.objects.count() == 0


### Тесты для постов
@pytest.mark.django_db
def test_post_list(authenticated_client, post):
    client, _ = authenticated_client
    response = client.get("/api/posts/")
    assert response.status_code == 200
    assert response.data[0]["title"] == post.title

@pytest.mark.django_db
def test_post_detail(authenticated_client, post):
    client, _ = authenticated_client
    response = client.get(f"/api/posts/{post.id}/")
    assert response.status_code == 200
    assert response.data["title"] == post.title

@pytest.mark.django_db
def test_post_create(authenticated_client, forum):
    client, user = authenticated_client
    data = {"forum": forum.id, "title": "New Post", "content": "New Content", "author": user.id}
    response = client.post("/api/posts/", data)
    assert response.status_code == 201
    assert response.data["title"] == "New Post"

@pytest.mark.django_db
def test_post_update(authenticated_client, post):
    client, _ = authenticated_client
    data = {
        "title": "Updated Post",
        "content": "Updated Content",
        "author": 1,
        "forum": 1
    }
    response = client.put(f"/api/posts/{post.id}/", data)
    assert response.status_code == 200, f"Response: {response.data}"
    assert response.data["title"] == "Updated Post"

@pytest.mark.django_db
def test_post_delete(authenticated_client, post):
    client, _ = authenticated_client
    response = client.delete(f"/api/posts/{post.id}/")
    assert response.status_code == 204
    assert Post.objects.count() == 0


### Тесты для рейтинга
@pytest.mark.django_db
def test_rating_update(authenticated_client, post):
    client, user = authenticated_client
    data = {"post_id": post.id, "score": 1}
    response = client.post("/api/rating/update/", data)
    assert response.status_code == 200
    assert Rating.objects.filter(user=user, post=post).exists()


### Тесты для глобального рейтинга
@pytest.mark.django_db
def test_global_rating_get(authenticated_client, global_rating):
    client, _ = authenticated_client
    response = client.get(f"/api/users/global-rating/{global_rating.user.id}/")
    assert response.status_code == 200
    assert response.data["rating"] == global_rating.rating

@pytest.mark.django_db
def test_global_rating_update(authenticated_client, global_rating):
    client, _ = authenticated_client
    data = {"rating": 20}
    response = client.put(f"/api/users/global-rating/{global_rating.user.id}/", data)
    assert response.status_code == 200
    assert response.data["rating"] == 20

@pytest.mark.django_db
def test_post_creation_with_invalid_data(authenticated_client):
    """Тест создания поста с некорректными данными."""
    client, _ = authenticated_client
    invalid_data = {"title": "", "content": "Missing title"}
    response = client.post("/api/posts/", invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.data, "Отсутствует ошибка для поля title"


@pytest.mark.django_db
def test_user_profile_retrieve(authenticated_client):
    """Тест получения данных профиля пользователя."""
    client, user = authenticated_client
    response = client.get(f"/api/users/{user.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username