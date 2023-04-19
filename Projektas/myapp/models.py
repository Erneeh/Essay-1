from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from datetime import timedelta
from datetime import datetime as dt


class Membership(models.Model):
    MEMBERSHIP_CHOICES = (
        ('Ultra', 'Ultra'),
        ('Premium', 'Premium'),
        ('Basic', 'Basic'),
        ('Free', 'Free')
    )
    PERIOD_DURATION = (
        ('Days', 'Days'),
        ('Week', 'Week'),
        ('Months', 'Months'),
    )
    slug = models.SlugField(default=None)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
    duration = models.PositiveIntegerField(default=7)
    duration_period = models.CharField(max_length=100, default='Day', choices=PERIOD_DURATION)
    stripe_product_id = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.membership_type


class Price(models.Model):
    product = models.ForeignKey(Membership, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

    def __str__(self):
        return self.product.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(User, related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
    stripe_sub_id = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=UserMembership)
def create_subscription(sender, instance, *args, **kwargs):
    if instance:
        Subscription.objects.create(user_membership=instance,
                                    expires_in=dt.now().date() + timedelta(days=instance.membership.duration))


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username


@receiver(post_save, sender=Subscription)
def update_active(sender, instance, *args, **kwargs):
    if instance.expires_in < dt.today().date():
        subscription = Subscription.objects.get(id=instance.id)
        subscription.delete()


class Kontaktai(models.Model):
    user = models.TextField(max_length=20)
    elpastas = models.EmailField(max_length=30)
    komentaras = models.TextField(max_length=400)

    def __str__(self):
        return self.elpastas
