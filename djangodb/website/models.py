from django.db import models

# Create your models here.
class Chemical(models.Model):
    labitemtype = models.CharField(max_length=100)
    labitemsubtype = models.CharField(max_length=100)
    labitemid = models.IntegerField()
    labitemname =  models.CharField(max_length=100)
    
    def __str__(self):
        return self.labitemname 
