# employers/forms.py
from django import forms
from jobs.models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description','requirements', 'salary', 'location','category', 'job_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description', 'rows': 4}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Requirements', 'rows': 3}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location', 'id': 'id_location', 'readonly': 'readonly'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., IT, Marketing, Sales'}),
            'job_type': forms.Select(attrs={'class': 'form-select'})  # Add the widget for job_type field

        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category or len(category.strip()) < 3:
            raise forms.ValidationError("Category must be at least 3 characters long.")
        return category.strip()    
