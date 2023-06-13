"""
This to test base models module
"""
import datetime

import pytest
#
from mixer.backend.django import mixer

#
# # nonspection SpellCheckingInspection
#
pytestmark = pytest.mark.django_db


class TestBaseModels(object):
    def test_state(self):
        """ Test for state model """
        state = mixer.blend('base.State', name="Competed")
        assert state is not None, 'should create a state'
        assert state.__str__() == f"{state.name}", \
            'should return transaction type object string representation'

    def test_default_state(self):
        """ Test for state model """
        state = mixer.blend('base.State', name="Competed")

        # mixer.blend('base.Transaction', state=state.defaut_state())
        assert state.default_state() is None, 'should return None for default state'

    def test_transaction_type(self):
        """ Test for transaction type model"""
        trans_type = mixer.blend('base.TransactionType', name="RegisterMember")
        assert trans_type is not None, 'Should create a transaction type'
        assert trans_type.__str__() == f"{trans_type.simple_name}", \
            'should return transaction type object string representation'

    def test_transactions(self):
        """ Test for transaction model"""
        trans = mixer.blend('base.Transaction')
        assert trans is not None, 'Should create a transaction'
        assert trans.__str__() == f"{trans.transaction_type} {trans.state}", \
            'should have a Transaction object string representation'
