from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    real_first_name = models.CharField(max_length=200, null=True)
    real_last_name = models.CharField(max_length=200, null=True)
    
    email = models.EmailField(unique=True, null=True)
    
    GENDER_CHOICES = (('M', 'Male'),
                      ('F', 'Female'),
                      ('T', 'Transgender'),
                      ('N', 'Prefer not to tell'),
                      )
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    
    bio = models.TextField(max_length=300, null=True)

    avatar = models.ImageField(null=True, blank=True, default="default-avatar.svg")

    # privacy = models.BooleanField(default=False)

    CL_SUBJECT = 0
    EL_SUBJECT = 1
    FR_SUBJECT = 2
    IPLA_SUBJECT = 3
    MA_SUBJECT = 4
    PH_SUBJECT = 5
    CM_SUBJECT = 6
    OS_SUBJECT = 7
    JS_SUBJECT = 8
    CI_SUBJECT = 9
    ME_SUBJECT = 10
    CH_SUBJECT = 11
    EI_SUBJECT = 12
    BA_SUBJECT = 13
    MIS_SUBJECT = 14
    FM_SUBJECT = 15
    EC_SUBJECT = 16
    EE_SUBJECT = 17
    CE_SUBJECT = 18
    CO_SUBJECT = 19
    IPEECS_SUBJECT = 20
    AP_SUBJECT = 21
    GP_SUBJECT = 22
    SS_SUBJECT = 23
    GA_SUBJECT = 24
    HK_SUBJECT = 25
    LS_SUBJECT = 26
    BM_SUBJECT = 27
    SUBJECT_CHOICES = [(CL_SUBJECT, '中國文學系'), (EL_SUBJECT, '英美語文學系'), 
                       (FR_SUBJECT, '法國語文學系'), (IPLA_SUBJECT, '文學院學士班'),
                       (CM_SUBJECT, '化學系'), (OS_SUBJECT, '光電科學與工程學系'),
                       (JS_SUBJECT, '理學院學士班'), (CI_SUBJECT, '土木工程學系'), 
                       (ME_SUBJECT, '機械工程學系'), (CH_SUBJECT, '化學工程與材料工程學系'), 
                       (EI_SUBJECT, '工學院學士班'), (BA_SUBJECT, '企業管理學系'), 
                       (MIS_SUBJECT, '資訊管理學系'), (FM_SUBJECT, '財務金融學系'),
                       (EC_SUBJECT, '經濟學系'), (EE_SUBJECT, '電機工程學系'),
                       (CE_SUBJECT, '資訊工程學系'), (CO_SUBJECT, '通訊工程學系'),
                       (IPEECS_SUBJECT, '資訊電機學院學士班'), (AP_SUBJECT, '大氣科學學系'),
                       (GP_SUBJECT, '地球科學學系'), (SS_SUBJECT, '太空工程與科學學系'),
                       (GA_SUBJECT, '地科院學士班'), (HK_SUBJECT, '客家語文暨社會科學學系'), 
                       (LS_SUBJECT, '生命科學系'), (BM_SUBJECT, '生醫工程與科學學系')]
    subject = models.IntegerField(choices=SUBJECT_CHOICES, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Topic(models.Model):
    name = models.CharField(max_length=200)
    post_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)
    
    message_count = models.IntegerField(default=0, null=True, blank=True)
    like_count = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        pass
        # ordering = ['-updated', '-created', 'like_count', 'message_count']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Report(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    choices = (
        ('Spam', 'Spam'),
        ('Terrorism', 'Terrorism'),
        ('Discrimination', 'Discrimination'),
        ('Misinformation', 'Misinformation'),
        ('Public Shaming', 'Public Shaming'),
        ('Illegal or Dangerous', 'Illegial or Dangerous'),
        ('Sexual Harrassment', 'Sexual Harassment'),
        ('Else', 'Else'),
    )
    
    reason = models.CharField(max_length=50, choices=choices, default='Spam')

    def __str__(self):
        return self.name
        
class Image(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    