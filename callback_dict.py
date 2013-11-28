class CallbackDict(object):
  def __init__(self):
    self.callback_dict = {}

  def add_callback(self, name, cb):
    cbs = self.callback_dict.get(name) or []
    cbs.append (cb)
    self.callback_dict [name] = cbs

  def call_callbacks(self, name, *args):
    for cb in (self.callback_dict.get(name) or []):
      ret = cb (*args)
      if ret: return ret
