from django.db import models

from base.models import BaseModel, gender


# Create your models here.
class Members(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=15)
    gender = models.CharField(max_length=2)
    membership_no = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

