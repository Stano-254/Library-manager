import pytest
from mixer.backend.django import mixer

from members.backend.service import MemberService

pytestmark = pytest.mark.django_db


@pytestmark
class TestMemberService(object):
    """
     Test the Member  services
    """

    def test_get(self):
        mixer.blend('base.State', name="Active")
        mixer.blend('members.Members', national_id="345678", first_name="John", last_name="Kayumba")
        member = MemberService().get(national_id="345678")
        assert member is not None, 'Should have a Member object'

    def test_filter(self):
        """ Test for filter Member Model  service"""
        mixer.blend('base.State', name="Active")
        mixer.cycle(4).blend('members.Members')
        members = MemberService().filter()
        assert members is not None, 'Should return a queryset of Members'
        assert len(members) == 4, 'should return four Members'

    def test_create(self):
        """ Test for create Member Model service """
        mixer.blend('base.State', name="Active")
        kwargs = {
            'first_name': "John",
            'last_name': 'Sakaja',
            'national_id': '345678',
            'gender': 'Female',
            'membership_no': '234567',
            'state': mixer.blend('base.State', name='Active')

        }
        member = MemberService().create(**kwargs)
        assert member is not None, 'should return created Member object'

    def test_update(self):
        mixer.blend('base.State', name="Active")
        old_member = mixer.blend('members.Members', first_name="John", last_name="Kamau", membership_no='2345')
        updated_member = MemberService().update(old_member.id, membership_no='345678')
        assert updated_member.membership_no == '345678', 'Should have an updated instance of Member'
