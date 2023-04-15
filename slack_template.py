from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SlackTemplate:
	"""
	Example attachment:
	{
		"color": "#000000",
		"blocks": [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Manual AWS Change Detected:\n*<mailto:user@domain.com|user@domain.com>*"
				}
			},
			{
				"type": "section",
				"fields": [
					{
						"type": "mrkdwn",
						"text": "*Event name:*\nCreateToken"
					},
					{
						"type": "mrkdwn",
						"text": "*Event source:*\nsso.amazonaws.com"
					},
					{
						"type": "mrkdwn",
						"text": "*Event ID:*\n54e00bbd-50cd-0b6c-9b2e-000000e2e156"
					},
					{
						"type": "mrkdwn",
						"text": "*When:*\nThu Jan 28 12:32:01"
					},
					{
						"type": "mrkdwn",
						"text": "*Error:*\nAccess deny."
					}
				]
			}
		]
	}
	"""
	email: str
	user_identity: str
	event_name: str
	event_source: str
	event_id: str
	event_time: str
	error: str
	# result: dict = field(init=False)
	color: str = field(init=False)

	def __post_init__(self) -> None:
		self.color = '#FF0000' if self.error else '#00FF00'

	@staticmethod
	def new_field(header, text) -> dict:
		return {
			'type': 'mrkdwn',
			'text': f"*{header}:*\n{text}"
		}

	def get_human_event_time(self) -> str:
		dt_obj = datetime.strptime(self.event_time, "%Y-%m-%dT%H:%M:%SZ")
		return str(dt_obj.strftime("%a %b %e %H:%M:%S"))

	def render_attachment(self):

		fields = [
			self.new_field('Event name', f":rain_cloud: {self.event_name}"),
			self.new_field('Event source', self.event_source),
			self.new_field('Event ID', self.event_id),
			self.new_field('When', self.get_human_event_time()),
		]

		if self.error:
			fields.append(self.new_field('Error', f":red_circle: {self.error}"))

		blocks = [
			{
				'type': 'section',
				'text': {
					'type': 'mrkdwn',
					'text': f"*Violator:*\n{self.user_identity}",
				},
			},
			{
				'type': 'section',
				'fields': fields,
			}
		]

		skel = {
			"color": self.color,
			"blocks": blocks
		}

		return skel
