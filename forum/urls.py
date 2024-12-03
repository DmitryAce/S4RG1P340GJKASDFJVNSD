from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'forums', ForumViewSet)
router.register(r'posts', PostViewSet)
router.register(r'ratings', RatingViewSet)



schema_view = get_schema_view(
    openapi.Info(
        title="Forum API",
        default_version="v1",
        description="API documentation for Forum, Post, Rating, and User operations.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/register/', RegisterView.as_view(), name='user-register'),
    path('users/login/', LoginView.as_view(), name='user-login'),
    path('users/logout/', LogoutView.as_view(), name='user-logout'),
    path('rating/update/', RatingUpdateView.as_view(), name='rating-update'),
    path('users/global-rating/<int:pk>/', GlobalRatingCreateUpdateView.as_view(), name='global-rating-create-update'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + router.urls