from django.db import models

from base.models import State, GenericBaseModel, salutations, BaseModel
from members.models import Members

# code 300.
# Create your models here.
# 001
class Author(GenericBaseModel):

    salutation = models.CharField(choices=salutations(), max_length=5)
    state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.salutation} {self.name}"

#002
class Category(GenericBaseModel):
    state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    class Meta(object):
        ordering = ('name',)
#003
class Books(BaseModel):
    title = models.CharField(max_length=100)
    published_date = models.DateField()
    edition = models.CharField(max_length=10)
    ISBN = models.CharField(max_length=25, unique=True)
    book_image = models.ImageField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.author}"

#004
class BookIssued(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(auto_now_add=True)
    borrow_duration = models.IntegerField(default=0)
    return_date = models.DateTimeField()
    return_fee = models.DecimalField(default=0.0, decimal_places=2, max_digits=16)
    fee_paid = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book} - {self.member} - {self.return_date}"


