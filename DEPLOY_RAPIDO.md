# 🚀 Deploy Rápido no Streamlit Cloud

## Passo a Passo Simplificado

### 1️⃣ Acesse o Streamlit Cloud
👉 https://share.streamlit.io/

### 2️⃣ Faça Login
- Clique em **"Sign in with GitHub"**
- Autorize o acesso

### 3️⃣ Crie Novo App
- Clique em **"New app"** (botão azul)

### 4️⃣ Preencha os Dados

```
Repository: hytalofernando/dashboard-sql
Branch: master
Main file path: main.py
App URL (opcional): escolha um nome único
```

### 5️⃣ Configurar Secrets (OPCIONAL)

**Opção A: Deploy Rápido (SQLite - para teste)**
- ✅ NÃO adicione secrets
- ✅ Clique direto em "Deploy!"
- ⚠️ Dados serão perdidos a cada redeploy

**Opção B: PostgreSQL (para produção)**
1. Clique em **"Advanced settings"**
2. Vá em **"Secrets"**
3. Cole:
```toml
DATABASE_URL = "postgresql+psycopg2://usuario:senha@host:5432/database"
```
4. Substitua pelos dados do seu banco PostgreSQL

### 6️⃣ Deploy!
- Clique em **"Deploy!"**
- Aguarde 2-5 minutos
- ✅ Pronto! Seu app está no ar!

---

## 🔐 Como Acessar Após Deploy

Seu app estará em: `https://[seu-nome-app].streamlit.app`

**Login:**
- Usuário: `admin` ou `usuario`
- Senha: (você sabe qual é, não está mais visível na tela 😉)

---

## 💾 Onde Conseguir PostgreSQL Gratuito?

### Supabase (RECOMENDADO)
1. Crie conta: https://supabase.com/
2. New Project > Copie a Database URL
3. Troque `postgresql://` por `postgresql+psycopg2://`
4. Cole nos Secrets do Streamlit Cloud

### ElephantSQL
1. Crie conta: https://www.elephantsql.com/
2. Create Instance > Plano Tiny Turtle (free)
3. Copie a URL
4. Cole nos Secrets do Streamlit Cloud

---

## ⚠️ Se Usar PostgreSQL

**Importante:** Descomente esta linha no `requirements.txt`:

```
psycopg2-binary==2.9.9
```

Depois faça:
```bash
git add requirements.txt
git commit -m "feat: adiciona suporte PostgreSQL"
git push origin master
```

O Streamlit Cloud vai detectar e fazer redeploy automaticamente.

---

## 🆘 Problemas?

### App não inicia
- Veja os logs na interface do Streamlit Cloud
- Clique no app > "Manage app" > "Logs"

### Erro de banco
- Verifique a connection string nos Secrets
- Certifique-se que `psycopg2-binary` está no requirements.txt

### Dados desaparecem
- Você está usando SQLite (normal)
- Configure PostgreSQL para persistência

---

## 🎯 Deploy Rápido em 30 Segundos

1. https://share.streamlit.io/ → Sign in
2. New app → `hytalofernando/dashboard-sql` → `master` → `main.py`
3. Deploy!
4. ✅ Pronto!

---

**Consulte `VARIAVEIS_AMBIENTE.md` para configuração detalhada de banco de dados.**

