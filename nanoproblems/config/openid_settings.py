import os

if os.environ.get('PRODUCTION') == 'False':
    REALM_URL = 'http://localhost:8000/'
    RETURN_URL = 'http://localhost:8000/users/login'
else:
    REALM_URL = 'http://nanoproblems-dev.elasticbeanstalk.com/'
    RETURN_URL = 'http://nanoproblems-dev.elasticbeanstalk.com/login'
