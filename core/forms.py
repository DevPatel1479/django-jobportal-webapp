
from django import forms
from django.core.exceptions import ValidationError
from users.models import User
from employers.models import EmployerProfile
from jobseekers.models import JobSeekerProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.CharField(widget=forms.HiddenInput())  # Add the role field here
    document = forms.FileField(
        required=False,
        label="Company proof (PDF, PNG, JPG)",
        help_text="Required if you select Job Provider"
    )
    company_name = forms.CharField(
        required=False,  # Validation happens in `clean()` based on role
        label="Company Name",
        max_length=255
    )

    class Meta:
        model = User
        # fields = ['username', 'email', 'password', 'confirm_password', 'is_employer', 'is_jobseeker']
        fields = ['name', 'email', 'is_employer', 'is_jobseeker']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Check if the email exists
            raise ValidationError("This email address is already in use. Please choose another one.")
        return email
    # def clean_password(self):
    #     password = self.cleaned_data.get('password')

    #     # Ensure that the password is at least 8 characters long
    #     if len(password) < 8:
    #         raise ValidationError("Password must be at least 8 characters long.")

    #     return password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if not password:
            raise ValidationError("Password must be at least 8 characters long.")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        # Ensure that the password and confirm password match
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        # Here, we're using the role value passed from the hidden field in the form
        user_role = cleaned_data.get("role")  # Hidden field 'role'

        # Check that the role is either 'jobseeker' or 'employer'
        if user_role == 'jobprovider':
            cleaned_data['is_employer'] = True
            cleaned_data['is_jobseeker'] = False
            if not self.cleaned_data.get('document'):
                raise forms.ValidationError("Company proof is required for Job Providers.")
            if not self.cleaned_data.get('company_name'):
                raise forms.ValidationError("Company name is required for Job Providers.")
        elif user_role == 'jobseeker':
            cleaned_data['is_jobseeker'] = True
            cleaned_data['is_employer'] = False
        else:
            raise forms.ValidationError("Invalid role selected.")

        return cleaned_data

    def save(self, commit=True):
        # Create the user object
        user = super().save(commit=False)
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
            print(f"user saved: {user}")

            # Create the appropriate profile based on the user's role
            if user.is_employer:
                profile, _ = EmployerProfile.objects.get_or_create(user=user)
                # If a new file was uploaded, delete the old one first
                new_file = self.cleaned_data.get('document')
                if new_file:
                    if profile.company_proof:
                        profile.company_proof.delete(save=False)
                    profile.company_proof = new_file
                profile.company_name = self.cleaned_data.get('company_name')
                print("company name")
                print(profile.company_name)
                profile.save()
                # employer_profile = EmployerProfile.objects.create(user=user, company_name="")
                # print(f"Employer Profile created: {employer_profile}")  # Debug log for employer profile creation
            elif user.is_jobseeker:
                
                jobseeker_profile = JobSeekerProfile.objects.create(user=user, name = user.name)
                print(f"Job Seeker Profile created: {jobseeker_profile}")  # Debug log for jobseeker profile creation

        return user

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={
                'id': 'resumeInput',
                'accept': '.pdf,.doc,.docx',
                'style': 'display:none;',
            }),
        }