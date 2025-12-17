# 🚀 Deploy no Streamlit Cloud

## Passo a Passo para Deploy

### 1. Acesse o Streamlit Cloud
- Vá em: https://share.streamlit.io/
- Faça login com sua conta GitHub

### 2. Novo App
- Clique em "New app"
- Selecione o repositório: `hytalofernando/dashboard-sql`
- Branch: `master`
- Main file path: `main.py`

### 3. Configurações Opcionais

#### Se quiser persistência de dados (recomendado):
No Streamlit Cloud, em "Advanced settings" > "Secrets", adicione:

```toml
SQLITE_PATH = "/mount/data/estoque.db"
```

**Importante:** O Streamlit Cloud não persiste arquivos automaticamente. Para produção real:
- Use um banco PostgreSQL externo (ElephantSQL, Supabase, etc.)
- Configure a variável `DATABASE_URL` nos secrets:

```toml
DATABASE_URL = "postgresql+psycopg2://usuario:senha@host:5432/database"
```

E adicione ao `requirements.txt`:
```
psycopg2-binary==2.9.9
```

### 4. Deploy
- Clique em "Deploy!"
- Aguarde alguns minutos (primeira vez pode demorar)
- Seu app estará disponível em: `https://[seu-app].streamlit.app`

## 🔐 Credenciais Padrão

Após o deploy, faça login com:

- **Admin**: 
  - Usuário: `admin`
  - Senha: `admin123`

- **Usuário**: 
  - Usuário: `usuario`
  - Senha: `usuario123`

## ⚠️ Importante

### Banco de Dados
- O SQLite no Streamlit Cloud é **efêmero** (dados perdidos a cada deploy)
- Para uso em produção, configure um banco externo (PostgreSQL recomendado)
- O sistema cria usuários padrão automaticamente na primeira execução

### Segurança
- **Altere as senhas padrão** após o primeiro acesso
- Configure variáveis secretas no Streamlit Cloud (não no código)

## 🔧 Solução de Problemas

### App não inicia
1. Verifique os logs no Streamlit Cloud
2. Certifique-se que `requirements.txt` está correto
3. Verifique se o Python é compatível (3.8+)

### Erros de banco
1. O banco será recriado a cada deploy (normal em SQLite)
2. Para persistência, use banco externo
3. Migrations rodam automaticamente no início

## 📊 Recursos do Dashboard

- ✅ Login com controle de acesso (admin/usuário)
- ✅ Dashboard com gráficos interativos
- ✅ Adicionar/Atualizar equipamentos
- ✅ Remover equipamentos por quantidade
- ✅ Mesmo código pode ter NOVO e USADO separados
- ✅ Filtros de busca avançados
- ✅ Timestamps de criação e atualização

## 🌐 URL do Repositório

https://github.com/hytalofernando/dashboard-sql

## 📝 Manutenção

Para atualizar o app no Streamlit Cloud:
```bash
git add .
git commit -m "sua mensagem"
git push origin master
```

O Streamlit Cloud detecta automaticamente e faz redeploy.

## 🆘 Suporte

Para problemas ou dúvidas:
- Consulte a documentação: https://docs.streamlit.io/
- Verifique os arquivos: `MANUTENCAO.md`, `README.md`

