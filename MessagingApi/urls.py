from django.urls import include, path, re_path
from MessagingApi import views
urlpatterns = [
    path(r'Login/', views.UserLogin),
    path(r'WriteMessage/', views.WriteMessage),
    path(r'GetMyUnreadMessages/', views.GetMyUnreadMessages),
    path(r'GetMyMessages/', views.GetMyMessages),
    path(r'ReadMessage/', views.ReadMessage),
    path(r'DeleteMessage/<int:pk>/', views.DeleteMessage),

]