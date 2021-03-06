import transaction
import colander

from pyramid.exceptions import ConfigurationError
from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    )

from pyramid_zodbconn import get_connection

from ..interfaces import ISite
from ..objectmap import ObjectMap
from ..catalog import Catalog
from ..schema import Schema
from ..folder import Folder
from ..principal import Principals
from ..acl import NO_INHERIT
from ..content import content
from ..util import oid_of

class SiteSchema(Schema):
    """ The schema representing site properties. """
    title = colander.SchemaNode(colander.String(),
                                missing=colander.null)
    description = colander.SchemaNode(colander.String(),
                                      missing=colander.null)

@content(ISite, icon='icon-home')
class Site(Folder):
    """ An object representing the root of a Substance D site.  Contains
    ``objectmap``, ``catalog``, and ``principals`` services.  Initialize with
    an initial login name and password: the resulting user will be granted
    all permissions."""
    
    __propschema__ = SiteSchema()
    
    title = ''
    description = ''

    def __init__(self, initial_login, initial_email, initial_password):
        Folder.__init__(self)
        objectmap = ObjectMap()
        catalog = Catalog()
        principals = Principals()
        self.add_service('objectmap', objectmap)
        self.add_service('catalog', catalog)
        self.add_service('principals', principals)
        user = principals['users'].add_user(
            initial_login, initial_password, initial_email
            )
        group = principals['groups'].add_group('admininstrators')
        group.connect(user)
        catalog.refresh()
        objectmap.add(self, ('',))
        self.__acl__ = [(Allow, oid_of(group), ALL_PERMISSIONS)]
        self['__services__'].__acl__ = [
            (Allow, oid_of(group), ALL_PERMISSIONS),
            NO_INHERIT,
            ]

    def get_properties(self):
        return dict(title=self.title, description=self.description)

    def set_properties(self, struct):
        self.__dict__.update(struct)
        self._p_changed = True

    @classmethod
    def root_factory(cls, request, transaction=transaction, 
                     get_connection=get_connection):
        """ A classmethod which can be used as a Pyramid ``root_factory``.
        It accepts a request and returns an instance of Site."""
        # this is a classmethod so that it works when Site is subclassed.
        conn = get_connection(request)
        zodb_root = conn.root()
        if not 'app_root' in zodb_root:
            settings = request.registry.settings
            password = settings.get(
                'substanced.initial_password')
            if password is None:
                raise ConfigurationError(
                    'You must set a substanced.initial_password '
                    'in your configuration file')
            username = settings.get(
                'substanced.initial_login', 'admin')
            email = settings.get(
                'substanced.initial_email', 'admin@example.com')
            app_root = cls(username, email, password)
            zodb_root['app_root'] = app_root
            transaction.commit()
        return zodb_root['app_root']

def includeme(config): # pragma: no cover
    config.add_content_type(ISite, Site)
    config.scan('.views')
    
