# code 200

from django.db import models

from base.models import BaseModel, gender, State


# Create your models here.
class Members(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=50,unique=True)
    mobile_no = models.CharField(max_length=15)
    gender = models.CharField(max_length=2,choices=gender())
    membership_no = models.CharField(max_length=10,unique=True)
    state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

