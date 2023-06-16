import logging

from base.backend.transactionlogbase import TransactionLogBase
from base.backend.utils.utilities import validate_name
from members.backend.service import MemberService
from django.forms.models import model_to_dict

lgr = logging.getLogger(__name__)


class MembersAdministration(TransactionLogBase):
    """
    handle the administration functionality relating to members including CRUD
    """

    def create_member(self, request, **kwargs):
        """
          Handles adding of members in the library system
          :param request: the original request
          :param kwargs: keyword arguments for creation of member.
          :return: dict response with code
          """
        transaction = None
        try:
            transaction = self.log_transaction('CreateMember', request=request, user=request.user)
            if not transaction:
                return {'code': '900.500.500', 'message': 'Create member transaction failed'}
            first_name = kwargs.get('first_name')
            last_name = kwargs.get('last_name')
            if not validate_name(first_name):
                self.mark_transaction_failed(transaction, message="Invalid first name")
                return {'code': '500.400.003', 'message': 'Invalid first name'}
            if not validate_name(last_name):
                self.mark_transaction_failed(transaction, message="Invalid last name")
                return {'code': '500.400.003', 'message': 'Invalid last name'}
            member = MemberService().create(**kwargs)
            if not member:
                self.mark_transaction_failed(
                    transaction, message='Failed to create member', response_code='200.001.003')
                return {'code': '200.001.003', 'message': 'Failed to create member'}
            self.complete_transaction(transaction, message='Success')
            return {'code': '100.000.000', 'message': 'success', 'data': model_to_dict(member)}
        except Exception as e:
            lgr.exception(f"Exception occurred during create of member :{e}")
            self.mark_transaction_failed(transaction, response=str(e))
            return {'code': '999.999.999', 'message': 'Error occurred during creation of member'}

    def get_member(self, request, member_id):
        """
        handle fetching of one member
        :param request: original request as received
        :param member_id: the unique identifier of the member
        :return: HttpResponse with member data
        """
        pass

    def get_members(self, request, **kwargs):
        """
        Handles fetching of multiple user, either with added conditions
        (like active members or inactive members etc.) or without conditions
        :param request: original request received
        :param kwargs: The parameters used to filter based on conditions if any.
        :return: dict response of a list of all user based on conditions provided
        """
        pass

    def update_member(self, request, member_id, **kwargs):
        """
        Handles updating of members personal information or
        any other information related to members
        :param request: Original Django HTTP request
        :type request: WSGIRequest
        :param member_id:
        :param kwargs: dict of other parameters
        :return: dict response
        """
        pass

    def delete_member(self, request, member_id):
        """
        Handles deletion of user from the system hypothetically
        though the user is never deleted just updated to state deleted
        :param request: Original Django HTTP request
        :param member_id: the unique member identifier
        :return: dict response with code
        """
        pass
