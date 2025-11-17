.. automodule:: {{ fullname }}
   :no-members:
   :undoc-members:
   :show-inheritance:

{{ doc }}

{{ fullname | escape | underline }}

{% if modules %}
Subpackages
==========

.. autosummary::
   :nosignatures:
   :toctree: .
{% for m in modules %}
   {{ fullname }}.{{ m }}
{% endfor %}
{% endif %}

{% if functions %}
Functions
==========

.. autosummary::
   :nosignatures:
{% for f in functions %}
   {{ fullname }}.{{ f }}
{% endfor %}
{% endif %}

{% if classes %}
Classes
==========

.. autosummary::
   :nosignatures:
{% for c in classes %}
   {{ fullname }}.{{ c }}
{% endfor %}
{% endif %}

{% if attributes %}
Attributes
==========

.. autosummary::
   :nosignatures:
{% for a in attributes %}
   {{ fullname }}.{{ a }}
{% endfor %}
{% endif %}

{# -- Start Detail Blocks -- #}

{% if functions %}

Function Details
-------
{% for f in functions %}
.. _{{ fullname }}.{{ f }}:

.. autofunction:: {{ fullname }}.{{ f }}

{% endfor %}
{% endif %}

{% if classes %}

Class Details
-------
{% for c in classes %}
.. _{{ fullname }}.{{ c }}:

.. autoclass:: {{ fullname }}.{{ c }}
   :members:
   :undoc-members:
   :show-inheritance:

{% endfor %}
{% endif %}

{% if attributes %}

Attribute Details
-------
{% for a in attributes %}
.. _{{ fullname }}.{{ a }}:

.. autoattribute:: {{ fullname }}.{{ a }}

{% endfor %}
{% endif %}
