from django.shortcuts import render, redirect, get_object_or_404
from .models import JobSeekerProfile, Skill
from django.contrib.auth.decorators import login_required
from core.forms import JobSeekerProfileForm
from django.core.files.storage import default_storage
from django.contrib import messages
from django.http import JsonResponse
from jobs.models import Job
from users.models import User
from applications.models import JobApplication
from employers.models import EmployerProfile

# Create your views here.


def dashboard(request):
    user = request.user
    job_seeker_profile = JobSeekerProfile.objects.get(user=user)
    jobs = Job.objects.select_related('employer').order_by('-created_at')
    applied_job_ids = JobApplication.objects.filter(job_seeker=job_seeker_profile).values_list('job_id', flat=True)
    all_jobs =  Job.objects.all()
    titles = Job.objects.values_list('title', flat=True).distinct()
    locations = Job.objects.values_list('location', flat=True).distinct()
    categories = Job.objects.values_list('category', flat=True).distinct()
    companies = EmployerProfile.objects.values_list('company_name', flat=True).distinct()
    context = {
        'user' : user,
        'jobs' : jobs,
        'titles': titles,
        'locations': locations,
        'categories': categories,
        'companies': companies,
        "applied_job_ids": set(applied_job_ids), 
    }
    
    return render(request, 'jobseekers/dashboard.html', context)

# @login_required
# def profile(request):

#     jobseeker_profile = JobSeekerProfile.objects.get(user = request.user)
#     context = {
#         'user': request.user,
#         'jobseeker_profile': jobseeker_profile,
#     }
    

#     return render(request, 'core/profile.html', context)




@login_required
def profile(request):
    profile = JobSeekerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        skill_name = request.POST.get("skill_name")
        if skill_name:  # This check is crucial
            skill_name = skill_name.strip()
            if skill_name:
                skill, created = Skill.objects.get_or_create(name=skill_name)
                profile.skills.add(skill)
                messages.success(request, "Skill added successfully")
            return redirect('profile')
        if 'profile_photo' in request.FILES:
            if profile.profile_photo:
                profile.profile_photo.delete()  # Delete old photo
            profile.profile_photo = request.FILES['profile_photo']
            profile.save()
            messages.success(request, "Profile photo updated successfully")
            return redirect('profile')
        if 'about_me' in request.POST:
            profile.about_me = request.POST.get('about_me', '')
            profile.save()
            messages.success(request, "About Me updated successfully")
            return redirect('profile')
        # Upload resume
        if 'resume' in request.FILES:
            # Delete old resume if exists
            if profile.resume:
                profile.resume.delete()
            profile.resume = request.FILES['resume']
            profile.save()

        # Remove resume
        elif request.POST.get('remove_resume'):
            if profile.resume:
                profile.resume.delete()
                profile.resume = None
                profile.save()
        return redirect('profile')

    context = {
        'user': request.user,
        'jobseeker_profile': profile,
        "skills": profile.skills.all()
    }
    return render(request, 'core/profile.html', context)


@login_required
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        jobseeker_profile, _ = JobSeekerProfile.objects.get_or_create(user=request.user)
        jobseeker_profile.resume = request.FILES['resume']
        jobseeker_profile.save()
        messages.success(request, "Resume uploaded successfully.")
    return redirect('profile')

@login_required
def delete_resume(request):
    if request.method == 'POST':
        jobseeker_profile = JobSeekerProfile.objects.get(user=request.user)
        if jobseeker_profile.resume:
            jobseeker_profile.resume.delete(save=False)  # Deletes file from storage
            jobseeker_profile.resume = None
            jobseeker_profile.save()
            messages.success(request, "Resume deleted successfully.")
    return redirect('profile')


@login_required
def add_skill(request):
    if request.method == 'POST':
        name = request.POST.get('skill_name', '').strip()
        if name:
            skill_obj, _ = Skill.objects.get_or_create(name=name)
            profile = JobSeekerProfile.objects.get(user=request.user)
            profile.skills.add(skill_obj)
            return redirect('profile')
            # return JsonResponse({'status': 'success', 'skill': skill_obj.name})
    return JsonResponse({'status': 'error'}, status=400)

@login_required

def remove_skill(request):
    if request.method == 'POST':
        name = request.POST.get('skill_name', '').strip()
        try:
            skill_obj = Skill.objects.get(name=name)
            profile = JobSeekerProfile.objects.get(user=request.user)
            profile.skills.remove(skill_obj)
            # return redirect("profile")
            return JsonResponse({'status': 'success'})
        except Skill.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Skill not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)


def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Get the jobseeker profile associated with the logged-in user
    try:
        job_seeker_profile = JobSeekerProfile.objects.get(user=request.user)
    except JobSeekerProfile.DoesNotExist:
        messages.error(request, "You need to complete your profile before applying.")
        return redirect('profile')  # Replace with your actual profile edit URL name
    
    # Check for missing resume or skills
    if not job_seeker_profile.resume or job_seeker_profile.skills.count() == 0:
        if not job_seeker_profile.resume:
            messages.error(request, "Please upload your resume before applying for jobs.")
        if job_seeker_profile.skills.count() == 0:
            messages.error(request, "Please add at least one skill to your profile.")
        return redirect('profile')  # Replace with your profile edit view URL name
    
    # Check if the user has already applied for the job
    if JobApplication.objects.filter(job=job, job_seeker=job_seeker_profile).exists():
        messages.info(request, "You’ve already applied to this job.")
        return redirect('dashboard')  # Redirect to the dashboard if already applied
    
    # If not already applied, create a new job application
    job_application = JobApplication.objects.create(
        job=job,
        job_seeker=job_seeker_profile,
        status='applied'
    )
    
    messages.success(request, f"You’ve applied for “{job.title}”.")
    return redirect('dashboard')  # Redirect to the dashboard after successful application




def job_search(request):
    # Get GET parameters from the search form
    title = request.GET.get('keywords', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    company = request.GET.get('company', '')
    is_search = bool(request.GET)
    no_filters = is_search and not any([title, location, category, company])
    if no_filters:
        messages.info(request, "All jobs are available.")
    # Initialize the base queryset
    jobs = Job.objects.select_related('employer').order_by('-created_at')
    company_no_jobs_found = False
    # Filter jobs based on the selected criteria
    if title:
        jobs = jobs.filter(title__icontains=title)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if category:
        jobs = jobs.filter(category__icontains=category)
    if company:
        jobs = jobs.filter(employer__company_name__icontains=company)
        if not jobs.exists():
            company_no_jobs_found = True
    titles     = Job.objects.values_list('title', flat=True).distinct()
    locations  = Job.objects.values_list('location', flat=True).distinct()
    categories = Job.objects.values_list('category', flat=True).distinct()
    companies  = EmployerProfile.objects.values_list('company_name', flat=True).distinct()


    applied_job_ids = JobApplication.objects.filter(
        job_seeker__user=request.user
    ).values_list('job_id', flat=True)

    # Pass the filtered jobs and other data to the template
    return render(request, 'jobseekers/dashboard.html', {
        'jobs': jobs,
        
        'titles': titles,
        'locations': locations,
        'categories': categories,
        'companies': companies,
        'filter_keywords': title,
        'filter_location': location,
        'filter_category': category,
        'filter_company' : company,
        'applied_job_ids' : set(applied_job_ids),
        'company_no_jobs': company_no_jobs_found
    })