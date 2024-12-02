from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rating, GlobalRating

@receiver(post_save, sender=Rating)
def update_global_rating_on_save(sender, instance, created, **kwargs):
    user = instance.user
    global_rating, created = GlobalRating.objects.get_or_create(user=user)
    
    if created:
        global_rating.rating = instance.score
    else:
        global_rating.rating += instance.score
    
    global_rating.save()

@receiver(post_delete, sender=Rating)
def update_global_rating_on_delete(sender, instance, **kwargs):
    user = instance.user
    global_rating = GlobalRating.objects.get(user=user)
    
    global_rating.rating -= instance.score
    global_rating.save()
