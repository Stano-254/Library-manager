"""
Transaction logs
"""
import logging
from django.db import transaction
from base.backend.service import StateService, TransactionService, TransactionTypeService
from base.backend.utils.utilities import get_request_data

lgr = logging.getLogger(__name__)


class TransactionLogBase(object):
    """
    The class for logging transactions.
    """
    @staticmethod
    def complete_transaction(transactions, **kwargs):
        """
        Marks the transaction object as complete.
        :param transactions: Transaction obj we are updating
        :type transactions: Transaction
        :param kwargs: arguments to pass during updating
        :return: The transaction updated
        :rtype: Transaction | None
        """
        try:
            if 'state' not in kwargs:
                kwargs['state'] = StateService().get(name='Completed')
            return TransactionService().update(transactions.id, **kwargs)
        except Exception as e:
            lgr.exception('complete_transaction Exception: %s', e)
        return None

    @staticmethod
    def log_transaction(transaction_type, **kwargs):
        """
        Logs a transaction type having the provided arguments.
        :param transaction_type: The name of the type of transaction we are creating.
        :type transaction_type: str
        :param kwargs: key value arguments to generate the transaction.
        :return: The created transaction.
        :rtype: Transaction | None
        """
        try:
            with transaction.atomic():
                transaction_type = TransactionTypeService().get(name=transaction_type)
                if 'state' not in kwargs:
                    kwargs['state'] = StateService().get(name="Active")
                if 'request' in kwargs:
                    request = kwargs.pop('request', {})
                    kwargs['user'] = getattr(request, 'user', None)
                    data = get_request_data(request)
                    if data:
                        kwargs['source_ip'] = data.get('source_ip', None)
                        kwargs['request'] = data
                return TransactionService().create(transaction_type=transaction_type, **kwargs)
        except Exception as e:
            print(f"error in logs {e}")
            lgr.exception('log_transaction Exception: %s', e)
        return None

    @staticmethod
    def mark_transaction_failed(transaction_obj, **kwargs):
        """
        Marks the transaction object as Failed.
        :param transaction_obj: The transaction we are updating.
        :type transaction_obj: Transaction
        :param kwargs: Any key->word arguments to pass to the method.
        :return: The transaction updated.
        :rtype: Transaction | None
        """
        try:
            if kwargs is None:
                kwargs = {'state': StateService().get(name='Failed')}
            else:
                kwargs['state'] = StateService().get(name='Failed')
            return TransactionService().update(transaction_obj.id, **kwargs)
        except Exception as e:
            lgr.exception('mark_transaction_failed Exception: %s', e)
        return None
