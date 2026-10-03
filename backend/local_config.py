import json, os, secrets, ipaddress
from pathlib import Path

def data_directory():
    configured = os.getenv('CHURCH_DATA_DIR')
    if configured:
        return Path(configured).expanduser().resolve()
    base = Path(os.getenv('LOCALAPPDATA', Path.home() / '.local' / 'share'))
    return base / 'NovaCidadeFinanceiro'

def load_config():
    root = data_directory()
    root.mkdir(parents=True, exist_ok=True)
    path = root / 'configuracao.json'
    if not path.exists():
        config = {'setup_token': secrets.token_urlsafe(32), 'host': '127.0.0.1', 'port': 8787, 'allowed_hosts': ['localhost','127.0.0.1'], 'backup_folder': '', 'ssl_certfile': '', 'ssl_keyfile': ''}
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor,'w',encoding='utf-8') as file:
            json.dump(config,file,indent=2)
    with path.open(encoding='utf-8') as file:
        return root, json.load(file)
