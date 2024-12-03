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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()


class ForumViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления форумами.
    Позволяет создавать, читать, обновлять и удалять записи о форумах.
    """
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение списка всех форумов или поиск форума по ID.",
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_QUERY,
                description="ID форума для фильтрации (опционально).",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение списка форумов.",
                schema=ForumSerializer(many=True)
            ),
            403: openapi.Response(description="Доступ запрещен.")
        },
    )
    def get_queryset(self):
        """
        Возвращает список форумов. Если указан параметр `pk`, возвращает конкретный форум.
        """
        pk = self.request.query_params.get('pk')
        if pk:
            return self.queryset.filter(pk=pk)
        return self.queryset

    @swagger_auto_schema(
        operation_description="Получение детальной информации о форуме по ID.",
        responses={
            200: openapi.Response(
                description="Детальная информация о форуме.",
                schema=ForumSerializer()
            ),
            404: openapi.Response(description="Форум не найден."),
            403: openapi.Response(description="Доступ запрещен.")
        },
    )
    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        """
        Возвращает детальную информацию о форуме по его ID.
        """
        try:
            forum = self.queryset.get(pk=pk)
        except Forum.DoesNotExist:
            return Response({"error": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(forum)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Удаление форума по ID.",
        responses={
            204: openapi.Response(description="Форум успешно удален."),
            404: openapi.Response(description="Форум не найден."),
            403: openapi.Response(description="Доступ запрещен.")
        },
    )
    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        """
        Удаляет форум по его ID.
        """
        try:
            forum = self.queryset.get(pk=pk)
            forum.delete()
            return Response({"message": "Forum deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Forum.DoesNotExist:
            return Response({"error": "Forum not found"}, status=status.HTTP_404_NOT_FOUND)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления постами.
    Позволяет создавать, читать, обновлять и удалять записи о постах.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение списка всех постов или поиск поста по ID.",
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_QUERY,
                description="ID поста для фильтрации (опционально).",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение списка постов.",
                schema=PostSerializer(many=True)
            ),
            403: openapi.Response(description="Доступ запрещен.")
        },
    )
    def get_queryset(self):
        """
        Возвращает список постов. Если указан параметр `pk`, возвращает конкретный пост.
        """
        pk = self.request.query_params.get('pk')
        if pk:
            return self.queryset.filter(pk=pk)
        return self.queryset

    @swagger_auto_schema(
        operation_description="Получение детальной информации о посте по ID.",
        responses={
            200: openapi.Response(
                description="Детальная информация о посте.",
                schema=PostSerializer()
            ),
            404: openapi.Response(description="Пост не найден."),
            403: openapi.Response(description="Доступ запрещен.")
        },
    )
    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        """
        Возвращает детальную информацию о посте по его ID.
        """
        try:
            post = self.queryset.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Удаление поста по ID.",
        responses={
            204: openapi.Response(description="Пост успешно удален."),
            404: openapi.Response(description="Пост не найден."),
            403: openapi.Response(description="Доступ запрещен.")
        },
    )
    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        """
        Удаляет пост по его ID.
        """
        try:
            post = self.queryset.get(pk=pk)
            post.delete()
            return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


class RatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления рейтингами.
    Позволяет выполнять CRUD-операции над записями рейтингов.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение списка всех рейтингов или поиск рейтинга по ID.",
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_QUERY,
                description="ID рейтинга для фильтрации (опционально).",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение списка рейтингов.",
                schema=RatingSerializer(many=True)
            ),
            403: openapi.Response(description="Доступ запрещен."),
        },
    )
    def get_queryset(self):
        """
        Возвращает список рейтингов. Если указан параметр `pk`, возвращает конкретный рейтинг.
        """
        pk = self.request.query_params.get('pk')
        if pk:
            return self.queryset.filter(pk=pk)
        return self.queryset

    @swagger_auto_schema(
        operation_description="Получение детальной информации о рейтинге по ID.",
        responses={
            200: openapi.Response(
                description="Детальная информация о рейтинге.",
                schema=RatingSerializer()
            ),
            404: openapi.Response(description="Рейтинг не найден."),
            403: openapi.Response(description="Доступ запрещен."),
        },
    )
    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        """
        Возвращает детальную информацию о рейтинге по его ID.
        """
        try:
            rating = self.queryset.get(pk=pk)
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(rating)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Удаление рейтинга по ID.",
        responses={
            204: openapi.Response(description="Рейтинг успешно удален."),
            404: openapi.Response(description="Рейтинг не найден."),
            403: openapi.Response(description="Доступ запрещен."),
        },
    )
    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        """
        Удаляет рейтинг по его ID.
        """
        try:
            rating = self.queryset.get(pk=pk)
            rating.delete()
            return Response({"message": "Rating deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Rating.DoesNotExist:
            return Response({"error": "Rating not found"}, status=status.HTTP_404_NOT_FOUND)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Представление для получения и обновления данных текущего пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение информации о текущем пользователе.",
        responses={
            200: openapi.Response(
                description="Успешное получение информации о пользователе.",
                schema=UserSerializer()
            ),
            403: openapi.Response(description="Доступ запрещен."),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Возвращает данные текущего пользователя.
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновление информации текущего пользователя.",
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                description="Информация пользователя успешно обновлена.",
                schema=UserSerializer()
            ),
            400: openapi.Response(description="Ошибка в запросе."),
            403: openapi.Response(description="Доступ запрещен."),
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Обновляет данные текущего пользователя.
        """
        return super().put(request, *args, **kwargs)

    def get_object(self):
        """
        Возвращает текущего аутентифицированного пользователя.
        """
        return self.request.user


class LoginView(APIView):
    """
    Представление для аутентификации пользователя.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Аутентификация пользователя по логину и паролю.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Имя пользователя."
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Пароль пользователя."
                ),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Успешный вход пользователя.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об успешном входе."
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Неверные учетные данные.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об ошибке."
                        )
                    }
                )
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Аутентифицирует пользователя по имени пользователя и паролю.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Представление для выхода пользователя из системы.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Выход текущего пользователя из системы.",
        responses={
            200: openapi.Response(
                description="Успешный выход пользователя.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение о завершении сессии."
                        )
                    }
                )
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Завершает текущую сессию пользователя.
        """
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    Представление для регистрации нового пользователя.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Уникальное имя пользователя."
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Электронная почта пользователя."
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Пароль пользователя."
                ),
                'bio': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Краткая информация о пользователе (опционально).",
                    default=""
                ),
            },
            required=['username', 'email', 'password']
        ),
        responses={
            201: openapi.Response(
                description="Пользователь успешно зарегистрирован.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об успешной регистрации."
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка запроса (например, имя пользователя уже существует).",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Описание ошибки."
                        )
                    }
                )
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Создает нового пользователя на основе переданных данных.
        """
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
    """
    Представление для обновления рейтинга поста.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Обновление рейтинга для поста (положительная или отрицательная оценка).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Идентификатор поста, который оценивается."
                ),
                'score': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Оценка: +1 или -1."
                ),
            },
            required=['post_id', 'score']
        ),
        responses={
            200: openapi.Response(
                description="Рейтинг успешно обновлен.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение об успешном обновлении рейтинга."
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Пост не найден.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Сообщение о том, что пост не найден."
                        )
                    }
                )
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Обновляет или создает рейтинг для указанного поста.
        """
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
    """
    Представление для управления глобальным рейтингом пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """
        Получение глобального рейтинга пользователя по идентификатору.
        """
        try:
            global_rating = GlobalRating.objects.get(user__pk=pk)
        except GlobalRating.DoesNotExist:
            raise NotFound(detail="Global rating not found for this user.")

        serializer = GlobalRatingSerializer(global_rating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        """
        Создание записи глобального рейтинга пользователя, если её не существует.
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.")

        global_rating, created = GlobalRating.objects.get_or_create(user=user)

        if created:
            global_rating.rating = 0  # Устанавливаем начальное значение рейтинга
            global_rating.save()

        serializer = GlobalRatingSerializer(global_rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, *args, **kwargs):
        """
        Обновление глобального рейтинга пользователя.
        """
        try:
            global_rating = GlobalRating.objects.get(user__pk=pk)
        except GlobalRating.DoesNotExist:
            raise NotFound(detail="Global rating not found for this user.")

        new_rating = request.data.get('rating')
        if new_rating is not None:
            global_rating.rating = new_rating
            global_rating.save()

        serializer = GlobalRatingSerializer(global_rating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        """
        Удаление записи глобального рейтинга пользователя.
        """
        try:
            global_rating = GlobalRating.objects.get(user__pk=pk)
        except GlobalRating.DoesNotExist:
            raise NotFound(detail="Global rating not found for this user.")

        global_rating.delete()
        return Response({"message": "Global rating deleted"}, status=status.HTTP_204_NO_CONTENT)
