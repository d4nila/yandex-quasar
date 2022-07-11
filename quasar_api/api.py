from .schemas import *
from .utils import *
from .errors import *
from pathlib import Path
from itertools import chain
from dacite import from_dict
import json
import httpx

class Quasar:
	def __init__(self, cookies):
		if Path(cookies + '.txt').is_file():
			self.cookies = open(cookies + '.txt', 'r').read()
		else:
			self.cookies = cookies

		self.client = httpx.Client()

		host = 'passport.yandex.ru'
		if len(self.cookies) > 0 and self.cookies[0] == '[':
			try:
				raw = json.loads(self.cookies)
				host = next(
					p['domain'] for p in raw
					if p['domain'].startswith('passport.yandex.')
				)
				cookies = '; '.join([f"{p['name']}={p['value']}" for p in raw])
			except:
				raise InvalidCookiesError(f'Invalid cookies')
		else:
			raise InvalidCookiesError(f'Invalid cookies')

		r = self.client.post(
			'https://mobileproxy.passport.yandex.net/1/bundle/oauth/token_by_sessionid',
			data = {
				'client_id': 'c0ebe342af7d48fbbbfcf2d2eedb8f9e',
				'client_secret': 'ad0a908f0aa341a182a37ecd75bc319e',
			}, 
			headers = {
				'Ya-Client-Host': host,
				'Ya-Client-Cookie': cookies
			}
		)
		if 'access_token' not in r.text:
			raise InvalidCookiesError(f'Invalid cookies')

		self.access_token = r.json()['access_token']

		r = self.client.get(
			'https://mobileproxy.passport.yandex.net/1/bundle/account/short_info/?avatar_size=islands-300',
			headers = {'Authorization': f'OAuth {self.access_token}'}
		).json()
		self.account = r

		if 'errors' in r:
			raise InvalidCookiesError(f'Invalid cookies')

		payload = {
			'type': 'x-token',
			'retpath': 'https://www.yandex.ru'
		}
		headers = {'Ya-Consumer-Authorization': f'OAuth {self.access_token}'}
		r = self.client.post(
			'https://mobileproxy.passport.yandex.net/1/bundle/auth/x_token/',
			data = payload, 
			headers = headers
		)
		resp = r.json()

		if resp['status'] != 'ok':
			raise error.YandexError(str(resp))

		host = resp['passport_host']
		payload = {'track_id': resp['track_id']}
		r = self.client.get(
			f'{host}/auth/session/', params = payload
		)
		
		if not r.text:
			raise YandexError('Can\'t login to account')

	def get_devices(self):
		resp = self.client.get(
			'https://iot.quasar.yandex.ru/m/v3/user/devices'
		)

		if '"status":"ok"' not in resp.text:
			raise YandexError(f'Can\'t fetch devices: {resp.text}')

		resp = resp.json()
		devices = list(chain(*[i['all'] for i in resp['households']]))
		return [from_dict(data_class = Device, data = {
				'created': convert_datetime(
					get_key(device, ['created'])
				),
				'id': get_key(device, ['id']),
				'name': get_key(device, ['name']),
				'room': get_key(device, ['room_name']),
				'room_id': get_room_id(
					resp, get_key(device, ['room_name'])
				),
				'type': get_key(device, ['type']),
				'manufacturer': get_key(device, 
					['parameters', 'device_info', 'manufacturer']
				),
				'model': get_key(device, 
					['parameters', 'device_info', 'model']
				),
				'sw_version': get_key(device, 
					['parameters', 'device_info', 'sw_version']
				)
			}) for device in devices]

	def get_device(self, uid):
		resp = self.client.get(
			f'https://iot.quasar.yandex.ru/m/user/devices/{uid}'
		)

		if '"status":"ok"' not in resp.text:
			raise YandexError(f'Can\'t fetch device: {resp.text}')

		resp = resp.json()
		cs = from_dict(data_class = Extended, data = {
			'is_favorite': get_key(resp, ['favorite']),
			'id': get_key(resp, ['id']),
			'name': get_key(resp, ['name']),
			'names': get_key(resp, ['names']),
			'room': get_key(resp, ['room']),
			'online': True if get_key(resp, ['state']) == 'online' \
				else False,
			'type': get_key(resp, ['type']),
			'external_id': get_key(resp, ['external_id']),
			'sensors': [],
			'skill_id': get_key(resp, ['skill_id']),
			'capabilities': [],
			'groups': get_key(resp, ['groups']),
			'wss_url': get_key(resp, ['updates_url'])
		})

		for cpb in resp['capabilities']:
			if cpb['type'] == 'devices.capabilities.on_off' \
				and 'media_device.tv' not in cs.type:
				cs.capabilities.append(from_dict(
					data_class = OnOffCapability,
					data = {
						'type': cpb['type'],
						'instance': get_key(cpb, ['state', 'instance']),
						'value': get_key(cpb, ['state', 'value'])
					}
				))
				cs.turn_on = lambda: self._change_state(
					uid,
					'devices.capabilities.on_off',
					'on',
					True
				)
				cs.turn_off = lambda: self._change_state(
					uid,
					'devices.capabilities.on_off',
					'on',
					False
				)

			elif cpb['type'] == 'devices.capabilities.color_setting':
				cs.capabilities.append(from_dict(
					data_class = ColorCapability,
					data = {
						'type': cpb['type'],
						'instance': get_key(cpb, ['state', 'instance']),
						'value': from_dict(data_class = CurrentColor, data = {
							'id': get_key(cpb, ['state', 'value', 'id']),
							'name': get_key(cpb, ['state', 'value', 'name']),
							'type': get_key(cpb, ['state', 'value', 'type']),
							'color': get_key(cpb, ['state', 'value', 'value'])
						}),
						'palette': get_key(cpb, ['parameters', 'palette'])
					}
				))
				cs.set_color = lambda color: self._change_state(
					uid,
					'devices.capabilities.color_setting',
					'color',
					color
				)

			elif cpb['type'] == 'devices.capabilities.range' \
				and 'media_device.tv' not in cs.type:
				cs.capabilities.append(from_dict(
					data_class = RangeCapability,
					data = {
						'type': cpb['type'],
						'instance': get_key(cpb, ['state', 'instance']),
						'value': get_key(cpb, ['state', 'value']),
						'range': from_dict(data_class = Range, data = {
							'min': get_key(cpb, ['parameters', 'range', 'min']),
							'max': get_key(cpb, ['parameters', 'range', 'max']),
							'precision': get_key(cpb, ['parameters', 'range', 'precision'])
						}),
						'unit': get_key(cpb, ['parameters', 'unit'])
					}
				))
				cs.set_brightness = lambda br: self._change_state(
					uid,
					'devices.capabilities.range',
					'brightness',
					int(br)
				)

			elif cpb['type'] == 'devices.capabilities.custom.button':
				cs.capabilities.append(from_dict(
					data_class = CustomButton,
					data = {
						'name': get_key(cpb, ['parameters', 'name']),
						'instance': get_key(cpb, ['parameters', 'instance'])
					}
				))
				cs.use_custom = lambda name: self._change_state(
					uid,
					'devices.capabilities.custom.button',
					str(name),
					True
				)

		if cs.type == 'devices.types.media_device.tv':
			cs.channel_up = lambda: self._change_state(
				uid,
				'devices.capabilities.range',
				'channel',
				1,
				True
			)
			cs.channel_down = lambda: self._change_state(
				uid,
				'devices.capabilities.range',
				'channel',
				-1,
				True
			)
			cs.volume_up = lambda: self._change_state(
				uid,
				'devices.capabilities.range',
				'volume',
				1,
				True
			)
			cs.volume_down = lambda: self._change_state(
				uid,
				'devices.capabilities.range',
				'volume',
				-1,
				True
			)
			cs.set_channel = lambda channel: self._change_state(
				uid,
				'devices.capabilities.range',
				'channel',
				int(channel)
			)
			cs.mute = lambda: self._change_state(
				uid,
				'devices.capabilities.toggle',
				'mute',
				True
			)
			cs.power = lambda: self._change_state(
				uid,
				'devices.capabilities.on_off',
				'on',
				True
			)

		for sens in resp['properties']:
			cs.sensors.append(from_dict(
				data_class = Sensor,
				data = {
					'last_updated': convert_datetime(
						get_key(sens, ['last_updated'])
					),
					'instance': get_key(sens, ['parameters', 'instance']),
					'name': get_key(sens, ['parameters', 'name']),
					'percent': get_key(sens, ['state', 'percent']),
					'status': get_key(sens, ['state', 'status']),
					'value': get_key(sens, ['state', 'value']),
					'type': get_key(sens, ['type']),
					'unit': get_key(sens, ['parameters', 'unit'])
				}
			))

		if cs.type == 'devices.types.hub':
			cs.get_linked = lambda: self._hub_linked(cs.id)

		return cs

	def get_smart_speakers(self):
		r = self.client.get(
			'https://quasar.yandex.ru/devices_online_stats'
		)

		if '"status":"ok"' not in r.text:
			raise YandexError(f'Can\'t fetch smart speakers: {r.text}')

		r = r.json()

		return [from_dict(
			data_class = Speaker,
			data = a
		) for a in r['items']]

	def _change_state(self, uid, typ, instance, value, relative = False):
		data = {
			'actions': [{
				'type': typ,
				'state': {
					'instance': instance,
					'value': value
				}
			}]
		}

		if relative:
			data['actions'][0]['state']['relative'] = True

		resp = self.client.post(
			f'https://iot.quasar.yandex.ru/m/user/devices/{uid}/actions',
			headers = {
				'x-csrf-token': self._get_csrf()
			},
			json = data
		)
		return True if '"status":"ok"' in resp.text else False

	def play_youtube_video(self, iud, url):
		data = {
			'msg': {
				'provider_item_id': url
			},
			'device': iud
		}

		data['msg']['player_id'] = 'youtube'

		r = self.client.post(
			'https://yandex.ru/video/station', 
			data = json.dumps(data), 
			headers = {'x-csrf-token': self._get_front_csrf()}
		)
		
		return True if '"msg":"success"' in r.text else None

	def _hub_linked(self, uid):
		r = self.client.get(
			f'https://iot.quasar.yandex.ru/m/user/devices/{uid}/controls'
		)

		if '"status":"ok"' not in r.text:
			raise YandexError(f'Can\'t fetch linked devices: {r.text}')

		r = r.json()

		return [from_dict(data_class = ShortLinked, data = {
			'id': a['id'],
			'name': a['name']
		}) for a in r['devices']]

	def _get_csrf(self):
		return self.client.get(
			'https://yandex.ru/quasar?storage=1'
		).json()['storage']['csrfToken2']

	def _get_front_csrf(self):
		return self.client.get(
			'https://frontend.vh.yandex.ru/csrf_token'
		).text