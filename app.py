# Setup paths to work for us
import sys
sys.path.insert(0, 'src')

from watcher import watch

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
   from twisted.internet import reactor
   main()
   reactor.run()
