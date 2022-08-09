from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class CustomUserManager(models.Manager):
    def create_user(self, userid,email,  userType, name, password=None):
        user=self.model(
            email=email,
            name=name,
            userid=userid,
            userType=userType
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, userid, email, userType, name, password):
        user=self.create_user(
            email=email,
            name=name,
            userid=userid,
            userType=userType,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user
    def get_by_natural_key(self, userid):
        return self.get(userid=userid)

class UserInfo(AbstractBaseUser):
    userid = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    
    name= models.CharField(max_length=100)
    USER_CHOICES = [
        ('Student', 'Student'),
        ('Instructor', 'Instructor'),
        ('Admin', 'Admin'),
    ]
    userType = models.CharField(max_length=10, choices=USER_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    REQUIRED_FIELDS = ('email', 'name', 'userType')
    USERNAME_FIELD = 'userid'
    objects = CustomUserManager()
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def natural_key(self):
        return [self.email]
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    def has_module_perms(self, app_label):
        return True
    

class Course(models.Model):
    code = models.CharField(max_length=10)
    desc= models.CharField(max_length=100)
    profs =models.ManyToManyField(UserInfo, related_name='course_profs')
    course_credits = models.FloatField()
    DEPARTMENT_CHOICES = [
        ('AM', 'Engineering and Computational Mechanics'),
        ('BB', 'Biochemical Engineering and Biotechnology'),
        ('CH', 'Chemical Engineering'),
        ('CS', 'Computer Science and Engineering'),
        ('CE', 'Civil Engineering'),
        ('EE', 'Electrical Engineering'),
        ('ES', 'Energy Science and Engineering'),
        ('MS', 'Materials Science and Engineering'),
        ('MT', 'Mathematics'),
        ('ME', 'Mechanical Engineering'),
        ('PH', 'Physics'),
        ('TT', 'Textile and Fibre Engineering')
    ]
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    students = models.ManyToManyField(UserInfo, related_name='course_students')
    course_intro = models.FileField(upload_to='course_intro')
    publish_grades = models.BooleanField(default=False)

    def __str__(self):
        return self.code

