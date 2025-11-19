
.. .. automodule:: {{ fullname }}
..    :no-members:
..    :show-inheritance:

.. {{ doc }}

.. {{ super }}


.. {{ fullname | escape | underline }}

.. automodule:: {{ fullname }}
   :no-members:
   :show-inheritance:

{{ fullname | escape | underline }}
===========

{{ super }}


{% if modules %}
Subpackages
===========

.. autosummary::
   :nosignatures:
   :toctree: .
{% for m in modules %}
   {{ fullname }}.{{ m }}
{% endfor %}
{% endif %}


{% if functions %}
Functions
=========

.. autosummary::
   :nosignatures:
{% for f in functions %}
   {{ fullname }}.{{ f }}
{% endfor %}
{% endif %}


{% if classes %}
Classes
=======

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
----------------
{% for f in functions %}
.. _{{ fullname }}.{{ f }}:

.. autofunction:: {{ fullname }}.{{ f }}

{% endfor %}
{% endif %}


{# ---------- CLASSES ---------- #}
{% block classes %}
{% if classes %}
.. rubric:: Classes

{% for item in classes %}
.. _{{ fullname }}.{{ item }}:

.. autoclass:: {{ fullname }}.{{ item }}
   :members:
   :member-order: bysource


{% endfor %}
{% endif %}
{% endblock %}


