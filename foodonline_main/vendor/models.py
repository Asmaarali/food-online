from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification_email
from datetime import time , date , datetime


# Create your models here.
class Vendor(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name='user_profile',on_delete=models.CASCADE)
    vendor_name=models.CharField(max_length=50)
    vendor_slug=models.SlugField(max_length=50 , unique=True)
    vendor_license=models.ImageField(upload_to='vendor/license')
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    #is open badge
    def is_open(self):
        # check current opening hours
        c_today = date.today()
        today = c_today.isoweekday()
        # print(c_today)
        current_opening_hours = OpeningHour.objects.filter(vendor=self , day = today)
        # print(opening_hours)
        # check is open or not in giving time slot
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        is_open = None
        for i in current_opening_hours:
            try:
                start=str(datetime.strptime(i.from_hour , "%I:%M %p").time())
                end=str(datetime.strptime(i.to_hour , "%I:%M %p").time())
                # print(start)
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
            except:
                is_open = False
        return is_open
    
    # triger the save function from admin
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            orig = Vendor.objects.get(pk = self.pk)
            if orig.is_approved != self.is_approved:  # self
                # mail_template and context are duplicating in if else block so we put here
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                
                if self.is_approved == True:
                    # send notification email
                    mail_subject = 'Congratulations! Your restaurant has been approved.'
                    send_notification_email(mail_subject, mail_template, context)
                else:
                    # send notification email
                    mail_subject = 'We are sorry! You are not eligible for publishing your food menu on our Marketplace.'
                    send_notification_email(mail_subject, mail_template, context)
        return super(Vendor , self).save(*args, **kwargs)
    

class OpeningHour(models.Model):

    DAYS = [
        (1,("Monday")),
        (2,("Tuesday")),
        (3,("Wednesday")),
        (4,("Thursday")),
        (5,("Friday")),
        (6,("Saturday")),
        (7,("Sunday")),
    ]
    
    # for h in range(0,24):
    #     for m in (0,30):
    #         print(time(h,m).strftime('%I:%M %p'))

    HOUR_OF_DAY = [(time(h,m).strftime('%I:%M %p'),time(h,m).strftime('%I:%M %p')) for h in range(0,24) for m in (0,30)]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY, max_length=10 , blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY, max_length=10 , blank=True)
    is_closed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('day' , '-from_hour')
        unique_together = ('vendor','day' , 'from_hour' , 'to_hour')
    
    
    def __str__(self):
        return self.get_day_display()
        
        # day_dict = dict(self.DAYS)
        # return day_dict.get(self.day, "Unknown")
    