import os
import json
import logging
import logging.config

# Config provides all the methods we need.
class Config(object):
    def __init__(self, base=None, root=None, files=None):
        '''
        Config objects' initialisation allow overriding of their attribute values depending on the
        arguments they are passed.

        Config values are set/overridden in the following order of precedence (step 4 having highest priority)
        1. Hardcoded / pre-set values in the Config object
        2. Read from additional config object passed in as the 'base' argument
        3. Read from files passed as the 'files' argument in the initialiser, eg. DevConfig(files=['settings_dev.cfg'])
        4. Read from the environment

        In step 2, the current config object absorbs ALL keys on the given 'base' Config object, and their
        corresponding values
        In steps 3-4, only values for keys that are ALREADY on the Config object are absorbed

        args
            name          Describe the argument

        kwargs
            kwarg         Describe the kwarg
        '''
        if base:
            self.update(base, absorb=True)

        # Load dev settings, if provided
        self.load_dev_settings(root=root, files=files)

        # Load from environment
        self.update(os.environ, absorb=False)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

    def __setitem__ (self, key, value):
        return setattr(self, key, value)

    def to_dict(self):
        return {k: getattr(self, k) for k in dir(self) if k.isupper()}

    def iteritems(self):
        return iter(self.to_dict().items())

    def get(self, key, default=None):
        return getattr(self, key, default)

    def update(self, target, absorb=False):
        '''
        Updates self with a dictionary, overwriting existing keys

        args
            target        Target dictionary to absorb values from
        '''
        for k, e in target.items():
            if k.isupper():
                if k not in self and not absorb:
                    continue

                if e is not None:
                    v = getattr(self, k, None)

                    if isinstance(v, bool):
                        setattr(self, k, bool(int(e)))
                    elif isinstance(v, int):
                        setattr(self, k, int(e))
                    else:
                        setattr(self, k, e)
        return self

    # no choice but to take this out.
    # can't get the path of the individual "settings_dev" of individual app from here.
    def load_dev_settings(self, root=None, files=None):
        '''
        Updates self with values from a settings file, usually named settings_dev.cfg

        args
            root          Filesystem path of settings module calling this method

        kwargs
            files         List of settings files to update from
        '''
        root = root or os.path.dirname(os.path.abspath(__file__))
        files = files or []
        settings_dev = {}
        for f in files :
            try:
                cfg = '/'.join([root, f])
                exec(compile(open(cfg).read(), cfg, 'exec'), {}, settings_dev)
                self.update(settings_dev)
            except IOError as e : #file don't exist, proceed as normal
                pass
