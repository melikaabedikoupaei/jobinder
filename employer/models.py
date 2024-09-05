from django.db import models

class Position(models.Model):
    JobID = models.IntegerField(primary_key=True)
    WindowID = models.IntegerField(null=True)
    Title = models.CharField(max_length=255, null=True)
    Description = models.TextField(null=True)
    Requirements = models.TextField(null=True)
    City = models.CharField(max_length=100, null=True)
    State = models.CharField(max_length=100, null=True)
    Country = models.CharField(max_length=100, null=True)
    Zip5 = models.FloatField(null=True)
    StartDate = models.CharField(max_length=100, null=True)
    EndDate = models.CharField(max_length=100, null=True)
    job = models.CharField(max_length=100, null=True)
    Combined = models.TextField(null=True)
    def __str__(self):
        return self.Title if self.Title else str(self.JobID)