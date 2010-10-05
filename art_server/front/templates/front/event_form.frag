<form method="post" class="event-form">
	<a class="close-link" href="." onclick="hideAddEventForm(); return false;">[x]</a>
	{{ new_event_form }}	
	<input type="submit" value="Schedule the Event" />
	<p style="margin-top: 40px;">Checking no days schedules the event to run every day.</p>
	<p>Similarly, checking no hours schedules the event to run every hour.</p>
	<p>Checking no minutes only schedules the event to run at the top of the hour.</p>
	{% csrf_token %}
</form>