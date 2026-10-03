import webbrowser
import uvicorn
from backend.local_config import load_config

def main():
    root, config = load_config()
    port = int(config['port'])
    print('Nova Cidade · Financeiro local')
    print('Dados locais:',root)
    print('Código do primeiro cadastro: consulte configuracao.json nesta pasta. Não compartilhe.')
    url = f"{'https' if config.get('ssl_certfile') else 'http'}://127.0.0.1:{port}"
    print('Acesso neste computador:',url)
    if config['host'] == '0.0.0.0':
        print('Rede local habilitada. Use o IP configurado em allowed_hosts e a mesma porta.')
    uvicorn.run('backend.local:app', host=config['host'],port=port,proxy_headers=False,access_log=False,ssl_certfile=config.get('ssl_certfile') or None,ssl_keyfile=config.get('ssl_keyfile') or None)
if __name__ == '__main__': main()
