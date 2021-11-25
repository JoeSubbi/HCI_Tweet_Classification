from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('judge/', views.judge, name='judge'),
    path('stats/<tweet_id>/', views.stats, name = 'stats'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout',)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)