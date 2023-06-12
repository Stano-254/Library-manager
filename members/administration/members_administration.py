class MembersAdministration(object):
    """
    handle the administration functionality relating to members including CRUD
    """

    def create_member(self, request, kwargs):
        """
          Handles adding of members in the library system
          :param request: the original request
          :param kwargs: keyword arguments for creation of member.
          :return: dict response with code
          """
        pass

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
