from django.urls import path
from .views import *

app_name ="employer"

urlpatterns = [
    path("post-a-job/", postjob ,name="post-a-job"),
   
]
