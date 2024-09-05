from django.urls import path
from .views import *

app_name ="candidate"

urlpatterns = [
    path("browsejobs/",browsejobs,name="browsejobs"),
    path("candidates/",candidates,name="candidates"),
    path("candidates/<int:pid>",candidate_single,name="candidate_single"),
    path("create_resume/",createresume,name="create_resume"),
    path('upload_resume/', upload_resume, name='upload_resume'),
    path("result/",result,name="result"),
    path("upload_resume_result/",upload_resume_result,name="upload_resume_result"),
    path("want-a-job/",wantajob,name="want-a-job"),
]
