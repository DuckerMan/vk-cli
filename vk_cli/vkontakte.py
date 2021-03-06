#!/usr/bin/env python3

import vk

class api(vk.API):
	"""ВКонтакте API.

	Обёртка над сторонней библиотекой, делает FieldDict из всех словарей,
	которые возвращает эта библиотека.
	"""

	def __call__(self, *args, **kwargs):
		return FieldDict.process_all(super().__call__(*args, **kwargs))


class FieldDict(dict):
	"""Словарь с полями."""

	def __init__(self, *args, **kwargs):
		"""Инициализирует словарь self и принимает его элементы как свои поля"""
		super().__init__(*args, **kwargs)
		self.__dict__ = self

	@classmethod
	def process_all(cls, response):
		"""Если response словарь, то превращает его в cls.

		Если response список или словарь, то рекурсивно превращает каждый его
		элемент в cls. Иначе возвращает response.
		"""
		if type(response) is dict:
			for key, elem in response.items():
				response[key] = cls.process_all(elem)
			return cls(response)
		if type(response) is list:
			for i, elem in enumerate(response):
				response[i] = cls.process_all(elem)
		return response
