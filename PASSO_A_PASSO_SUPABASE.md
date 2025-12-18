# 🔧 Passo a Passo: Configurar Supabase no Streamlit Cloud

## ⚠️ IMPORTANTE: Verificar se o Projeto está Ativo

### 1. Acesse o Supabase
- URL: https://app.supabase.com/
- Faça login
- Selecione seu projeto

### 2. Verifique o Status
**Se você ver uma mensagem tipo:**
- ❌ "Project is paused"
- ❌ "Project is inactive"  
- ❌ "Project needs to be restored"

**ENTÃO FAÇA ISSO:**
1. Clique no botão **"Restore project"** ou **"Resume"**
2. Aguarde 2-3 minutos para o projeto inicializar
3. A tela ficará verde/ativa

---

## 📋 Como Pegar a Connection String Correta

### Opção 1: Connection String Direta (Recomendada)

1. **No painel do Supabase, vá em:**
   - **Settings** (⚙️ engrenagem) no menu lateral esquerdo
   - **Database** (no submenu)

2. **Role a página até encontrar "Connection string"**

3. **Você verá várias abas/opções:**
   - **URI** ← SELECIONE ESTA!
   - Nodejs
   - .NET
   - etc.

4. **Clique em "URI"** e você verá algo assim:

```
postgresql://postgres:[YOUR-PASSWORD]@db.kkfwxabdkdgrkxcselyg.supabase.co:5432/postgres
```

5. **Clique no ícone "👁️ Reveal Password"** (se tiver)
   - A senha será preenchida automaticamente
   - Ou você precisa substituir `[YOUR-PASSWORD]` pela sua senha

6. **Copie a string completa**

---

### Opção 2: Connection Pooling (Se a Opção 1 não funcionar)

Se o host `db.xxx.supabase.co` não funcionar, tente com Connection Pooling:

1. **No mesmo lugar (Settings → Database)**

2. **Procure por "Connection Pooling"** (pode estar em uma seção separada)

3. **Escolha o modo:**
   - **Transaction** (recomendado para Streamlit)

4. **Você verá algo assim:**

```
postgresql://postgres.kkfwxabdkdgrkxcselyg:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**Observe as diferenças:**
- Host: `aws-0-us-east-1.pooler.supabase.com` (ao invés de `db.xxx.supabase.co`)
- Porta: `6543` (ao invés de `5432`)
- Usuário: `postgres.kkfwxabdkdgrkxcselyg` (ao invés de só `postgres`)

5. **Copie esta string**

---

## 🔄 Formato para o Streamlit

**IMPORTANTE:** Você precisa adicionar `+psycopg2` após `postgresql`

### Se você copiou (Opção 1):
```
postgresql://postgres:hytalobb3030@db.kkfwxabdkdgrkxcselyg.supabase.co:5432/postgres
```

### Transforme em:
```
postgresql+psycopg2://postgres:hytalobb3030@db.kkfwxabdkdgrkxcselyg.supabase.co:5432/postgres
```

### Se você copiou (Opção 2 - Pooling):
```
postgresql://postgres.kkfwxabdkdgrkxcselyg:hytalobb3030@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### Transforme em:
```
postgresql+psycopg2://postgres.kkfwxabdkdgrkxcselyg:hytalobb3030@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

---

## ⚙️ Configurar no Streamlit Cloud

### 1. Acesse o Streamlit Cloud
- URL: https://share.streamlit.io/
- Encontre seu app **dashboard-sql**

### 2. Abra Settings
- Clique nos **três pontinhos (⋮)** no card do app
- Clique em **Settings**

### 3. Configure o Secret
- Clique na aba **Secrets**
- **APAGUE TUDO** que está lá (Ctrl+A, Delete)
- **Cole a configuração:**

```toml
DATABASE_URL = "postgresql+psycopg2://postgres:hytalobb3030@db.kkfwxabdkdgrkxcselyg.supabase.co:5432/postgres"
```

**OU** (se usar Connection Pooling):

```toml
DATABASE_URL = "postgresql+psycopg2://postgres.kkfwxabdkdgrkxcselyg:hytalobb3030@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
```

### 4. Salve
- Clique em **Save**
- O app fará redeploy automaticamente
- Aguarde 1-2 minutos

---

## 🧪 Testar se Funcionou

### 1. Abra seu app no Streamlit
- Aguarde o redeploy terminar
- Se ver erro, clique em **"Manage app"** → **"Logs"**

### 2. Nos logs, procure por:
```
✅ PostgreSQL conectado: PostgreSQL 15.x...
```

Se ver isso, **FUNCIONOU!** ✅

Se ver:
```
❌ Erro ao conectar ao banco: ...
⚠️ Caindo para SQLite local...
```

Então ainda há problema na conexão.

### 3. Teste adicionando um equipamento
- Faça login (admin/admin123)
- Vá em "Adicionar Equipamento"
- Adicione um teste

### 4. Verifique no Supabase
- Vá no Supabase → **Table Editor**
- Você verá as tabelas `users` e `equipments`
- Se aparecerem, **SUCESSO!** 🎉

---

## 🚨 Se AINDA não funcionar

### Alternativa: Criar Novo Projeto no Supabase

O host `db.kkfwxabdkdgrkxcselyg.supabase.co` pode estar com problemas.

1. No Supabase, crie um **novo projeto**
2. Escolha uma região próxima (ex: South America)
3. Defina uma senha simples (ex: `senha1234`)
4. Aguarde a criação (2-3 minutos)
5. Pegue a nova connection string
6. Configure no Streamlit

---

## 📞 Me Avise

Faça o teste e me diga:

1. ✅ O projeto do Supabase está **ativo**?
2. 📋 Qual connection string você está usando? (pode ocultar a senha com ***)
3. 📊 O que aparece nos logs do Streamlit? (clique em "Manage app" → "Logs")

Com essas informações, eu te ajudo a resolver! 🚀

