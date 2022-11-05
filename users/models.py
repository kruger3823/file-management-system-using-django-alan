from django.db import models
from django.contrib.auth.models import User
from PIL import Image


DEPARTMENT_CHOICES =(
    ("mca", "MCA"),
    ("eee", "EEE"),
    ("cse", "CSE"),
    ("ncc", "NCC"),
)
  
class Department(models.Model):
    dep_name = models.CharField(max_length=200,choices=DEPARTMENT_CHOICES)
    def __str__(self):
        return self.dep_name 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

