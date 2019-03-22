from feature_request.models import *
from crud_factory import *

ServiceFactory = CRUDFactory

BaseUserService = ServiceFactory.create_service(User, db)
FeatureRequestService = ServiceFactory.create_service(FeatureRequest, db)
ClientService = ServiceFactory.create_service(Client, db)
ProductAreaService = ServiceFactory.create_service(ProductArea, db)


class UserService(BaseUserService):
    """ Register a new user """

    @classmethod
    def create(cls, **kwargs):
        """ Register a non-staff account """

        password = kwargs.pop("password", "")

        user = BaseUserService.create(**kwargs)
        user.set_password(password)

        return user
