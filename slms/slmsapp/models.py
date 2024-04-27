from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

class CustomUser(AbstractUser):
    USER ={
        (1,'admin'),
        (2,'staff')
    }
    user_type = models.CharField(choices=USER,max_length=50,default=1)

    profile_pic = models.ImageField(upload_to='media/profile_pic')


class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.admin.username


class Staff_Leave(models.Model):

    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=100)
    from_date = models.CharField(max_length=100)
    to_date = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.staff_id.admin.first_name + self.staff_id.admin.last_name


class UserFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.user} - {self.created_at}'

class AdminFeedback(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_feedbacks')
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    feedback = models.TextField()

    def str(self):
        return f"Feedback for {self.employee.username} by {self.admin.username}"


from django.db import models
from django.conf import settings
from slmsapp.models import Staff

class LeaveRequest(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Leave Request for {self.staff.admin.username}"