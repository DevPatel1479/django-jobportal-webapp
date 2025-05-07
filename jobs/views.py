from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from .models import Job
from employers.models import EmployerProfile
from employers.forms import JobForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



@csrf_exempt
def bulk_delete_jobs(request):
    if request.method == "POST":
        data = json.loads(request.body)
        job_ids = data.get('job_ids', [])
        print("Received job IDs:", job_ids)

        try:
            employer = EmployerProfile.objects.get(user=request.user)
            jobs_to_delete = Job.objects.filter(id__in=job_ids, employer=employer)
            print("Jobs found for deletion:", jobs_to_delete)

            count, _ = jobs_to_delete.delete()
            print("Jobs deleted:", count)

            return JsonResponse({'status': 'success', 'deleted': count})
        except EmployerProfile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Employer not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'jobs/job_detail_partial.html', {'job': job})
    # fallback:
    return render(request, 'jobs/job_detail_partial.html', {'job': job})

def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    print(f"in edit {job}")
    form = JobForm(request.POST or None, instance=job)
    if request.method == 'POST':
        if form.is_valid():

            form.save()
            return JsonResponse({'success': True})
        html = render_to_string(
            'jobs/job_edit_partial.html',
            {'form': form, 'job': job},
            request=request
        )
        return JsonResponse({'success': False, 'html': html})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'jobs/job_edit_partial.html', {'form': form, 'job':  job,})
    return render(request, 'employers/employer_dashboard.html', {'form': form})
    

def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    job.delete()
    return redirect('employer_dashboard')  # adjust if needed