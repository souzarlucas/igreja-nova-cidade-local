import os, secrets, sqlite3, tempfile, hashlib
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
MAGIC = b'NCB1'

def key(password, salt):
    if len(password) < 12: raise ValueError('A senha de backup deve ter pelo menos 12 caracteres.')
    return hashlib.pbkdf2_hmac('sha256',password.encode(),salt,600_000,32)

def create_backup(database, folder, password):
    database, folder = Path(database), Path(folder)
    if not database.is_file(): raise ValueError('Banco não encontrado. Inicie o sistema primeiro.')
    folder.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='nova-cidade-',dir=database.parent) as temporary:
        snapshot = Path(temporary)/'snapshot.sqlite'
        source=sqlite3.connect(f'{database.resolve().as_uri()}?mode=ro',uri=True)
        destination=sqlite3.connect(snapshot)
        try: source.backup(destination)
        finally: destination.close();source.close()
        if snapshot.stat().st_size > 256*1024*1024: raise ValueError('Banco maior que o limite desta rotina de backup (256 MB).')
        salt,nonce=secrets.token_bytes(16),secrets.token_bytes(12)
        header=MAGIC+salt+nonce
        content=header+AESGCM(key(password,salt)).encrypt(nonce,snapshot.read_bytes(),header)
    from datetime import datetime,timezone
    target=folder/f"nova-cidade-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(3)}.ncb"
    descriptor=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(descriptor,'wb') as file: file.write(content)
    return target

def restore_backup(backup, target, password):
    content=Path(backup).read_bytes()
    if len(content)<48 or content[:4]!=MAGIC: raise ValueError('Formato de backup inválido.')
    target=Path(target)
    if target.exists(): raise ValueError('A restauração não pode sobrescrever um arquivo existente.')
    header=content[:32]
    plain=AESGCM(key(password,content[4:20])).decrypt(content[20:32],content[32:],header)
    if not plain.startswith(b'SQLite format 3\0'): raise ValueError('Banco inválido.')
    target.parent.mkdir(parents=True,exist_ok=True)
    descriptor=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    try:
        with os.fdopen(descriptor,'wb') as file: file.write(plain)
        with sqlite3.connect(target) as db:
            if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok': raise ValueError('Integridade do banco inválida.')
    except Exception:
        target.unlink(missing_ok=True);raise
    return target
