import os

if os.environ.get('BASE') == 'True':
    from .base import *
elif os.environ.get('LOCAL') == 'True':
    from .local import *
