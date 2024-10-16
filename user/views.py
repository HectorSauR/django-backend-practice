# from django.shortcuts import render

from rest_framework.generics import (
    CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from user.models import User
from user.serializers import (
    CreateUserSerializer,
    UpdateUserSerializer,
    LoginSerializer,
    UserSerializer
)

from knox import views as knox_views

from django.contrib.auth import login
from django.db.models.query import QuerySet

from utils.order_utils import QuickSort
from utils.generate_users_pdf import generate_users_pdf
from django.http import HttpResponse


class ListUserAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset: QuerySet = User.objects.get_queryset()

        user = self.request.user

        if not user.is_superuser or not user.is_staff:
            return queryset.filter(id=user.id)

        query_params: dict = self.request.query_params
        try:
            age: int = query_params.get('age', None)
            if age is not None:
                queryset = queryset.filter(age=age)

            field: str = query_params.get('order', None)
            if field is not None:

                order = "asc"
                if field.lower().startswith('-'):
                    order = "desc"
                    field = field[1:].lower()

                quicksort = QuickSort(
                    list(queryset),
                    field,
                    order
                )
                queryset: list = quicksort.sort()

        except ValueError:
            pass

        return queryset


class RetrieveUsersPDFAPI(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_queryset(self):
        queryset: QuerySet = User.objects.get_queryset()

        user = self.request.user

        if not user.is_superuser or not user.is_staff:
            return queryset.filter(id=user.id)

        query_params: dict = self.request.query_params
        try:
            age: int = query_params.get('age', None)
            if age is not None:
                queryset = queryset.filter(age=age)

            field: str = query_params.get('order', None)
            if field is not None:

                order = "asc"
                if field.lower().startswith('-'):
                    order = "desc"
                    field = field[1:].lower()

                quicksort = QuickSort(
                    list(queryset),
                    field,
                    order
                )
                queryset: list = quicksort.sort()

        except ValueError:
            pass

        return queryset

    def retrieve(self, request, *args, **kwargs):
        data = self.get_queryset()
        pdf = generate_users_pdf({
            'users': data
        })

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="users_report.pdf"'

        return response


class CreateUserAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class UpdateUserAPI(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user.id != instance.id:
            raise PermissionDenied(
                "You do not have permissions to update this user.")

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteUserAPI(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(id=user.id)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if instance.is_superuser or instance.is_staff:
            raise PermissionDenied(
                "High privileged users cannot be removed.")

        if user.id != instance.id and not user.is_superuser:
            raise PermissionDenied(
                "You don't have perms to delete this user.")

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        response = super().post(request, format=None)

        return Response(response.data, status=status.HTTP_200_OK)
