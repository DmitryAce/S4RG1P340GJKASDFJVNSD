from rest_framework import viewsets, generics, permissions, status
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action

User = get_user_model()


class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.request.query_params.get('pk')
        if pk:
            return self.queryset.filter(pk=pk)
        return self.queryset

    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        try:
            forum = self.queryset.get(pk=pk)
        except Forum.DoesNotExist:
            return Response({"error": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(forum)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        try:
            forum = self.queryset.get(pk=pk)
            forum.delete()
            return Response({"message": "Forum deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Forum.DoesNotExist:
            return Response({"error": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.request.query_params.get('pk')
        if pk:
            return self.queryset.filter(pk=pk)
        return self.queryset

    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        try:
            post = self.queryset.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        try:
            post = self.queryset.get(pk=pk)
            post.delete()
            return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.request.query_params.get('pk')
        if pk:
            return self.queryset.filter(pk=pk)
        return self.queryset

    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        try:
            rating = self.queryset.get(pk=pk)
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(rating)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        try:
            rating = self.queryset.get(pk=pk)
            rating.delete()
            return Response({"message": "Rating deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found"}, status=status.HTTP_404_NOT_FOUND)



class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Возвращаем только текущего пользователя
        return self.request.user


# views.py
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        bio = data.get("bio", "")

        # Проверка, существует ли пользователь с таким именем
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Создание пользователя с хешированием пароля
        user = User.objects.create_user(username=username, email=email, password=password, bio=bio)

        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class RatingUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        score = request.data.get('score')  # Ожидаем значение +1 или -1
        
        # Находим пост
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, есть ли уже оценка для этого пользователя
        rating, created = Rating.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            rating.score = score  # Если оценка существует, просто обновляем
            rating.save()
        else:
            rating.score = score
            rating.save()

        return Response({"message": "Rating updated successfully"}, status=status.HTTP_200_OK)


class GlobalRatingCreateUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        # Получаем глобальный рейтинг пользователя по pk
        try:
            global_rating = GlobalRating.objects.get(user__pk=pk)
        except GlobalRating.DoesNotExist:
            raise NotFound(detail="Global rating not found for this user.")

        # Сериализуем данные и возвращаем их
        serializer = GlobalRatingSerializer(global_rating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        # Создаем новый глобальный рейтинг для пользователя, если его нет
        user = User.objects.get(pk=pk)

        global_rating, created = GlobalRating.objects.get_or_create(user=user)

        # Устанавливаем начальное значение рейтинга, если оно не было установлено
        global_rating.rating = 0  # начальное значение рейтинга
        global_rating.save()

        serializer = GlobalRatingSerializer(global_rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, *args, **kwargs):
        # Обновляем глобальный рейтинг пользователя по pk
        try:
            global_rating = GlobalRating.objects.get(user__pk=pk)
        except GlobalRating.DoesNotExist:
            raise NotFound(detail="Global rating not found for this user.")

        # Обновляем рейтинг, если новое значение указано в запросе
        new_rating = request.data.get('rating')
        if new_rating is not None:
            global_rating.rating = new_rating
            global_rating.save()

        serializer = GlobalRatingSerializer(global_rating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        # Удаление глобального рейтинга пользователя по pk
        try:
            global_rating = GlobalRating.objects.get(user__pk=pk)
        except GlobalRating.DoesNotExist:
            raise NotFound(detail="Global rating not found for this user.")

        global_rating.delete()
        return Response({"message": "Global rating deleted"}, status=status.HTTP_204_NO_CONTENT)