import os

if os.environ.get('BASE') == 'True':
    from .base import *
elif os.environ.get('LOCAL') == 'True':
    from .local import *
elif os.environ.get('PRODUCTION') == 'True':
    from .production import *
