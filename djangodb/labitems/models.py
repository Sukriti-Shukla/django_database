from django.db import models
from django.contrib.postgres.fields import ArrayField
import json
from django.contrib.auth.models import User


# Create your models here.
class Chemical(models.Model):
    labitemtype = models.CharField(max_length=100)
    labitemsubtype = models.CharField(max_length=100)
    labitemid = models.IntegerField()
    labitemname =  models.CharField(max_length=100)
    documents =  models.ImageField(upload_to='images/',null=True,blank=True)
    files =  models.FileField(upload_to='docs/',null=True,blank=True)
    json_data = models.JSONField(blank=True, null=True)
    additional_fields = models.TextField(blank=True, null=True)
    custom_fields = ArrayField(models.CharField(max_length=100),blank=True,null=True)
    last_modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def set_additional_fields(self, fields):
        self.additional_fields = json.dumps(fields)

    def get_additional_fields(self):
        if self.additional_fields:
            return json.loads(self.additional_fields)
        return {}

    
    def save(self, *args, **kwargs):
        if isinstance(self.additional_fields, dict):
            self.additional_fields = json.dumps(self.additional_fields)
        super().save(*args, **kwargs)

    


    def __str__(self):
        return self.labitemname 

