from django.urls import path
from .views import  Login, Logout, AllMessagesForUser, CreateNewMessage, AllUnreadMessagesForUser, ReadMessage, \
    RegisterAndShowUsers

urlpatterns = [
    path('register', RegisterAndShowUsers.as_view()),
    path('login', Login.as_view()),
    path('logout', Logout.as_view()),
    path('<str:user>/messages', AllMessagesForUser.as_view()),
    path('<str:user>/messages/unread', AllUnreadMessagesForUser.as_view()),
    path('<str:user>/create-message',CreateNewMessage.as_view()),
    path('<str:user>/messages/<int:pk>', ReadMessage.as_view()),
]
