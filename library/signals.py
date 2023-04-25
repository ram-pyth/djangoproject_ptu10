from django.contrib.auth.models import User  # siuntėjas
from django.db.models.signals import post_save  # signalas
from django.dispatch import receiver  # gavėjo dekoratorius

from .models import Profilis


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profilis.objects.create(user=instance)
    else:
        instance.profilis.save()

    print('printas iš signals, gavėjo, kwargs', kwargs)
    print(instance, created)
