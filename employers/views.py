from django.shortcuts import render, redirect
from .models import EmployerProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employers.forms import JobForm
from jobs.models import Job
from applications.models import JobApplication

# Create your views here.


@login_required
def employer_dashboard(request):
    profile = EmployerProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(employer=profile).order_by('-created_at')
    applications = JobApplication.objects.filter(job__in=jobs)
    show_post_modal = False
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = profile
            job.save()
            messages.success(request, "Job posted!")

            return redirect('employer_dashboard')  # Replace with your URL name
        else:
            show_post_modal = True
    else:
        form = JobForm()
    # print(f"jobs : {jobs.last().id}")
    context = {
        'form': form,
        'jobs': jobs,
        'jobs_posted_count': jobs.count(),
        'applications_count': applications.count(),  # Placeholder
        'shortlisted_count': applications.filter(status='shortlisted').count(),   # Placeholder
        'rejected_count': applications.filter(status='rejected').count(),      # Placeholder
        'show_post_modal':    show_post_modal,
    }
    return render(request, 'employers/employer_dashboard.html', context)

@login_required
def employer_profile_view(request):
    try:
        profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        profile = None

    return render(request, 'employers/employer_profile.html', {
        'user': request.user,
        'profile': profile,
    })


@login_required
def edit_employer_profile(request):
    try:
        profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        profile = EmployerProfile(user=request.user)

    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        website = request.POST.get('website')

        profile.company_name = company_name
        profile.website = website

        if 'company_proof' in request.FILES:
            profile.company_proof = request.FILES['company_proof']

        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('employer_profile')

    return redirect('employer_profile')
