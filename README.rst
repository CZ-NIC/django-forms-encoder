======================
 django-forms-encoder
======================

Encode django forms to JSON.

Encoded forms follow the structure described in `schema.json <schema.json>`_.

-----
Usage
-----

You can use ``DjangoFormsEncoder`` directly with ``json`` module from the standard library.

.. code-block:: python

   import json
   from django_forms_encoder import DjangoFormsEncoder

   json.dumps(form, cls=DjangoFormsEncoder)

You can also use filter ``encode_form`` in your templates if you add ``django_forms_encoder`` to ``INSTALLED_APPS``.
This filter will convert the Django form to simple Python structure, that can be easily converted to JSON.
You'll probably want to use it together with ``json_script`` filter from Django.

.. code-block:: html

   {% load django_forms_encoder %}

   {{ form|encode_form|json_script:'login-form' }}
