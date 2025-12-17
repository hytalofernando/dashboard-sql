# 🔐 Configuração de Variáveis de Ambiente no Streamlit Cloud

## 📋 Variáveis Necessárias

### Opção 1: SQLite (Modo Demo - Dados Efêmeros)

**Nenhuma variável necessária!** O sistema usa SQLite local automaticamente.

⚠️ **Atenção:** No Streamlit Cloud, dados SQLite são perdidos a cada redeploy.

---

### Opção 2: PostgreSQL (RECOMENDADO para Produção)

Configure a variável `DATABASE_URL` com a string de conexão do seu banco PostgreSQL.

---

## 🚀 Como Configurar no Streamlit Cloud

### Passo 1: Acesse as Configurações do App

1. Entre em https://share.streamlit.io/
2. Clique no seu app: `dashboard-sql`
3. Clique nos **três pontinhos** (⋮) ao lado do app
4. Selecione **"Settings"**

### Passo 2: Configure os Secrets

1. Vá em **"Secrets"** no menu lateral
2. Cole a configuração desejada (veja exemplos abaixo)
3. Clique em **"Save"**
4. O app será reiniciado automaticamente

---

## 📝 Exemplos de Configuração

### Para SQLite (Simples, mas efêmero)

**Opção A: Sem configuração (padrão)**
- Não adicione nada nos secrets
- O sistema usará `estoque.db` local
- ⚠️ Dados perdidos a cada redeploy

**Opção B: Tentar persistência (pode não funcionar)**
```toml
SQLITE_PATH = "/mount/data/estoque.db"
```
⚠️ Streamlit Cloud pode não persistir este caminho

---

### Para PostgreSQL (RECOMENDADO)

#### Opção 1: ElephantSQL (Gratuito - 20MB)

1. Crie conta em: https://www.elephantsql.com/
2. Crie uma instância (plano Tiny Turtle - gratuito)
3. Copie a URL de conexão
4. No Streamlit Cloud, em **Secrets**, adicione:

```toml
DATABASE_URL = "postgresql+psycopg2://usuario:senha@hostname.db.elephantsql.com/database"
```

**Substitua** `usuario`, `senha`, `hostname` e `database` pelos seus valores.

---

#### Opção 2: Supabase (Gratuito - 500MB)

1. Crie conta em: https://supabase.com/
2. Crie um novo projeto
3. Vá em Settings > Database > Connection String > URI
4. Copie a URI e **troque** `postgresql://` por `postgresql+psycopg2://`
5. No Streamlit Cloud, em **Secrets**, adicione:

```toml
DATABASE_URL = "postgresql+psycopg2://postgres:sua_senha@db.xxxxx.supabase.co:5432/postgres"
```

---

#### Opção 3: Railway (Gratuito com limite)

1. Crie conta em: https://railway.app/
2. Crie novo projeto > Add PostgreSQL
3. Clique no banco > Connect > Connection URL
4. Copie a URL e **troque** `postgresql://` por `postgresql+psycopg2://`
5. No Streamlit Cloud, em **Secrets**, adicione:

```toml
DATABASE_URL = "postgresql+psycopg2://postgres:senha@containers-us-west-xx.railway.app:xxxx/railway"
```

---

#### Opção 4: Neon (Gratuito - 3GB)

1. Crie conta em: https://neon.tech/
2. Crie um novo projeto
3. Copie a connection string
4. **Troque** `postgresql://` por `postgresql+psycopg2://`
5. No Streamlit Cloud, em **Secrets**, adicione:

```toml
DATABASE_URL = "postgresql+psycopg2://usuario:senha@ep-xxxxx.us-east-2.aws.neon.tech/neondb"
```

---

## 🔧 Configuração Adicional para PostgreSQL

Se você escolheu PostgreSQL, adicione ao `requirements.txt`:

```
psycopg2-binary==2.9.9
```

**Já está incluído?** Verifique o arquivo `requirements.txt` do projeto.

---

## 🧪 Testar Configuração

### Teste Local (antes de fazer deploy)

1. Crie arquivo `.streamlit/secrets.toml` (local, não commitado):

```toml
DATABASE_URL = "sua_connection_string_aqui"
```

2. Execute localmente:
```bash
streamlit run main.py
```

3. Verifique se conecta ao banco corretamente

4. **Não commite o arquivo secrets.toml!** (já está no .gitignore)

---

## ✅ Configuração Mínima Recomendada para Produção

### Para iniciar rápido (SQLite):
- **Nenhuma configuração necessária**
- Deploy direto
- ⚠️ Use apenas para demonstração

### Para produção real (PostgreSQL):

```toml
# No Streamlit Cloud > Settings > Secrets
DATABASE_URL = "postgresql+psycopg2://usuario:senha@host:5432/database"
```

---

## 🔐 Segurança

### ⚠️ NUNCA:
- ❌ Commite secrets no GitHub
- ❌ Compartilhe URLs de banco com senhas
- ❌ Use senhas fracas

### ✅ SEMPRE:
- ✅ Use variáveis de ambiente no Streamlit Cloud
- ✅ Use senhas fortes
- ✅ Mantenha backups do banco
- ✅ Use SSL/TLS na conexão (já incluído no PostgreSQL)

---

## 📊 Comparação de Opções

| Provedor | Gratuito | Limite | Persistência | Recomendado |
|----------|----------|--------|--------------|-------------|
| SQLite (local) | ✅ | - | ❌ Efêmero | Para demo |
| ElephantSQL | ✅ | 20MB | ✅ | Para testes |
| Supabase | ✅ | 500MB | ✅ | ⭐ Melhor gratuito |
| Railway | ✅ | Tempo limite | ✅ | Para MVP |
| Neon | ✅ | 3GB | ✅ | ⭐ Melhor para crescer |

---

## 🆘 Problemas Comuns

### Erro: "could not connect to server"
- Verifique se a connection string está correta
- Verifique se o banco PostgreSQL está ativo
- Verifique se a senha está correta

### Erro: "no module named psycopg2"
- Adicione `psycopg2-binary==2.9.9` ao `requirements.txt`
- Faça commit e push

### Dados desaparecem a cada deploy
- Você está usando SQLite no Streamlit Cloud
- Mude para PostgreSQL para persistência

---

## 📞 Suporte

- Documentação Streamlit Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Documentação SQLAlchemy: https://docs.sqlalchemy.org/

---

## 🎯 Resumo Rápido

**Para subir AGORA (teste/demo):**
1. Não adicione secrets
2. Deploy direto no Streamlit Cloud
3. Use SQLite (dados efêmeros)

**Para produção (recomendado):**
1. Crie banco PostgreSQL gratuito (Supabase ou Neon)
2. Configure `DATABASE_URL` nos secrets do Streamlit Cloud
3. Adicione `psycopg2-binary` ao requirements.txt
4. Deploy!

---

**Pronto para fazer deploy?** Siga o guia `DEPLOY_STREAMLIT.md`! 🚀

