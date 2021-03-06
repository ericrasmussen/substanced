Building a Retail Application
-----------------------------

It's not the intent that normal unprivleged users of an application you build
using Substance D ever see the :term:`SDI` management interface.  That
interface is reserved for privileged users, like you and your staff.

To build a "retail" application, you just use normal Pyramid :term:`view
configuration` to associate objects with view logic based on the content
types provided to you by Substance D and the content types you've defined.

For example, here's a view that will respond on the root Substance D "site"
object and return its title:

.. code-block:: python
   :linenos:

   from pyramid.view import view_config
   from substanced.interfaces import ISite

   @view_config(context=ISite)
   def hello(request):
       html = '<html><head></head><body>Hello from %s!</body></html>'
       request.response.body = html % request.context.title
       return request.response

Note that we did *not* use the :class:`substanced.sdi.mgmt_view` decorator.
Instead we used the :class:`pyramid.view.view_config` decorator, which will
expose the view to normal site visitors, not just those visiting the
resource via the :term:`SDI`.

Substance D exposes a :term:`resource tree` that you can hang views from to
build your application.  You'll want to read up on :term:`traversal` to
understand how to associate view configuration with :term:`resource` objects.
