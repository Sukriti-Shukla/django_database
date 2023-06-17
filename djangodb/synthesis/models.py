from django.db import models
from django.contrib.postgres.fields import ArrayField
import json

class SynthesisChemical(models.Model):
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)
    precursor_chemicals = models.JSONField(blank=True, null=True) 
    synthesized_by = models.CharField(max_length=200)
    synthesized_on = models.DateField()
    added_by = models.CharField(max_length=200)
    added_on = models.DateField()
    proceduretype = models.CharField(max_length=200,blank=True, null=True)
    proceduresubtype = models.CharField(max_length=200,blank=True, null=True)
    description = models.TextField(max_length=2000,blank=True, null=True)
    custom_parameters = ArrayField(models.CharField(max_length=100),blank=True,null=True)
    additional_fields = models.TextField(blank=True, null=True)
    files =  models.FileField(upload_to='docs/',null=True,blank=True)

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
        return self.name
    

