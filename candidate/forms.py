# forms.py
from django import forms
from .models import Candidate, Degree,WorkExperience,ProfessionalSkills,Resume

class CandidateForm(forms.ModelForm):
    

    class Meta:

        model = Candidate
        fields = '__all__'

        widgets = {
            'candidate_name': forms.TextInput(attrs={'title': 'First name',"class":"form-control" }),
            'candidate_family_name': forms.TextInput(attrs={'title': 'Last Name',"class":"form-control"}),
            'image': forms.FileInput(attrs={'title': 'image',"class":"form-control","placeholder":""}),
            'gender': forms.RadioSelect(attrs={'title': 'Gender'}),
            'birth_date': forms.DateInput(attrs={'title': 'Age',"class":"form-control"}),
            'location': forms.Textarea(attrs={'title': 'Location',"rows":1,"class":"form-control"}),
            'language' :forms.CheckboxSelectMultiple(attrs={'title': 'language'}),
            'email': forms.EmailInput(attrs={'title': 'Email'}),
            'github_profile': forms.URLInput(attrs={'title': 'Github'}),
            'linkedin_profile': forms.URLInput(attrs={'title': 'LinkedIn'})
        }


class DegreeForm(forms.ModelForm):

    class Meta:
        model = Degree
        fields = ('degree_type', 'major', 'graduation_year', 'institution')
        widgets = {
            'degree_type': forms.TextInput(attrs={'title': 'degree_type'}),
            'major': forms.TextInput(attrs={'title': 'major'}),
            'graduation_year': forms.DateInput(attrs={'title': 'Graduation Year'}),
            'institution ': forms.TextInput(attrs={'title': 'institution '})
        }


class WorkExperienceForm(forms.ModelForm):

    class Meta:
        model = WorkExperience
        fields = ('company_name', 'job_title', 'start_date', 'end_date', 'responsibilities')
        widgets = {

            'company_name': forms.TextInput(attrs={'title': 'Company Name'}),
            'job_title': forms.TextInput(attrs={'title': 'Job Title'}),
            'start_date': forms.DateInput(attrs={'title': 'Start Date'}),
            'end_date': forms.DateInput(attrs={'title': 'End Date'}),
            'responsibilities': forms.Textarea(attrs={'title': 'responsibilities'})
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('file',)
        labels = {
            'file': ' '
        }
        widgets = {
        'file': forms.FileInput(attrs={'title': 'resume',"class":"form-control"})
        }
        
