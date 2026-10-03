# Nova Cidade · Financeiro local para Windows

Este é o segundo projeto, independente da publicação anterior. A licença é MIT. O banco SQLite fica somente no computador da mídia, em `%LOCALAPPDATA%\NovaCidadeFinanceiro\igreja.sqlite`. Não há hospedagem externa, telemetria nem chamadas a serviços externos durante o uso.

Inclui cadastro básico dos ministérios, responsável e voluntários; contas com perfis e liberação financeira individual; receitas, despesas com justificativa e forma de execução, pedidos de recursos, orçamentos mensais/anuais, gráficos e análises. Eventos e cadastro individual de membros não fazem parte desta edição. Os nomes dos voluntários continuam no cadastro básico do ministério.

## Instalar

1. Instale Python 3.13 de 64 bits de https://www.python.org/downloads/ (instalador oficial). Se o computador não tem internet, leve o instalador em um pendrive.
2. Extraia TODO o pacote em `C:\NovaCidadeFinanceiro`. Não execute diretamente dentro do ZIP nem coloque esta pasta no Google Drive.
3. Execute `INSTALAR-WINDOWS.bat`. O pacote Windows inclui as dependências na pasta `wheelhouse`, para esta etapa funcionar sem internet. A interface já está compilada em `dist`, dispensando Node.js no computador da mídia.
4. Execute `INICIAR-WINDOWS.bat` e deixe a janela aberta. Acesse `http://127.0.0.1:8787` no navegador.
5. Abra `%LOCALAPPDATA%\NovaCidadeFinanceiro\configuracao.json`. Copie apenas o valor de `setup_token` para o primeiro cadastro. Escolha sua senha e e-mail no próprio sistema. O código não permite novo cadastro depois que a primeira conta existe.
6. Crie os ministérios, crie as contas autorizadas, vincule cada responsável e libere o financeiro individualmente. A conta principal é a única que concede acessos.

O funcionamento foi verificado no ambiente de desenvolvimento macOS, com dependências Windows preparadas. A execução real no computador Windows da igreja e o firewall precisam ser validados nesse computador. Não há conta de demonstração no pacote.

## Outros computadores da igreja

O computador da mídia executa o serviço local; os demais usam o navegador. Nenhum dado é armazenado em servidor externo. O computador da mídia deve estar ligado; se ele desligar, os demais não conseguem abrir o sistema.

1. Reserve no roteador um IP fixo para o computador da mídia; veja o IPv4 com `ipconfig`. Exemplo ilustrativo: `192.168.1.50`.
2. Pare o sistema. Em `configuracao.json`, altere `host` para `0.0.0.0` e acrescente o IP real em `allowed_hosts`, mantendo `localhost` e `127.0.0.1`. Não use `*`.
3. No Windows, classifique somente a rede confiável da igreja como Privada. No PowerShell como administrador, abra APENAS a porta local:

```powershell
New-NetFirewallRule -DisplayName "Nova Cidade Financeiro LAN" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8787 -Profile Private -RemoteAddress LocalSubnet
```

4. Inicie novamente. Nos outros computadores da mesma rede, acesse `http://IP-DA-MIDIA:8787` e entre com uma conta individual.
5. Não encaminhe esta porta no roteador e não ative túneis para internet. Esta edição foi solicitada SEM acesso fora da igreja.

O modo HTTP em rede local não cifra o tráfego. Para proteger senhas e sessões contra interceptação na própria rede, configure HTTPS local com um certificado confiável instalado nos computadores; preencha os caminhos `ssl_certfile` e `ssl_keyfile` em `configuracao.json`. A chave privada deve ficar somente no computador da mídia. Não ignore avisos de certificado. Alternativamente, uma VPN restrita à rede local pode cifrar o transporte. Até concluir essa configuração, o padrão escuta apenas neste computador (`127.0.0.1`); use a LAN apenas em uma rede restrita e confiável.

O sistema aceita certificados próprios da igreja; sua emissão/instalação precisa ser feita no Windows e não foi configurada remotamente aqui.

## Backup criptografado para Google Drive

1. Instale e conecte o aplicativo Google Drive para computador na conta da igreja.
2. Escolha uma pasta exclusiva de backups, não compartilhada com pessoas externas.
3. Execute `BACKUP-WINDOWS.bat`. Digite uma senha própria com no mínimo 12 caracteres e confirme. Escolha a pasta sincronizada do Drive como destino.
4. O arquivo `.ncb` é uma cópia consistente do banco, protegida por AES-256-GCM e senha derivada com PBKDF2-SHA256 (600.000 iterações). O banco aberto NÃO é sincronizado, e a senha não é salva nem enviada ao Drive.
5. Sem internet, o backup continua sendo criado localmente; o aplicativo Drive envia depois, quando houver conexão. Confira a confirmação de sincronização no próprio Drive.
6. Guarde a senha em local seguro separado do Drive. Sem ela, não é possível restaurar. Mantenha também uma cópia em pendrive protegido e teste a restauração periodicamente.

O backup é manual, e deve ser feito após os lançamentos ou ao fim do expediente. Não há tarefa agendada nem upload diretamente pela API do Google. A conexão da conta Drive precisa ser feita por você no Windows. Você pode definir `backup_folder` em `configuracao.json` para reutilizar a pasta.

## Testar restauração sem sobrescrever o banco

No terminal da pasta do sistema:

```powershell
.venv\Scripts\python.exe backup.py --restaurar "CAMINHO\backup.ncb" --destino "C:\NovaCidadeRecuperacao\igreja-recuperada.sqlite"
```

A rotina recusa sobrescrever qualquer arquivo existente e verifica a integridade. Ela não troca o banco em uso automaticamente. Para recuperação real: pare o sistema, preserve o banco atual e seus arquivos WAL/SHM, faça outro backup e só então substitua o conjunto do banco com orientação técnica. Não deixe dois computadores operando cópias independentes do banco.

## Atualizações e privacidade

Antes de atualizar, faça backup. Substitua apenas os arquivos do programa; o banco fica fora da pasta do código. Use contas Windows individuais, bloqueio de tela, permissões de pasta e criptografia de disco (BitLocker quando disponível). Não coloque o banco, o código de primeiro acesso, configurações, senhas ou backups no GitHub. A configuração do computador, rede, HTTPS e Drive não foi realizada por este pacote.
