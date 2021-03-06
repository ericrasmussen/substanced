from zope.interface.interfaces import IObjectEvent

from zope.interface import (
    Interface,
    Attribute,
    )

class IContent(Interface):
    """ Marker interface representing an object that has a content type """

class ICatalogable(Interface):
    """ Marker interface describing catalogable content.  An object must
    implement this interface to have its attributes indexed """

class IPropertied(Interface):
    """ Interface for objects with a set of properties defined by a Colander
    schema"""
    __propschema__ = Attribute('Colander schema which denotes property schema')

    def get_properties():
        """ Returns a data structure representing the current property state
        according to the attached __propschema__ (usually a dictionary)."""

    def set_properties(struct):
        """ Persists a data structure representing the property state
        represented by ``struct`` (usually a dictionary).  The data structure
        will have already been validated against the __propschema__."""
        
class IObjectMap(Interface):
    """ A map of objects to paths and a reference engine """
    def objectid_for(obj_or_path_tuple):
        """ Return the object id for obj_or_path_tuple """
        
    def path_for(objectid):
        """ Return the path tuple for objectid """

    def object_for(objectid):
        """ Return the object associated with ``objectid`` or ``None`` if the
        object cannot be found."""
        
    def add(obj):
        """ Add a new object to the object map.  Assigns a new objectid to
        obj.__objectid__ to the object if it doesn't already have one.  The
        object's path or objectid must not already exist in the map.  Returns
        the object id."""
        
    def remove(obj_objectid_or_path_tuple):
        """ Removes an object from the object map using the object itself, an
        object id, or a path tuple.  Returns a set of objectids (children,
        inclusive) removed as the result of removing this object from the
        object map."""
        
    def pathlookup(obj_or_path_tuple, depth=None, include_origin=True):
        """ Returns an iterator of document ids within
        obj_or_path_tuple (a traversable object or a path tuple).  If depth
        is specified, returns only objects at that depth.  If
        ``include_origin`` is ``True``, returns the docid of the object
        passed as ``obj_or_path_tuple`` in the returned set, otherwise it
        omits it."""
        
    def connect(src, target, reftype):
        """Connect ``src_object`` to ``target_object`` using the reference
        type ``reftype``.  ``src`` and ``target`` may be objects or object
        identifiers."""

    def disconnect(src, target, reftype):
        """Disonnect ``src_object`` from ``target_object`` using the
        reference type ``reftype``. ``src`` and ``target`` may be objects or
        object identifiers"""

    def sources(obj, reftype):
        """ Return a generator consisting of objects which have ``obj`` as a
        relationship source using ``reftype``.  ``obj`` can be an object or
        an object id."""
        
    def targets(obj, reftype):
        """ Return a generator consisting of objects which have ``obj`` as a
        relationship target using ``reftype``. ``obj`` can be an object or an
        object id."""

    def targetids(obj, reftype):
        """ Return a set of objectids which have ``obj`` as a relationship
        target using ``reftype``.  ``obj`` can be an object or an object id."""

    def sourceids(obj, reftype):
        """ Return a set of objectids which have ``obj`` as a relationship
        source using ``reftype``.  ``obj`` can be an object or an object id."""
        
class ICatalog(Interface):
    """ A collection of indices """
    objectids = Attribute(
        'a sequence of objectids that are cataloged in this catalog')

class ISite(IPropertied):
    """ Marker interface for something that is the root of a site """

class ISearch(Interface):
    """ Adapter for searching the catalog """

class IObjectWillBeAdded(IObjectEvent):
    """ An event type sent when an before an object is added """
    object = Attribute('The object being added')
    parent = Attribute('The folder to which the object is being added')
    name = Attribute('The name which the object is being added to the folder '
                     'with')

class IObjectAdded(IObjectEvent):
    """ An event type sent when an object is added """
    object = Attribute('The object being added')
    parent = Attribute('The folder to which the object is being added')
    name = Attribute('The name of the object within the folder')

class IObjectWillBeRemoved(IObjectEvent):
    """ An event type sent before an object is removed """
    object = Attribute('The object being removed')
    parent = Attribute('The folder from which the object is being removed')
    name = Attribute('The name of the object within the folder')
    moving = Attribute('Boolean indicating that this removal is part of an '
                       'object move')

class IObjectRemoved(IObjectEvent):
    """ An event type sent when an object is removed """
    object = Attribute('The object being removed')
    parent = Attribute('The folder from which the object is being removed')
    name = Attribute('The name of the object within the folder')
    moving = Attribute('Boolean indicating that this removal is part of an '
                       'object move')

class IObjectModified(IObjectEvent):
    """ May be sent when an object is modified """
    object = Attribute('The object being modified')

class IFolder(Interface):
    """ A Folder which stores objects using Unicode keys.

    All methods which accept a ``name`` argument expect the
    name to either be Unicode or a byte string decodable using the
    default system encoding or the UTF-8 encoding."""

    order = Attribute("""Order of items within the folder
    (Optional) If not set on the instance, objects are iterated in an
    arbitrary order based on the underlying data store.""")

    def keys():
        """ Return an iterable sequence of object names present in the folder.

        Respect ``order``, if set.
        """

    def __iter__():
        """ An alias for ``keys``
        """

    def values():
        """ Return an iterable sequence of the values present in the folder.

        Respect ``order``, if set.
        """

    def items():
        """ Return an iterable sequence of (name, value) pairs in the folder.

        Respect ``order``, if set.
        """

    def get(name, default=None):
        """ Return the object named by ``name`` or the default.

        ``name`` must be a Unicode object or a bytestring object.

        If ``name`` is a bytestring object, it must be decodable using the
        system default encoding or the UTF-8 encoding.
        """

    def __contains__(name):
        """ Does the container contains an object named by name?

        ``name`` must be a Unicode object or a bytestring object.

        If ``name`` is a bytestring object, it must be decodable using the
        system default encoding or the UTF-8 encoding.
        """

    def __nonzero__():
        """ Always return True
        """

    def __len__():
        """ Return the number of subobjects in this folder.
        """

    def __setitem__(name, other):
        """ Set object ``other' into this folder under the name ``name``.

        ``name`` must be a Unicode object or a bytestring object.

        If ``name`` is a bytestring object, it must be decodable using the
        system default encoding or the UTF-8 encoding.

        ``name`` cannot be the empty string.

        When ``other`` is seated into this folder, it will also be
        decorated with a ``__parent__`` attribute (a reference to the
        folder into which it is being seated) and ``__name__``
        attribute (the name passed in to this function.

        If a value already exists in the foldr under the name ``name``, raise
        :exc:`KeyError`.

        When this method is called, emit an ``IObjectWillBeAdded`` event
        before the object obtains a ``__name__`` or ``__parent__`` value.
        Emit an ``IObjectAdded`` event after the object obtains a ``__name__``
        and ``__parent__`` value.
        """

    def add(name, other, send_events=True, allow_services=False):
        """ Same as ``__setitem__``.

        If ``send_events`` is false, suppress the sending of folder events.
        If ``allow_services`` is True, allow the name ``__services__`` to be
        added.
        """

    def check_name(name, allow_services=False):
        """
        Checks the name passed for validity.  If the name is valid, and the
        name does not already exist in the folder, returns a validated name.
        If the name is not valid, a ValueError will be raised.  """

    def pop(name, default=None):
        """ Remove the item stored in the under ``name`` and return it.

        If ``name`` doesn't exist in the folder, and ``default`` **is not**
        passed, raise a :exc:`KeyError`.

        If ``name`` doesn't exist in the folder, and ``default`` **is**
        passed, return ``default``.

        When the object stored under ``name`` is removed from this folder,
        remove its ``__parent__`` and ``__name__`` values.

        When this method is called, emit an ``IObjectWillBeRemoved`` event
        before the object loses its ``__name__`` or ``__parent__`` values.
        Emit an ``ObjectRemoved`` after the object loses its ``__name__``
        and ``__parent__`` value,
        """

    def __delitem__(name):
        """ Remove the object from this folder stored under ``name``.

        ``name`` must be a Unicode object or a bytestring object.

        If ``name`` is a bytestring object, it must be decodable using the
        system default encoding or the UTF-8 encoding.

        If no object is stored in the folder under ``name``, raise a
        :exc:`KeyError`.

        When the object stored under ``name`` is removed from this folder,
        remove its ``__parent__`` and ``__name__`` values.

        When this method is called, emit an ``IObjectWillBeRemoved`` event
        before the object loses its ``__name__`` or ``__parent__`` values.
        Emit an ``IObjectRemoved`` after the object loses its ``__name__``
        and ``__parent__`` value,
        """

    def remove(name, send_events=True, moving=False):
        """ Same thing as ``__delitem__``.

        If ``send_events`` is false, suppress the sending of folder events.
        If ``moving`` is True, the events sent will indicate that a move is
        in process.
        """

    def move(name, other, newname=None):
        """
        Move a subobject named ``name`` from this folder to the folder
        represented by ``other``.  If ``newname`` is not none, it is used as
        the target object name; otherwise the existing subobject name is
        used.

        This operation is done in terms of a remove and an add.  The Removed
        and WillBeRemoved events sent will indicate that the object is
        moving.
        """

    def rename(oldname, newname):
        """
        Rename a subobject from oldname to newname.

        This operation is done in terms of a remove and an add.  The Removed
        and WillBeRemoved events sent will indicate that the object is
        moving.
        """
    def replace(name, newobject):
        """ Replace an existing object named ``name`` in this folder with a
        new object ``newobject``.  If there isn't an object named ``name`` in
        this folder, an exception will *not* be raised; instead, the new
        object will just be added.

        This operation is done in terms of a remove and an add.  The Removed
        and WillBeRemoved events will be sent for the old object, and the
        WillBeAdded and Add events will be sent for the new object.e
        """
        
        
class IPrincipal(IPropertied):
    """ Marker interface representing a user or group """

class IUser(IPrincipal):
    """ Marker interface representing a user """

class IGroup(IPrincipal):
    """ Marker interface representing a group """

class IUsers(Interface):
    """ Marker interface representing a collection of users """

class IGroups(Interface):
    """ Marker interface representing a collection of groups """
    
class IPrincipals(Interface):
    """ Marker interface representing a container of users and groups """

class IPasswordResets(Interface):
    """ Marker interface representing a collection of password reset requests
    """

class IPasswordReset(Interface):
    """ Marker interface represent a password reset request """

marker = object()

SERVICES_NAME = '__services__'

