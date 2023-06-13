"""
This to test members  module
"""
import pytest
#
from mixer.backend.django import mixer

#
# # nonspection SpellCheckingInspection
#
pytestmark = pytest.mark.django_db


class TestMembersModels(object):
    """ Test cases for all models under members module"""

    def test_members(self):
        mixer.blend('base.State', name='Active')
        member = mixer.blend('members.Members')
        assert member is not None, 'Should return a member object'
        assert member.__str__() == f"{member.first_name} {member.last_name}",\
            "'Should have a Member object string  representation'"
