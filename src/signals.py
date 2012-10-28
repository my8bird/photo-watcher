class Signal(object):
   def __init__(self):
      self._handlers = []

   def on(self, handler, *args, **kwds):
      self._handlers.append((handler, (args, kwds)))

   def off(self, handler, *args, **kwds):
      self._handlers.remove(handler, (args, kwds))

   def emit(self, *args, **kwds):
      # Find handlers to apply
      handlers = [h for h, config in self._handlers if self._shouldApply(config, args, kwds)]

      # Call each handler
      return [h(*args, **kwds) for h in handlers]

   def _shouldApply(self, (hArgs, hKwds), emitArgs, emitKwds):
      if len(hArgs) > len(emitArgs):
         # The signal has less arguments then the handler so they can not match
         return False

      for i, arg in enumerate(hArgs):
         if arg != emitArgs[i]:
            # A positional argument did not match
            return False

      for key, value in hKwds.viewitems():
         # If signal does not have a required key or the values do not match
         if not emitKwds.has_key(key) or value != emitKwds[key]:
            return False

      return True
