from twisted.internet       import reactor
from twisted.internet.defer import inlineCallbacks

from watchdog.observers import Observer
from watchdog.events    import FileSystemEventHandler


from signals import Signal


class FSEventWatcher(FileSystemEventHandler):
   def __init__(self):
      self.created  = Signal()
      self.deleted  = Signal()
      self.modified = Signal()
      self.moved    = Signal()

   def on_created(self, event):
      self.created.emit(event.src_path,
                        isdir  = event.is_directory,
                        isfile = not event.is_directory)

   def on_deleted(self, event):
      self.deleted.emit(event.src_path,
                        isdir  = event.is_directory,
                        isfile = not event.is_directory)

   def on_modified(self, event):
       self.modified.emit(event.src_path,
                          isdir  = event.is_directory,
                          isfile = not event.is_directory)

  def on_moved(self, event):
     self.moved.emit(event.src_path,
                     isdir  = event.is_directory,
                     isfile = not event.is_directory)


def watch(path):
   handler = FSEventWatcher()
   observer = Observer()
   observer.schedule(handler, path = path, recursive=True)
   observer.start()
   return handler
