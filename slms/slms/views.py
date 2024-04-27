from django.shortcuts import render, redirect, HttpResponse
from slmsapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from slmsapp.models import CustomUser
from slmsapp.forms import UserFeedbackForm, AdminFeedbackForm
from django.db.models import Q

from django.contrib.auth import get_user_model
from slmsapp.models import AdminFeedback

import slmsapp

User = get_user_model()


def BASE(request):
    return render(request, 'base.html')


def FIRSTPAGE(request):
    return render(request, 'firstpage.html')


def LOGIN(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password')
                                         )
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')
            elif user_type == '2':
                return redirect('staff_home')
            return redirect('index')

        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')
    else:
        messages.error(request, 'Email or Password is not valid')
        return redirect('login')


def doLogout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
def INDEX(request):
    return render(request, 'index.html')


login_required(login_url='/')


def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print(profile_pic)

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect('profile')

        except:
            messages.error(request, "Your profile updation has been failed")
    return render(request, 'profile.html')


def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)

    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"]: data
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            messages.success(request, 'Password Change  Succeesfully!!!')
            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.success(request, 'Current Password wrong!!!')
            return redirect("change_password")
    return render(request, 'change-password.html')


def submit_user_feedback(request):
    if request.method == 'POST':
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Assign the logged-in user to the feedback instance
            feedback.save()
            return redirect('staff_home')  # Redirect to a success page
    else:
        form = UserFeedbackForm()
    return render(request, 'slmsapp/user_feedback_form.html', {'form': form})


def submit_admin_feedback(request):
    # Fetch staff members from the database
    staff = CustomUser.objects.filter(user_type='2')  # Assuming '2' represents staff users

    if request.method == 'POST':
        form = AdminFeedbackForm(request.POST)
        if form.is_valid():
            employee_id = request.POST.get('staff')
            feedback_text = request.POST.get('feedback')

            feedback = AdminFeedback(
                admin=request.user,
                employee_id=employee_id,
                feedback=feedback_text
            )
            feedback.save()
            return redirect('admin_home')
    else:
        # If the request method is GET, initialize an empty form
        form = AdminFeedbackForm()

    # Render the template with the form and the staff members
    return render(request, 'slmsapp/admin_feedback_form.html', {'form': form, 'staff': staff})


'''
def submit_admin_feedback(request):
    if request.method == 'POST':
        form = AdminFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.admin = request.user
            feedback.save()
            return redirect('admin_home')
    else:
        form = AdminFeedbackForm()
    return render(request, 'slmsapp/admin_feedback_form.html', {'form': form})
'''

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.mail import send_mail
# from slmsapp.models import LeaveRequest
#
# def approve_leave(request, leave_id):
#     leave = LeaveRequest.objects.get(pk=leave_id)
#     leave.status = 1  # Update status to approved
#     leave.save()
#
#     # Send email notification
#     send_mail(
#         'Leave Request Approved',
#         f'Your leave request from {leave.from_date} to {leave.to_date} has been approved.',
#         'your_email@example.com',
#         [leave.staff_id.admin.email],
#         fail_silently=False,
#     )
#
#     messages.success(request, 'Leave request has been approved.')
#     return redirect('view_staff_leave')
#
# def disapprove_leave(request, leave_id):
#     leave = LeaveRequest.objects.get(pk=leave_id)
#     leave.status = 2  # Update status to disapproved
#     leave.save()
#
#     # Send email notification
#     send_mail(
#         'Leave Request Disapproved',
#         f'Your leave request from {leave.from_date} to {leave.to_date} has been disapproved.',
#         'your_email@example.com',
#         [leave.staff_id.admin.email],
#         fail_silently=False,
#     )
#
#     messages.success(request, 'Leave request has been disapproved.')
#     return redirect('view_staff_leave')

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect

def approve_or_disapprove_leave(request, leave_id):
    # Assuming you have a model named Leave and it has a status field
    leave = (slmsapp.objects.get(id=leave_id))
    if request.method == 'POST':
        # Assuming 'approve' and 'disapprove' are the POST parameters
        if 'approve' in request.POST:
            leave.status = 1 # Assuming 1 means approved
            leave.save()
            send_email(leave)
            messages.success(request, 'Leave has been approved and email sent to the user.')
        elif 'disapprove' in request.POST:
            leave.status = 2 # Assuming 2 means disapproved
            leave.save()
            send_email(leave)
            messages.success(request, 'Leave has been disapproved and email sent to the user.')
        return redirect('view_staff_leave') # Redirect to the page where you view staff leaves
    else:
        # Handle GET request or show a form to approve/disapprove
        pass

def send_email(leave):
    # Configure your email settings in settings.py
    from_email = 'your_email@example.com'
    to_email = leave.staff_id.admin.email # Assuming the user's email is stored in the admin model
    subject = 'Leave Status Update'
    message = f"Dear {leave.staff_id.admin.first_name}, your leave request has been { 'approved' if leave.status == 1 else 'disapproved' }."
    send_mail(subject, message, from_email, [to_email])
