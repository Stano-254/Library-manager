"""
This to test services module
"""
import datetime

import pytest
#
from mixer.backend.django import mixer

#
# # nonspection SpellCheckingInspection
#
pytestmark = pytest.mark.django_db


class TestBaseModel(object):
    def test_state(self):
        """ Test for state model """
        state = mixer.blend('base.State', name="Active")
        assert state is not None, 'should create a state'

    def test_transaction_type(self):
        """ Test for transaction type model"""
        trans_type = mixer.blend('base.TransactionType', name="RegisterMember")
        assert trans_type is not None, 'Should create a transaction type'
        assert trans_type.name == "RegisterMember", 'should return specific transaction type'

    def test_transactions(self):
        """ Test for transaction model"""
        trans = mixer.blend('base.Transaction')
        assert trans is not None, 'Should create a transaction'

