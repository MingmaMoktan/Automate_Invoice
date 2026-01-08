from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('advanced', 'Advanced'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

# --- SIGNALS: Auto-create profile when a User is created ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()