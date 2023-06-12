"""
this service base to centralize CRUD operations for all the service to inherit from
"""
import logging

lgr = logging.getLogger(__name__)


class ServiceBase(object):
    """
    Handles CRUD methods
    """
    manager = None

    def __int__(self, lock_for_update=False, *args, **annotations):
        """
         Initialize service to ensure if transaction is locked if need be.
        :param lock_for_update: determines whether to lock model
        :type lock_for_update: bool
        :param args: strictly ordered annotations respecting the order of params
        :param annotations: key-word argument for annotations. behave like model columns on the model
        :return:
        """
        super(ServiceBase, self).__init__()
        if lock_for_update and self.manager:
            self.manager = self.manager.select_for_update()
            if args:  # set up ordered tuples
                for arg in args:
                    if isinstance(args, tuple):
                        try:
                            data_dict = {'%s' % arg[0]: arg[1]}
                            self.manager = self.manager.annotate(**data_dict)
                        except Exception as e:
                            lgr.warning(f"Initialization of args error {e}")
            if annotations:
                self.manager = self.manager.annotate(**annotations)

    def get(self, *args, **kwargs):
        """
        This handles retrieval of single record from database
        :param args: arguments to pass to get method
        :param kwargs: key-word arguments to pass to get method
        :return: return an instance of manager
        """
        try:
            if self.manager:
                return self.manager.get(*args, **kwargs)
        except Exception as e:
            lgr.exception(f"{self.manager.model.__name__} service get exception: {e}")
        return None

    def filter(self, *args, **kwargs):
        """
        This method returns queryset of all object fetched from database
        :param args: Arguments passed to filter method
        :param kwargs: dict argument to pass to the filter method
        :return: Queryset | None
        """
        try:
            if self.manager:
                return self.manager.filter(*args, **kwargs)
        except self.manager.model.DoesNotExist as e:
            lgr.exception(f"{self.manager.model.__name__} service filter exception: {e}")
        except Exception as ex:
            lgr.exception(f"{self.manager.model.__name__} service filter General  exception: {ex}")
        return None

    def create(self, **kwargs):
        """
        This method for creation of data using provided kwargs
        :param kwargs: dict of key-value to be used for creation
        :return: Created obj
        """
        try:
            if self.manager:
                return self.manager.create(**kwargs)
        except Exception as e:
            lgr.exception(f"{self.manager.model.__name__} service filter General  exception: {e}")
        return None

    def update(self, pk, **kwargs):
        """
        Handles updating of a specific record
        :param pk: primary key of the record
        :param kwargs:  other params to use for update
        :return: the updated record
        """
        try:
            record = self.get(id=pk)
            if record:
                for k, v in kwargs.items():
                    setattr(record, k, v)
                record.save()
                record.refresh_from_db()
                return record
        except Exception as e:
            lgr.exception(f"{self.manager.model.__name__} service update General  exception: {e}")
        return None
