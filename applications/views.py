from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import JobApplication
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from jobs.models import Job

@login_required
def job_applications(request):
    # Fetching the applications for the logged-in jobseeker
    job_seeker = request.user.jobseekerprofile  # Assuming the User model has a JobSeekerProfile

    # Get the job applications for the current user
    applications = JobApplication.objects.filter(job_seeker=job_seeker).order_by('-applied_at')

    # Implementing pagination
    paginator = Paginator(applications, 5)  # Show 5 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Rendering the template with the applications and pagination context
    return render(request, 'applications/applications.html', {
        'applications': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })


@csrf_exempt
def withdraw_application(request):
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        status = request.POST.get('status')
        
        # Get the application and update the status
        try:
            application = JobApplication.objects.get(id=application_id, job_seeker=request.user.jobseekerprofile)
            application.status = status
            application.save()
            return JsonResponse({'success': True})
        except JobApplication.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Application not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Get all applicants for the job and prefetch related fields for performance
    applications = JobApplication.objects.filter(job=job).select_related('job_seeker__user')

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')

        application = get_object_or_404(JobApplication, id=application_id, job=job)

        # Prevent update if the status is withdrawn
        if application.status == 'withdrawn':
            # You can use messages framework if you want to notify the user
            from django.contrib import messages
            messages.warning(request, "Cannot update status. This application has been withdrawn.")
        else:
            # Update status based on action
            if action == 'shortlist':
                application.status = 'shortlisted'
                application.save()
                from django.contrib import messages
                messages.success(request, f"{application.job_seeker.name} has been shortlisted.")
            elif action == 'reject':
                application.status = 'rejected'
                application.save()
                from django.contrib import messages
                messages.success(request, f"{application.job_seeker.name} has been rejected.")

        # Always redirect to clear POST data and avoid duplicate submissions
        return redirect('view_applicants', job_id=job.id)

    return render(request, 'applications/view_applicants.html', {'job': job, 'applications': applications})
