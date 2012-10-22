from twisted.internet       import reactor
from twisted.internet.defer import inlineCallbacks

from watchdog.observers import Observer
from watchdog.events    import FileSystemEventHandler



class Signal:
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


def main():
    h = watch('.')
    def printer(path, isdir=False, isfile=False):
        print path
    def printerdir(path, isdir=False, isfile=False):
        print 'dir', path

    h.created.on(printer)
    h.deleted.on(printer)
    h.modified.on(printer)
    h.moved.on(printer)

    h.created.on(printerdir, isdir=True)
    h.deleted.on(printerdir, isdir=True)
    h.modified.on(printerdir, isdir = True)
    h.moved.on(printerdir, isdir=True)


if __name__ == '__main__':
    main()
    reactor.run()
