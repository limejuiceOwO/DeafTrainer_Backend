from django.urls import path,include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'logs', views.LogViewSet, basename='log')

urlpatterns = [
    path('',include(router.urls)),
    path('profile',views.ProfileView.as_view()),
    path('profile/upload_avatar',views.AvatarUploadView.as_view()),
    path('homepage',views.HomepageView.as_view()),
]
'''
urlpatterns = [
    #path('user', views.user, name='user'),#GET/PUT
    path('user/log/', views.LogListView.as_view(), name='log_list'),#GET/POST
    #path('user/log/ofbook/<str:book_id>', views.logs_of_book, name='logs_of_book'),
    path('user/log/<str:log_id>', views.LogQueryView.as_view(), name='log_query'),#GET/DELETE
    path('user/avatar', views.AvatarView.as_view(), name='avatar'),#GET/POST
    #path('user/lesson', views.lesson, name='lesson'),#GET(last)/POST(new)

   	path('book/', views.BookListView.as_view(), name='book_list'),#GET
    path('book/<str:book_id>', views.BookQueryView.as_view(), name='book_query'),#GET
    #path('book/<str:book_id>/thumbnail', views.book_thumbnail, name='book_thumbnail'),
    #path('book/<str:book_id>/<int:page_index>', views.getpage, name='get_book_page'),#GET

    ### Non-RESTful apis
    path('auth/login', views.LoginView.as_view(),name='login'),#POST
    path('auth/logout', views.LogoutView.as_view(),name='logout'),#POST
    path('auth/renew', views.RenewView.as_view(),name='renew'),#POST

    path('test',views.test),

    #path('register', views.register, name='register'),
    #path('revoke', views.revoke_password, name='revoke_password'),

]
'''