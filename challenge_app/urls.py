from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
urlpatterns = []
urlpatterns = [
    path('<int:id_challenge>/', views.get_leaderboard, name='leaderboard'),
    path('upload/<int:id_challenge>/', views.upload_file, name='upload'),
    path('', views.show_all_challenges, name='challenges'),
    path('login', views.login_view, name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='challenges'),name='logout')
]
try:
    if settings.MAINTENANCE_MODE == True:
        urlpatterns.insert(0,re_path('^.*$',views.maintenance,name='maintenance'))
except AttributeError:
    pass

        

