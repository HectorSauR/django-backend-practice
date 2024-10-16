from django.urls import path
from user.views import (CreateUserAPI, UpdateUserAPI,
                        ListUserAPI, DeleteUserAPI, RetrieveUsersPDFAPI)


urlpatterns = [
    path('', ListUserAPI.as_view(), name='list-users'),
    path('create/', CreateUserAPI.as_view(), name='create-user'),
    path('<int:pk>/update', UpdateUserAPI.as_view(), name='update-user'),
    path('<int:pk>/delete', DeleteUserAPI.as_view(), name='delete-user'),
    path('pdf', RetrieveUsersPDFAPI.as_view(), name='delete-user'),
]
