import argparse, getpass
from pathlib import Path
from backend.local_config import load_config
from backend.backup import create_backup, restore_backup

def main():
    parser=argparse.ArgumentParser(description='Backup criptografado do financeiro local')
    parser.add_argument('--restaurar');parser.add_argument('--destino');args=parser.parse_args()
    root,config=load_config()
    password=getpass.getpass('Senha do backup (mínimo 12 caracteres): ')
    if args.restaurar:
        if not args.destino: parser.error('Use --destino com um novo arquivo; pare o sistema antes de trocar o banco ativo.')
        target=restore_backup(args.restaurar,args.destino,password)
    else:
        if password != getpass.getpass('Confirme a senha do backup: '): raise ValueError('As senhas não coincidem.')
        folder=args.destino or config.get('backup_folder') or input('Pasta de backups (pode ser uma pasta sincronizada do Google Drive): ').strip()
        if not folder: raise ValueError('Informe a pasta de backup.')
        target=create_backup(root/'igreja.sqlite',folder,password)
    print('Arquivo criado:',target)
    print('O envio ao Drive depende do aplicativo Drive, da conta conectada e de internet. A senha não é enviada ao Drive.')
if __name__=='__main__':
    try: main()
    except Exception as error:
        print('Não foi possível concluir o backup/restauração:',str(error) or 'senha incorreta ou arquivo alterado.');raise SystemExit(1)
