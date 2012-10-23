# Install
## Requires
 * watchdog
 * twisted

Suggested setup using to virtualenv
```sh
# Get the code
git clone git@github.com:my8bird/photo-watcher.git
cd photo-watcher

# Install virtualenv if you don't have it
pip install virtualenv
# Create a virtual workspace for the python dependencies
virtualenv .

# Install the dependencies
pip install watchdog twisted boto
```
