import os
from starlette.middleware.trustedhost import TrustedHostMiddleware
from .local_config import load_config
from .database import LocalDatabase
from .app import create_app
root, config = load_config()
os.environ['SETUP_TOKEN'] = config['setup_token']
os.environ['LOCAL_FINANCE_ONLY'] = '1'
os.environ.pop('APP_ORIGIN', None)
database = LocalDatabase(root / 'igreja.sqlite')
database.migrate()
app = create_app(database)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=config['allowed_hosts'])
