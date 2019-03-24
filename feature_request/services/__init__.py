from feature_request.models import *
from crud_factory import *

ServiceFactory = CRUDFactory

BaseUserService = ServiceFactory.create_service(User, db)
BaseFeatureRequestService = ServiceFactory.create_service(FeatureRequest, db)
BaseClientService = ServiceFactory.create_service(Client, db)
BaseProductAreaService = ServiceFactory.create_service(ProductArea, db)


class UserService(BaseUserService):
    """ Activities of a User """

    @classmethod
    def create(cls, **kwargs):
        """ Register a user account """

        password = kwargs.pop("password", "")

        user = BaseUserService.create(**kwargs)
        user.set_password(password)

        return user


class ClientService(BaseClientService):
    """ Activities of client """

    @classmethod
    def create(cls, **kwargs):
        """ Creates a client """

        client = BaseClientService.query.filter(Client.name == kwargs.get("name"),
                                                Client.email == kwargs.get("email")).first()

        if client:
            return client

        client = BaseClientService.create(**kwargs)
        return client


class ProductAreaService(BaseProductAreaService):
    """ Activities of product area """

    @classmethod
    def create(cls, **kwargs):
        """ Creates a product area """

        product = BaseProductAreaService.query.filter(ProductArea.code == slugify(kwargs.get("name"))).first()

        if product:
            return product

        product = BaseProductAreaService.create(**kwargs)
        return product


class FeatureRequestService(BaseFeatureRequestService):
    """ Activities of feature request"""

    @classmethod
    def create(cls, **kwargs):
        """ Creates a feature request """

        client_priority = kwargs.get("client_priority")
        client_id = kwargs.get("client_id")

        update_priority_chain = False
        if BaseFeatureRequestService.query.filter(FeatureRequest.client_id == client_id,
                                                  FeatureRequest.client_priority == client_priority).count() > 0:
            update_priority_chain = True

        if update_priority_chain:
            cls.reduce_priorities(client_priority)

        obj = BaseFeatureRequestService.create(**kwargs)
        return obj

    @classmethod
    def reduce_priorities(cls, client_priority, **kwargs):

        db.session.query(FeatureRequest).filter(FeatureRequest.client_priority >= client_priority).update(
            {'client_priority': FeatureRequest.client_priority + 1})

        db.session.commit()

        return True
