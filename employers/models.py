from django.db import models
from users.models import User

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    company_proof = models.FileField(
        upload_to='company_proofs/',
        blank=True,
        null=True,
        help_text="Upload a PDF/PNG/JPG of your company proof."
    )

    def __str__(self):
        return self.user.name
    
