from django.db import models
from employers.models import EmployerProfile




class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('remote', 'Remote'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(default="Not specified")
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100, help_text="Enter job category (e.g., IT, Marketing, Sales)", default='IT/CS')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
