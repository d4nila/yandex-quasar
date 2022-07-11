from datetime import datetime
from itertools import chain

def convert_datetime(string):
	return datetime.strptime(
		string, 
		'%Y-%m-%dT%H:%M:%SZ'
	) if string else None

def get_room_id(resp, room_name):
	rooms = list(chain(*[i['rooms'] for i in resp['households']])) 
	for room in rooms:
		if room['name'] == room_name:
			return room['id']

def get_key(obj, keys):
	for key in keys:
		if key not in obj:
			return None
		obj = obj[key]
	return obj