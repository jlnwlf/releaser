Hello {{ mail }},

Heads up ! **{{ app.name }}** version **{{ version.numeral }}** will be released **{{ deployment.start|humanize }}**:

{% block details_table %}
<table>
  <tr><th>Start time</th><td>{{ deployment.start }}</td></tr>
  <tr><th>End time</th><td>{{ deployment.end }}</td></tr>
  <tr><th>Reason</th><td>{{ deployment.reason }}</td></tr>
  <tr><th>Expected Impact</th><td>{{ deployment.impact }}</td></tr>
  <tr><th>Rollback</th><td>{{ deployment.rollback }}</td></tr>
</table>
{% endblock %}

{% block changelist %}
Here are the changes introduced with that version:

{{ version.markdown_change_list }}
{% endblock %}

{% block postscriptum %}
The preproduction server is already running version {{ version.numeral }}, so please check for changes related to your business.
{% endblock %}
