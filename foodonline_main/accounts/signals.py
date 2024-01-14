# dont forget to import this file in apps.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User , UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    # print(created)
    if created:
        # print(created)
        UserProfile.objects.create(user=instance) #user is nothing 
    else:
        try:
            # print(instance.username)
            profile=UserProfile.objects.get(user=instance)  #if we dont put these 2 line in try catch and already created profile was deleted then you update the user it will give error mathcing query doesnot exist so in except we will create again profile of that user
            profile.save()
        except:
            #create userprofile if not exists:
            UserProfile.objects.create(user=instance)
        #     print("profile created becaust it is not created")
        # print('user updated')


    # post_save.connect(post_save_create_profile_receiver,sender=User) ALSO do without reciever