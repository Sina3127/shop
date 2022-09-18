import os

from settings.common import *

if os.environ.get("MOD", "DEBUG") == "DEBUG":
    from settings.develop import *
else:
    from settings.production import *