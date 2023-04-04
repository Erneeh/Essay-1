from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from datetime import timedelta
from datetime import datetime as dt


class PayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    payment_for = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


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
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
    duration = models.PositiveIntegerField(default=7)
    duration_period = models.CharField(max_length=100, default='Day', choices=PERIOD_DURATION)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(User, related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)

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
