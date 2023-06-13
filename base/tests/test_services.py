import pytest
from mixer.backend.django import mixer

from base.backend.service import StateService, TransactionTypeService, TransactionService

pytestmark = pytest.mark.django_db


@pytestmark
class TestStateService(object):
    """
     Test the state Model services
    """

    def test_get(self):
        mixer.blend('base.State', name="Active")
        state = StateService().get(name='Active')
        assert state is not None, 'Should have a State object'

    def test_filter(self):
        """ Test for filter state service"""
        mixer.cycle(4).blend('base.State')
        states = StateService().filter()
        assert states is not None, 'Should return a queryset of states'
        assert len(states) == 4, 'should return four states'

    def test_create(self):
        """ Test for create test service """
        state_active = StateService().create(name="Active", description="Active state")
        assert state_active is not None, 'should return created State object'

    def test_update(self):
        old_state = mixer.blend('base.State', name="Completed")
        new_state = StateService().update(old_state.id, name='Active')
        assert new_state.name is not old_state, 'Should have an updated instance of State'


class TestTransactionTypeService(object):
    """
    Test for all CRUD Services for TransactionType
    """

    def test_get(self):
        """ Test for get method on TransactionType"""
        mixer.blend('base.TransactionType', name='RegisterMember')
        transaction_type = TransactionTypeService().get(name="RegisterMember")
        assert transaction_type is not None, 'Should return instance of TransactionType'

    def test_filter(self):
        """ Test for filter method on TransactionType"""
        mixer.cycle(4).blend('base.TransactionType')
        transaction_type = TransactionTypeService().filter()
        assert transaction_type is not None, 'Should return queryset of TransactionTypes'
        assert len(transaction_type) == 4, 'Should return 4 TransactionTypes'

    def test_create(self):
        """ Test for create method on TransactionType"""
        kwargs = {
            'name': 'RegisterMember',
            'simple_name': 'Register Member',
            'state': mixer.blend('base.State', name='Active'),
        }
        transaction_type = TransactionTypeService().create(**kwargs)
        assert transaction_type is not None, 'Should return TransactionType instance'
        assert transaction_type.name == 'RegisterMember', 'Transaction created should match supplied name'

    def test_update(self):
        """ Test for update method on TransactionType"""
        transaction_type = mixer.blend('base.TransactionType', name='RegisterMember')
        new_transaction_type = TransactionTypeService().update(transaction_type.id, simple_name='Register Member')
        assert new_transaction_type.simple_name == "Register Member", 'Should have an updated TransactionType'


class TestTransactionService(object):
    def test_get(self):
        state = mixer.blend('base.State', name="Active")
        mixer.blend('base.Transaction', state=state, transaction_type__name="RegisterMember")
        transaction = TransactionService().get(transaction_type__name='RegisterMember')
        assert transaction is not None, 'Should return Transaction instance'

    def test_filter(self):
        mixer.cycle(4).blend('base.Transaction')
        transactions = TransactionService().filter()
        assert len(transactions) == 4, 'Should return 4 instances of Transaction'

    def test_create(self):
        kwargs = {
            'transaction_type': mixer.blend('base.TransactionType'),
            'state': mixer.blend('base.State')}
        transaction = TransactionService().create(**kwargs)
        assert transaction is not None, 'Should return Transaction instance'

    def test_update(self):
        transaction_type = mixer.blend('base.TransactionType', name="RegisterMember")
        old_trans = mixer.blend('base.Transaction')
        new_trans = TransactionService().update(old_trans.id, transaction_type=transaction_type)
        assert new_trans.transaction_type == transaction_type, 'Should return an updated transaction'
