{{ fullname | escape | underline }}

{{ doc }}

{% if modules %}
.. rubric:: Subpackages

.. autosummary::
   :nosignatures:
   :toctree: .
{% for m in modules %}
   {{ fullname }}.{{ m }}
{% endfor %}
{% endif %}

{% if functions %}
.. rubric:: Functions

.. autosummary::
   :nosignatures:
   :toctree: .
{% for f in functions %}
   {{ fullname }}.{{ f }}
{% endfor %}
{% endif %}

{% if classes %}
.. rubric:: Classes

.. autosummary::
   :nosignatures:
   :toctree: .
{% for c in classes %}
   {{ fullname }}.{{ c }}
{% endfor %}
{% endif %}

{% if attributes %}
.. rubric:: Attributes

.. autosummary::
   :nosignatures:
   :toctree: .
{% for a in attributes %}
   {{ fullname }}.{{ a }}
{% endfor %}
{% endif %}
