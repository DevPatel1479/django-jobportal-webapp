from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import LogoutView
from .forms import RegisterForm
from employers.models import EmployerProfile
from django.contrib.auth import logout
from jobs.models import Job
from applications.models import JobApplication
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import random


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        if request.user.is_jobseeker:

            return redirect('dashboard')
        elif EmployerProfile.objects.filter(user=request.user).exists():
            return redirect('employer_dashboard')
        else:
            # Employer is authenticated but no profile: log them out
            logout(request)
            
            return redirect('login')
        # return redirect('home')
        # else:
            # return redirect('home')
    else:
        jobs = (
        Job.objects
           .select_related('employer')
           .order_by('-created_at')[:12]
    )
        
        return render(request, 'core/home/index.html', {
        'jobs': jobs,
    })

def about_us(request):
    return render(request,'core/about_us.html')

def job_list(request):
    # get all jobs, newest first
    jobs = Job.objects.select_related('employer').order_by('-created_at')

    # if logged in, figure out which jobs they've applied to
    applied_job_ids = set()
    if request.user.is_authenticated:
        applied_job_ids = set(
            JobApplication.objects
                .filter(job_seeker__user=request.user)
                .values_list('job_id', flat=True)
        )

    return render(request, 'core/job_list.html', {
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,
    })

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        print(form)

        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            print(f"user {auth_login(request, user)}")
            # messages.success(request, "Registration successful!")
            if user.is_jobseeker:

                return redirect('dashboard')
            else:
                return redirect('employer_dashboard')
        else:
            print(form.non_field_errors())
            # Send exact form errors to template
            for error in form.non_field_errors():
                messages.error(request, error)
            role = request.POST.get('role', 'jobseeker')
            print(f"role : {role}")
            return render(request, 'core/authentication/register.html', {'form': form, 'role' : role})
    else:
        form = RegisterForm()
    return render(request, 'core/authentication/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # If user exists, log them in
            
            auth_login(request, user)
            print(user)
            
            if user.is_jobseeker:

                return redirect('dashboard')  # or any page you want to redirect to
            else:
                return redirect('employer_dashboard')
        else:
            # If user does not exist, show an error message
            messages.error(request, "Invalid email or password.")
            return render(request, 'core/authentication/login.html')

    return render(request, 'core/authentication/login.html')


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Clear any lingering messages before logging out
        messages.success(request,None)
        return super().dispatch(request, *args, **kwargs)
    

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'status': 'error', 'message': 'Email is required'})

            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['otp_email'] = email

            send_mail(
                subject='Your OTP Code',
                message=f'Your OTP is: {otp}',
                from_email='your_email@gmail.com',  # same as EMAIL_HOST_USER
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({'status': 'sent'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            input_otp = data.get('otp')
            email = data.get('email')

            saved_otp = request.session.get('otp')
            saved_email = request.session.get('otp_email')

            if saved_otp and saved_email and input_otp == saved_otp and email == saved_email:
                return JsonResponse({'status': 'verified'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
