# 🗄️ Configuração do Banco de Dados Supabase

## ✅ Connection String Correta:

```
postgresql+psycopg2://postgres:hytalobb3030@db.kkfwxabdkdgrkxcselyg.supabase.co:5432/postgres
```

---

## 🚀 Como Configurar no Streamlit Cloud:

### Passo 1: Acesse o Streamlit Cloud
1. Vá em: https://share.streamlit.io/
2. Faça login
3. Encontre seu app `dashboard-sql`

### Passo 2: Abra as Configurações
1. Clique nos **três pontinhos (⋮)** no card do app
2. Clique em **Settings**

### Passo 3: Configure o Secret
1. Clique na aba **Secrets**
2. **APAGUE TUDO** que está lá
3. **Cole EXATAMENTE isso:**

```toml
DATABASE_URL = "postgresql+psycopg2://postgres:hytalobb3030@db.kkfwxabdkdgrkxcselyg.supabase.co:5432/postgres"
```

### Passo 4: Salve
1. Clique em **Save**
2. O app vai fazer **redeploy automaticamente** (aguarde 1-2 minutos)

### Passo 5: Teste
1. Acesse seu app
2. Faça login (admin/admin123)
3. Adicione um equipamento de teste
4. Vá no Supabase → Table Editor
5. Você verá as tabelas `users` e `equipments`! ✅

---

## 🔍 Verificar se Funcionou no Supabase:

### Opção 1: Via Painel Web
1. Acesse: https://app.supabase.com/
2. Selecione seu projeto
3. Vá em **Table Editor** (ícone de tabela no menu lateral)
4. Você verá as tabelas:
   - ✅ `users` (com admin e usuario)
   - ✅ `equipments` (com os equipamentos que você adicionar)

### Opção 2: Via SQL Editor
1. No Supabase, vá em **SQL Editor**
2. Cole e execute:

```sql
-- Ver todas as tabelas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Ver usuários
SELECT id, username, role FROM users;

-- Ver equipamentos
SELECT * FROM equipments;
```

---

## ⚠️ Troubleshooting:

### Se o app não conectar:
1. **Verifique se o projeto do Supabase está ativo:**
   - No painel do Supabase, se aparecer "Project is paused", clique em "Restore"

2. **Verifique os logs do Streamlit:**
   - No Streamlit Cloud, clique em **Manage app**
   - Role até o final dos logs
   - Procure por erros de conexão

3. **Se ainda não funcionar:**
   - Use **Connection Pooling** ao invés de Direct Connection
   - No Supabase: Settings → Database → Connection Pooling
   - Copie a string que tem `pooler.supabase.com`

---

## 📊 Por que não funciona localmente?

Possíveis motivos:
- Firewall corporativo bloqueando porta 5432
- Proxy da empresa
- Antivírus bloqueando conexões PostgreSQL
- VPN ou restrições de rede

**Mas isso não importa!** O Streamlit Cloud tem conectividade própria e geralmente funciona perfeitamente! 🚀

---

## 🎉 Após Configurar:

Seus dados estarão **permanentemente salvos** no Supabase! Não importa quantas vezes você fechar/abrir o site, os dados continuarão lá! ✅

