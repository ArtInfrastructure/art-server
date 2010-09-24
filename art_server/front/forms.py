# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django import forms

DAY_CHOICES = (("0", "Monday"), ("1", "Tuesday"), ("2", "Wednesday"), ("3", "Thursday"), ("4", "Friday"), ("5", "Saturday"), ("6", "Sunday"))
HOUR_CHOICES = list([(str(i), str(i)) for i in range(0,24)])
MINUTE_CHOICES = list([(str(i), str(i)) for i in range(0,60,15)])

class BaseEventForm(forms.ModelForm):
	"""A form used as the base for iBoot and Projector event forms"""

	days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DAY_CHOICES, required=False)
	hours = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=HOUR_CHOICES, required=False)
	minutes = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=MINUTE_CHOICES, required=False)
	
	def clean_days(self):
		if not self.cleaned_data.has_key('days'): return ''
		return ','.join(self.cleaned_data['days'])

	def clean_hours(self):
		if not self.cleaned_data.has_key('hours'): return ''
		return ','.join(self.cleaned_data['hours'])

	def clean_minutes(self):
		if not self.cleaned_data.has_key('minutes'): return ''
		return ','.join(self.cleaned_data['minutes'])
