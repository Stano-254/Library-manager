from base.backend.servicebase import ServiceBase
from base.models import State, TransactionType, Transaction, UserIdentity


class StateService(ServiceBase):
    """ Service class for state"""
    manager = State.objects

class TransactionTypeService(ServiceBase):
    """ Service for Transaction type"""
    manager = TransactionType.objects

class TransactionService(ServiceBase):
    """ Service for transaction """
    manager = Transaction.objects

class UserIdentityService(ServiceBase):
    """ Service for transaction """
    manager = UserIdentity.objects