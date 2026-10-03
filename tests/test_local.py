import sqlite3
import pytest
from cryptography.exceptions import InvalidTag
from backend.backup import create_backup, restore_backup
from backend.local_config import load_config

def test_encrypted_backup_restores_live_wal_and_rejects_wrong_password(tmp_path):
    database=tmp_path/'church.sqlite'
    connection=sqlite3.connect(database)
    connection.execute('PRAGMA journal_mode=WAL')
    connection.execute('CREATE TABLE private_data(value TEXT)')
    connection.execute('INSERT INTO private_data VALUES(?)',('Confidential financial records',))
    connection.commit()
    backup=create_backup(database,tmp_path/'drive','Strong-backup-password')
    assert b'Confidential financial records' not in backup.read_bytes()
    target=tmp_path/'recovered.sqlite'
    with pytest.raises(InvalidTag): restore_backup(backup,target,'Wrong-backup-password')
    assert not target.exists()
    restore_backup(backup,target,'Strong-backup-password')
    with sqlite3.connect(target) as restored:
        assert restored.execute('SELECT value FROM private_data').fetchone()[0]=='Confidential financial records'
    with pytest.raises(ValueError): restore_backup(backup,target,'Strong-backup-password')
    assert connection.execute('SELECT count(*) FROM private_data').fetchone()[0]==1
    connection.close()

def test_configuration_defaults_to_localhost_and_keeps_setup_token(tmp_path,monkeypatch):
    monkeypatch.setenv('CHURCH_DATA_DIR',str(tmp_path))
    root,first=load_config();_,second=load_config()
    assert root==tmp_path
    assert first['host']=='127.0.0.1'
    assert first['allowed_hosts']==['localhost','127.0.0.1']
    assert first['setup_token']==second['setup_token'] and len(first['setup_token'])>=32
