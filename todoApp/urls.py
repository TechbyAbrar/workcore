from django.urls import path
from .views import homepage, loginway, signupway, corepage, task_update, delete_task, logout_way


urlpatterns = [
    path('',homepage, name='home'),
    path('signup/', signupway, name='signup'),
    path('login/', loginway, name='login'),
    path('logout/', logout_way, name='logout_way'),
    path('corepage/', corepage, name='corepage'),
    path('taskupdate/<int:sn>/', task_update, name='taskupdate'),
    path('delete_task/<int:sn>', delete_task, name='delete_task'),
]
