from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    schoolid=models.CharField(max_length=20,default="540000000000")
    schoolpassword=models.CharField(max_length=256,default="zzuli000000")
    mobile=models.CharField(max_length=20,default="16666666666")
    homemobile=models.CharField(max_length=20,default="16666666666")
    region=models.CharField(max_length=20,default="0")
    area=models.CharField(max_length=20,default="0")
    build=models.CharField(max_length=20,default="0")
    dorm=models.CharField(max_length=20,default="200")
    schoolgps=models.CharField(max_length=80,default="河南省郑州市金水区郑州轻工业大学第二学生园区")
    schoollat=models.CharField(max_length=20,default="34.48000")
    schoollon=models.CharField(max_length=20,default="113.39190")

    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户' # 这里应该是控制后台显示用户的地方
        verbose_name_plural = '用户'