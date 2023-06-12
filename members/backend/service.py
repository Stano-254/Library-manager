from base.backend.servicebase import ServiceBase
from members.models import Members


class MemberService(ServiceBase):
    """ members model CRUD operations """
    manager = Members.objects
