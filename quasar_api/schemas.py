from datetime import datetime
from dataclasses import dataclass
from typing import Union, Optional

@dataclass
class Device:
	created: Union[datetime, None]
	id: str
	name: str
	room: Union[str, None]
	room_id: Union[str, None]
	type: Union[str, None]
	manufacturer: Union[str, None]
	model: Union[str, None]
	sw_version: Union[str, None]

@dataclass
class Extended:
	is_favorite: Union[bool, None]
	id: Union[str, None]
	name: str
	names: list
	room: Union[str, None]
	online: Union[None, bool]
	type: Union[str, None]
	external_id: Union[str, None]
	sensors: Union[list, None]
	skill_id: Union[str, None]
	capabilities: Union[list, None]
	groups: Union[list, None]
	wss_url: Union[str, None]

@dataclass
class CurrentColor:
	id: Union[str, None, int]
	name: Union[str, None, int]
	type: Union[str, None, int]
	color: Union[str, None, dict]

@dataclass
class Range:
	min: Union[int, None]
	max: Union[int, None]
	precision: Union[int, None]

@dataclass
class OnOffCapability:
	type: str
	instance: Union[None, bool, str]
	value: Union[None, bool, str]

@dataclass
class ColorCapability:
	type: str
	instance: Union[None, bool, str]
	value: Union[None, bool, str, dict, CurrentColor]
	palette: Union[None, list]

@dataclass
class RangeCapability:
	type: str
	instance: Union[None, bool, str]
	value: Union[None, bool, str, int]
	range: Union[None, Range]
	unit: Union[None, str]

@dataclass
class ShortLinked:
	name: Union[str, None]
	id: Union[str, None]

@dataclass
class CustomButton:
	name: Union[str, None]
	instance: Union[str, None]

@dataclass
class Sensor:
	last_updated: Union[datetime, None]
	instance: Union[str, None]
	name: Union[str, None]
	percent: Union[str, None, float, int]
	status: Union[str, None, float, int]
	value: Union[str, None, float, int]
	type: Union[str, None, float, int]
	unit: Union[str, None, float, int]

@dataclass
class Speaker:
	icon: str
	id: str
	name: str
	online: bool
	platform: str
	screen_capable: bool
	screen_present: bool