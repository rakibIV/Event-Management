from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from event.models import Event
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        print("Sending activation mail to user")
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"
        
        subject = "Activate your email"
        message = f"Hi {instance.username},\n\nPlease click on the link below to activate your account:\nActivation link: {activation_url}\n\nThankyou!"
        reciepient = [instance.email]
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, reciepient)
        except Exception as e:
            print(f"Failed to send email to {instance.email} : {str(e)}")
            
            
@receiver(post_save, sender=User)
def assign_role(sender, instance, created,**kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='User')
        instance.groups.clear()
        instance.groups.add(user_group)
        instance.is_staff = True
        instance.save()
        
@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_confirmation(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = instance.participants.get(id=user_id)
            print(user)
            print(user.email)
            subject = "RSVP Confirmation for Your Event"
            message = f"Hello {user.username},\n\nYou have successfully RSVP'd for '{instance.name}'.\nDate: {instance.date} | Time: {instance.time} | Location: {instance.location}\n\nThank you for joining us!"
            recipient = [user.email]
            
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient,
            )

            if instance.image:
                email.attach_file(instance.image.path)

            try:
                email.send()
            except Exception as e:
                print(f"Failed to send email to {recipient} : {str(e)}")
