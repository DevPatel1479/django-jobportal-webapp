from django import forms
from jobseekers.models import JobSeekerProfile


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('resume',)