{% extends "base.html" %}

{% block content %}

<h1>Lista kategorii</h1>

{% if categories %}
    <ul class="list-group">
        {% for category in categories %}
            <li class="list-group-item">{{ category.name }}</li>
        {% endfor %}
    </ul>
{% else %}
    <p>Brak kategorii do wyświetlenia.</p>
{% endif %}

{% endblock %} 