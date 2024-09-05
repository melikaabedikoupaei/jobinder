from django.contrib import admin
from .models import Candidate, ProfessionalSkills, WorkExperience, Degree, Language

class DegreeInline(admin.StackedInline):
    model = Degree
    extra = 0  # Number of extra Degree forms to display

class WorkExperienceInline(admin.StackedInline):
    model = WorkExperience
    extra = 0  # Number of extra Degree forms to display

class ProfessionalSkillsInline(admin.StackedInline):
    model = ProfessionalSkills
    extra = 0  # Number of extra Degree forms to display


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'candidate_family_name', 'birth_date', 'gender')
    list_filter = ('candidate_name', 'candidate_family_name', 'birth_date', 'gender')
    search_fields = ('candidate_name', 'candidate_family_name', 'birth_date', 'gender')
    inlines = [DegreeInline,WorkExperienceInline]  # Adding DegreeInline to CandidateAdmin

admin.site.register(ProfessionalSkills)
admin.site.register(Degree)
admin.site.register(WorkExperience)
admin.site.register(Language)
