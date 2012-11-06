# -*- coding: utf-8 -*-

import xmlrpclib

class Application(object):
	def __init__(self):
		self.core = xmlrpclib.ServerProxy('http://core:8800', allow_none=True)

	def FindObject(self, object_type, **kwargs):
		req = {}

		for k in kwargs:
			if isinstance(kwargs[k], Object):
				req[k] = ('OBJECT_ID', kwargs[k].uuid)
			else:
				req[k] = ('VALUE', kwargs[k])

		return [Object(object_type, uuid, self.core) for uuid in self.core.FindObject(object_type, req)]

	def DeleteObject(self, obj):
		return self.core.DeleteObject(obj.object_type, obj.uuid)

	def NewObject(self, object_type):
		return Object(object_type, self.core.NewObject(object_type), self.core)

class Object(dict):
	def __init__(self, object_type, uuid, core):
		self.object_type = object_type
		self.uuid = uuid
		self.core = core

	def __repr__(self):
		return object.__repr__(self)

	def __getitem__(self, item):
		repl = self.core.GetObjectAttr(self.object_type, self.uuid, item)

		if not repl is None:
			t, v = repl
		else:
			raise KeyError

		if t == 'OBJECT_ID':
			print v
			object_type, uuid = v
			return Object(object_type, uuid, self.core)

		else:
			return v

	def __setitem__(self, item, value):
		if isinstance(value, Object):
			t, v = 'OBJECT_ID', value.uuid
		else:
			t, v = 'VALUE', value

		self.core.SetObjectAttr(self.object_type, self.uuid, item, (t, v))

	def __iter__(self):
		return iter(self.core.GetAttrList(self.object_type))

	def getattr(self, attr):
		if object.__hasattr__(self, attr):
			return object.__getattr__(self, attr)

		action_list = self.core.GetActionList(self.object_type)

		if not attr in action_list:
			raise AttributeError

		def action_wrapper(self, **kwargs):
			return self.Core.PerformAction(self.object_type, self.uuid, attr, kwargs)

		return action_wrapper

