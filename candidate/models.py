# In your Django app's models.py file
from django.contrib.auth.models import User
from django.db import models

class Language(models.Model):
    language_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.language_name


class Resume(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resumes/')
    
class Candidate(models.Model):
    candidate_name = models.CharField(max_length=200, null=True, blank=True)
    candidate_family_name = models.CharField(max_length=200, null=True, blank=True)
    image=models.ImageField(upload_to="candidate",default="candidate/default.jpg")
    birth_date = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=255,null=True, blank=True)  
    about_me =models.TextField(blank=True)
    STATUS_CHOICES = [
        ('Student', 'Student'),
        ('Graduate', 'Graduate'),
        ('Working', 'Working'),
        ('Not working', 'Not working'),
        ('Other', 'Other'),
    ]  
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, null=True, blank=True)  
    salary_expectation = models.CharField(max_length=100, blank=True)
    language = models.ManyToManyField(Language)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    visible = models.BooleanField(default=1)
    
    def __str__(self):
        if self.candidate_name and self.candidate_family_name:
            return self.candidate_name + " " + self.candidate_family_name
        else:
                return "No value"

class WorkExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Degree(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    degree_type = models.CharField(max_length=100,null=True, blank=True)
    major = models.CharField(max_length=100,null=True, blank=True)
    institution = models.CharField(max_length=100,null=True, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        if self.degree_type and self.major:
            return f"{self.degree_type} in {self.major}"
        else:
            return "No value"

class ProfessionalSkills(models.Model):
    person = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    skill_detail = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.skill_detail}"

