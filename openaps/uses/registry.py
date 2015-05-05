
class Registry (object):
  def __init__ (self):
    self.__USES__ = { }

  def __call__ (self):
    def decorator (cls):
      if cls.__name__ not in self.__USES__:
        self.__USES__[cls.__name__] = cls
      return cls
    return decorator

