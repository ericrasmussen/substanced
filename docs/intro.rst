Introduction
------------

.. sidebar::  A Scanner Darkly

	"The two hemispheres of my brain are competing?" Fred said.

	"Yes."

	"Why?"

	"Substance D. It often causes that, functionally. This is what we
	expected; this is what the tests confirm. Damage having taken place in
	the normally dominant left hemisphere, the right hemisphere is attempting
	to compensate for the impairment. But the twin functions do not fuse,
	because this is an abnormal condition the body isn't prepared for. It
	should never happen. "Cross-cuing", we call it. Related to splitbrain
	phenomena. We could perform a right hemispherectomy, but--"

	"Will this go away," Fred interrupted, "when I get off Substance D?"

	"Probably," the psychologist on the left said, nodding. "It's a
	functional impairment."

	The other man said, "It may be organic damage. It may be
	permanent. Time'll tell, and only after you are off Substance D for a
	long while. And off entirely."

	"What?" Fred said. He did not understand the answer-- was it yes or no?
	Was he damaged forever or not? Which had they said?

      -- Phillip K. Dick, A Scanner Darkly


Substance D is an application development environment that provides the
following features:

- Facilities that allow developers to define "content" (e.g. "a blog
  entry", "a product", or "a news item", etc).

- A management (aka "admin") web UI which allows nonexpert but privileged
  users to create, edit, update, and delete developer-defined content.

- "Undo" capability for actions taken via the management UI.

- A way to make highly granular hierarchical security declarations for
  content objects (e.g. "Bob can edit *this* post" or "Bob can edit all posts
  in this collection" as opposed to just "Bob can edit posts").

- Built-in users and groups management.

- Indexing and searching of content (field, keyword, facet, and full-text).

- A facility for relating content objects to each other.

- An "evolve" mechanism for evolving content over time as it changes.

Substance D is built upon on the following technologies:

- `ZODB <http://zodb.org>`_ .

- `Pyramid <http://pylonsproject.org>`_.

- `repoze.catalog <http://docs.repoze.org/catalog>`_

- `repoze.evolution <http://docs.repoze.org/evolution>`_

- `colander <http://docs.pylonsproject.org/projects/colander/en/latest/>`_

- `deform <http://docs.pylonsproject.org/projects/deform/en/latest/>`_

The Management Interface
------------------------

The Substance D management interface (aka :term:`SDI`) is a set of
:term:`view` registrations that are imposed upon the resource tree.  The SDI
allows you to add, delete, change and otherwise manage resources.

The SDI is extensible and allows you to plug your own views into it, so you
can present nontechnical users with a way to manage arbitrary kinds of
content.

