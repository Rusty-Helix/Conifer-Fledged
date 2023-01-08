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
    gender = models.CharField(choices=GENDER_CHOICES, null=True, max_length=2)
    
    bio = models.TextField(max_length=300, null=True)

    avatar = models.ImageField(null=True, blank=True, default="default-avatar.svg")

    # privacy = models.BooleanField(default=False)

    CL_DEPARTMENT = 0
    EL_DEPARTMENT = 1
    FR_DEPARTMENT = 2
    IPLA_DEPARTMENT = 3
    MA_DEPARTMENT = 4
    PH_DEPARTMENT = 5
    CM_DEPARTMENT = 6
    OS_DEPARTMENT = 7
    JS_DEPARTMENT = 8
    CI_DEPARTMENT = 9
    ME_DEPARTMENT = 10
    CH_DEPARTMENT = 11
    EI_DEPARTMENT = 12
    BA_DEPARTMENT = 13
    MIS_DEPARTMENT = 14
    FM_DEPARTMENT = 15
    EC_DEPARTMENT = 16
    EE_DEPARTMENT = 17
    CE_DEPARTMENT = 18
    CO_DEPARTMENT = 19
    IPEECS_DEPARTMENT = 20
    AP_DEPARTMENT = 21
    GP_DEPARTMENT = 22
    SS_DEPARTMENT = 23
    GA_DEPARTMENT = 24
    HK_DEPARTMENT = 25
    LS_DEPARTMENT = 26
    BM_DEPARTMENT = 27
    DEPARTMENT_CHOICES = [(CL_DEPARTMENT, '中國文學系'), (EL_DEPARTMENT, '英美語文學系'), 
                       (FR_DEPARTMENT, '法國語文學系'), (IPLA_DEPARTMENT, '文學院學士班'),
                       (CM_DEPARTMENT, '化學系'), (OS_DEPARTMENT, '光電科學與工程學系'),
                       (JS_DEPARTMENT, '理學院學士班'), (CI_DEPARTMENT, '土木工程學系'), 
                       (ME_DEPARTMENT, '機械工程學系'), (CH_DEPARTMENT, '化學工程與材料工程學系'), 
                       (EI_DEPARTMENT, '工學院學士班'), (BA_DEPARTMENT, '企業管理學系'), 
                       (MIS_DEPARTMENT, '資訊管理學系'), (FM_DEPARTMENT, '財務金融學系'),
                       (EC_DEPARTMENT, '經濟學系'), (EE_DEPARTMENT, '電機工程學系'),
                       (CE_DEPARTMENT, '資訊工程學系'), (CO_DEPARTMENT, '通訊工程學系'),
                       (IPEECS_DEPARTMENT, '資訊電機學院學士班'), (AP_DEPARTMENT, '大氣科學學系'),
                       (GP_DEPARTMENT, '地球科學學系'), (SS_DEPARTMENT, '太空工程與科學學系'),
                       (GA_DEPARTMENT, '地科院學士班'), (HK_DEPARTMENT, '客家語文暨社會科學學系'), 
                       (LS_DEPARTMENT, '生命科學系'), (BM_DEPARTMENT, '生醫工程與科學學系')]
    department = models.IntegerField(choices=DEPARTMENT_CHOICES, null=True)

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
        return self.reason
        
class Image(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    