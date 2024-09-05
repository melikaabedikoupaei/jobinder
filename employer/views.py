from django.shortcuts import render
from django.http import HttpResponse

def postjob (request):
    return render (request,"employer/post-a-job.html") 
