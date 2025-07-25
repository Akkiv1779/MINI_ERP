from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def assign_group(instance, created):
    if created:
        Group.objects.get_or_create(name=instance.role)
        instance.groups.add(Group.objects.get(name=instance.role))
