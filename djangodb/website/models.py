from django.db import models

# Create your models here.
class Chemical(models.Model):
    labitemtype = models.CharField(max_length=100)
    labitemsubtype = models.CharField(max_length=100)
    labitemid = models.IntegerField()
    labitemname =  models.CharField(max_length=100)
    documents =  models.ImageField(upload_to='images/',null=True,blank=True)
    json_data = models.JSONField(blank=True, null=True)
    def __str__(self):
        return self.labitemname 
