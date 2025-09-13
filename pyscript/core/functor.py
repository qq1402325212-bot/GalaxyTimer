# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/4/28
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import types
import weakref


# python 实现一个CFunctor类，能包装一个函数，避免引用计数
class CFunctor:
	def __init__(self, func, *args, **kwargs):
		if not callable(func):
			return None
		self._IsMethodFunc = True
		self._IsBuiltinFunc = False
		
		if isinstance(func, types.MethodType):
			self._obj = weakref.ref(func.__self__)
			self._func = func.__func__
			self._name = func.__name__
		elif isinstance(func, types.BuiltinMethodType) and func.__self__:
			self._obj = weakref.ref(func.__self__)
			self._name = func.__name__
			self._func = func.__name__
			
			self._IsBuiltinFunc = True
		else:
			self._obj = None
			self._func = func
			self._name = ""
			self._IsMethodFunc = False
		self._args = args
		self._kwargs = kwargs
	
	def IsAlive(self):
		if self._IsMethodFunc:
			return self._obj() is not None
		return True
	
	def RealFunc(self):
		if self._IsMethodFunc:
			if self._obj() is None:
				return None
			return getattr(self._obj(), self._name)
		return self._func
	
	def __eq__(self, other):
		if not isinstance(other, CFunctor):
			return False
		return self._func == other._func
	
	def __call__(self, *args, **kwargs):
		if self._args:
			args = self._args + args
		if self._kwargs:
			kwargs.update(self._kwargs)
		
		if not self._IsMethodFunc:
			return self._func(*args, **kwargs)
		
		realObj = self._obj()
		if not realObj:
			return
		if self._IsBuiltinFunc:
			func = getattr(realObj, self._name)
		else:
			func = self._func
			args = (realObj,) + args
		
		return func(*args, **kwargs)
