
from django.db import models
from jobs.models import Job
from users.models import User
from jobseekers.models import JobSeekerProfile

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn')
    ]
    

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='applications', null=True)  # Changed to JobSeekerProfile
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_seeker} applied for {self.job.title}"

    class Meta:
        unique_together = ('job', 'job_seeker')
