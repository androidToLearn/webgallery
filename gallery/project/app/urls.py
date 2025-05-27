from django.urls import path
from app import views

urlpatterns = [
    path('page1/', views.index1, name='index1'),
    path('pageImage/', views.pageImage, name='imagePage'),
    path('', views.loginPage, name='loginPage'),
    path('getImage/', views.getImage, name='getImage'),
    path('custom404/', views.custom404, name='custom404'),
    path('to_change_password/<int:isForget>/', views.to_change_password,
         name='to_change_password'),
    path('moveToChangePassword/', views.moveToChangePassword,
         name='moveToChangePassword'),
    path('send/<int:isForget>', views.sendEmailWithJsonToNextPage,
         name='send'),
    path('index1_new_user/', views.index1_new_user, name='index1_new_user'),
    path('share_image/', views.share_image, name='share_image'),
    path('download/', views.download, name='download'),
    path('moveToChangePassword1/', views.we, name='moveToChangePassword1'),
    path('to_favorite/', views.to_favorite, name='favorite'),
    path('change_password/', views.change_password, name='changeP'),
    path('loginPageNew/', views.loginPageNew, name='loginPageNew'),
    path('to_delete/', views.to_delete, name='to_delete'),
]
