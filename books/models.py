import datetime
from datetime import timedelta
from django.db import models
from base.models import State, GenericBaseModel, salutations, BaseModel
from members.models import Members

# code 300.
# Create your models here.
# 001
class Author(BaseModel):
    salutation = models.CharField(choices=salutations(), max_length=5)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True, null=True)
    state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.salutation} {self.first_name} {self.last_name}"

# 002
class Category(GenericBaseModel):
    state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    class Meta(object):
        ordering = ('name',)

# 003
class Books(BaseModel):
    title = models.CharField(max_length=100)
    published_date = models.DateField()
    edition = models.CharField(max_length=10)
    isbn = models.CharField(max_length=25, unique=True)
    book_image = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    no_of_books = models.IntegerField(default=1)
    no_of_reserve_books = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.author}"


# 004
class BookIssued(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(auto_now_add=True)
    borrow_duration = models.IntegerField(default=0)
    return_date = models.DateTimeField(blank=True,null=True)
    return_fee = models.DecimalField(default=0.0, decimal_places=2, max_digits=16)
    total_fee = models.DecimalField(default=0.0, decimal_places=2, max_digits=16)
    fee_paid = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book} - {self.member} - {self.return_date}"

    def save(self, *args, **kwargs):
        """
            Override save method  to ensure valid return date have been saved.
        """
        self.return_date = datetime.datetime.now() + timedelta(days=int(self.borrow_duration))
        super(BookIssued, self).save(*args, **kwargs)


class BookFees(models.Model):
    borrow_fee = models.DecimalField(default=0.0, decimal_places=2, max_digits=16)
    late_return_rate = models.IntegerField(default=0, help_text="rate of the initial charge per day")
    max_borrow_fee_limit = models.DecimalField(default=500.0, decimal_places=2, max_digits=16)

    def __str__(self):
        return f"{self.borrow_fee} {self.late_return_rate}"
