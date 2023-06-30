# code 200
import re

from django.db import models

from base.models import BaseModel, gender, State


# Create your models here.
#001
class Members(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=50, unique=True)
    mobile_no = models.CharField(max_length=15)
    gender = models.CharField(max_length=2, choices=gender())
    membership_no = models.CharField(max_length=10, unique=True, null=True,blank=True)
    state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """
            Override save method  to ensure valid member have been saved.
        """
        if Members.objects.filter(membership_no=self.membership_no):
            super(Members, self).save(*args, **kwargs)
        else:
            last_member_no = Members.objects.filter().order_by("-date_created").first()
            member_no = last_member_no.membership_no if last_member_no else "LB0000"
            ref = re.sub(r'[0-9]+$', lambda x: f"{str(int(x.group()) + 1).zfill(len(x.group()))}", member_no)
            self.membership_no = ref
            super(Members, self).save(*args, **kwargs)
