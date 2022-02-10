from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(default='default-avatar.png', upload_to='users/', null=True, blank=True)
    
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Company(models.Model):
    user_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=400)
    country = models.CharField(max_length=400)
    headquarters = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'


class Contact(models.Model):
    user_id = models.CharField(max_length=100, null=True)
    contact_name = models.CharField(max_length=400)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')
    contact_number = models.IntegerField()

    class Meta:
        db_table = 'contact'