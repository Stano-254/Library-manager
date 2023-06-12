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
