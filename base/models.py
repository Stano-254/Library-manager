import uuid

from django.db import models


# Create your models here.
def salutations():
    """
    return collection of salutation tittles
    :return: salutation choices
    """
    return [('Prof', 'Professor'), ('Dr', 'Doctor'), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Ms', 'Ms')]


def gender():
    """
    return a collection of gender
    :return:  tuple choice
    """
    return [('M', 'Male'), ('F', 'Female')]


class BaseModel(models.Model):
    """
    template for others classes to reuse
    """
    id = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        abstract = True


class GenericBaseModel(BaseModel):
    """
    template class for other classes with description and name
    """
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta(object):
        abstract = True


class State(GenericBaseModel):
    """
    defines states within the system i.e. State Active, Archived, Deleted
    """

    def __str__(self):
        return f"{self.name}"

    class Meta(object):
        ordering = ('name',)

    @classmethod
    def default_state(cls):
        """
        set default state for any model
        :return:
        """
        try:
            state = cls.objects.get(name="Active")
        except Exception as e:
            state = None
        return state


class TransactionType(GenericBaseModel):
    """
    store types of transaction in the database e.g. add member
    """
    simple_name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.simple_name}"

    class Meta(GenericBaseModel.Meta):
        unique_together = ('name',)


class Transaction(BaseModel):
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    request = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    response_code = models.CharField(max_length=20, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type} {self.state})"
