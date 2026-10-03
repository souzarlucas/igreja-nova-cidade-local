# Segurança da edição local

O computador da mídia mantém o SQLite fora da pasta do programa, em LOCALAPPDATA. Contas são criadas pelo administrador principal; sessão opaca com cookie HttpOnly/SameSite=Strict, hash no banco e expiração de oito horas. HTTPS adiciona Secure. Limites de login, checagem de origem e hosts permitidos, validação de dados e permissões por ministério são mantidos. A edição financeira recusa eventos e cadastro individual de membros.

Nenhuma configuração ou banco real acompanha o pacote. Apenas administradores autorizados acessam tudo; Tesouraria/Presbitério dependem de autorização individual; Ministério/Membro ficam no próprio vínculo. Revogação encerra sessões. O sistema escuta em localhost até configurar a rede local.

O modo LAN HTTP não fornece criptografia de transporte. Ative HTTPS com certificado confiável para proteger o tráfego e não exponha a porta à internet. Restrinja o firewall à rede privada local. Proteja a conta Windows, bloqueio de tela e disco, pois alguém com acesso aos arquivos locais pode ler o banco ou modificar o programa.

O backup usa snapshot SQLite, AES-256-GCM, salt/nonce aleatórios e chave derivada da senha com PBKDF2-SHA256 600.000 iterações. Arquivos temporários ficam fora do Drive e são apagados depois da cópia. Senhas não são persistidas pelo programa. A rotina de restauração verifica integridade e nunca sobrescreve o banco existente. Upload requer a configuração do cliente Drive pelo responsável. Não publique dados, arquivos .ncb, chaves, configuracao.json ou bancos no GitHub.
