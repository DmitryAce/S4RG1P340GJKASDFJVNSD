from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path

router = DefaultRouter()
router.register(r'forums', ForumViewSet)
router.register(r'posts', PostViewSet)
router.register(r'ratings', RatingViewSet)



urlpatterns = [
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/register/', RegisterView.as_view(), name='user-register'),
    path('users/login/', LoginView.as_view(), name='user-login'),
    path('users/logout/', LogoutView.as_view(), name='user-logout'),
    path('rating/update/', RatingUpdateView.as_view(), name='rating-update'),
    path('users/global-rating/<int:pk>/', GlobalRatingCreateUpdateView.as_view(), name='global-rating-create-update'),
] + router.urls