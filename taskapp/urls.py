from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

app_name = 'taskapp'
urlpatterns = [
    path('', views.IndexView, name='IndexView'),
    # url for logging in, links in views and login.html
    path("login/", views.login_request, name="login"),
    # url for registering, links in views and register.html
    path('register/', views.register_request, name="register"),

    path('logout/', views.logout_view, name='logout'),
    # create a task
    path('create-task', views.createTask, name='createTask'),
    # dashboard page
    path('dashboard', views.dashboard, name='dashboard'),
    # when you want to view task
    path('view_task', views.viewTask, name='viewTask'),
    # when you want to update a task
    path('update_task/<str:pk>/', views.update_task, name='update_task'),
    # this is to delete task and pk identifying it with the primary key
    path('delete/<str:pk>/', views.deleteTask, name='deleteTask'),
    # admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
