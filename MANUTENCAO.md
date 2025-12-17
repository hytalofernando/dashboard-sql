# 🔧 Guia de Manutenção e Segurança do Banco de Dados

## 🛡️ Garantia de Dados Permanentes

### ✅ O banco de dados é PERMANENTE e SEGURO

O sistema foi desenvolvido para **NUNCA** perder dados em operação normal. Veja como funciona:

---

## 🔄 Sistema de Migrations Automático

### Como funciona:

Toda vez que o sistema inicia (`main.py`), ele executa:

```python
init_db()  # Inicializa banco e executa migrations
```

A função `migrate_db()` em `database.py`:

1. ✅ **Verifica** se a tabela existe
2. ✅ **Lista** todas as colunas existentes
3. ✅ **Adiciona APENAS** colunas que faltam
4. ✅ **Preserva TODOS** os dados existentes
5. ✅ **Preenche** valores padrão em registros antigos

### Exemplo prático:

**Antes da atualização:**
```
equipments: id, codigo, tipo, quantidade
```

**Após rodar o sistema:**
```
equipments: id, codigo, tipo, quantidade, nome, data_adicao, ultima_atualizacao
```

**Resultado:** Todos os dados antigos continuam lá! ✅

---

## 📁 Localização do Banco de Dados

O arquivo do banco está em:
```
C:\Pyhton\novodb\estoque.db
```

Este arquivo contém **TODOS** os dados do sistema:
- Usuários
- Equipamentos
- Quantidades
- Datas

---

## 💾 Backup do Banco de Dados

### Backup Manual (Recomendado para empresas)

#### Opção 1: Backup Simples
```bash
# Copia o banco para um backup com data
copy estoque.db estoque_backup_2024-12-03.db
```

#### Opção 2: Script de Backup Automático (Windows)

Crie um arquivo `backup.bat`:

```batch
@echo off
set DATA=%date:~-4%%date:~3,2%%date:~0,2%
set HORA=%time:~0,2%%time:~3,2%
copy estoque.db backups\estoque_%DATA%_%HORA%.db
echo Backup criado: backups\estoque_%DATA%_%HORA%.db
```

Execute diariamente com o Agendador de Tarefas do Windows.

#### Opção 3: Backup em Python

Crie um arquivo `backup.py`:

```python
import shutil
from datetime import datetime
import os

# Cria pasta de backups se não existir
if not os.path.exists('backups'):
    os.makedirs('backups')

# Nome do backup com data/hora
backup_name = f"backups/estoque_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

# Copia o banco
shutil.copy2('estoque.db', backup_name)

print(f"✅ Backup criado: {backup_name}")
```

Execute periodicamente:
```bash
.\venv\Scripts\python.exe backup.py
```

---

## 🔐 Segurança dos Dados

### 1. Permissões de Arquivo

No Windows, configure permissões para que apenas administradores possam deletar:
- Clique com botão direito em `estoque.db`
- Propriedades → Segurança
- Configure permissões apropriadas

### 2. Localização Segura

Para produção, considere mover o banco para:
```
C:\ProgramData\SeuEmpresa\estoque\estoque.db
```

Atualize em `database.py`:
```python
DATABASE_URL = "sqlite:///C:/ProgramData/SeuEmpresa/estoque/estoque.db"
```

### 3. Backup em Nuvem

Configure sincronização automática da pasta `backups/` com:
- OneDrive
- Google Drive
- Dropbox
- Servidor da empresa

---

## 🚫 O que NUNCA acontece automaticamente

❌ O banco **NUNCA** é deletado automaticamente  
❌ Dados **NUNCA** são perdidos em updates  
❌ Migrations **NUNCA** removem colunas  
❌ Equipamentos **NUNCA** são apagados sem ação do admin  

---

## ✅ Boas Práticas para Empresas

### 1. Backup Diário Automático
Configure um script que roda todo dia às 23:00

### 2. Backup Antes de Atualizações
Sempre faça backup antes de atualizar o sistema

### 3. Teste de Restauração
Mensalmente, teste restaurar um backup para garantir que funciona

### 4. Monitoramento
Verifique regularmente:
- Tamanho do banco (`estoque.db`)
- Quantidade de registros
- Logs de erros

### 5. Documentação
Mantenha registro de:
- Quando foram feitos backups
- Alterações no sistema
- Problemas encontrados

---

## 🔄 Restaurar Backup

### Se precisar restaurar um backup:

```bash
# 1. Pare o Streamlit (Ctrl+C)

# 2. Faça backup do banco atual
copy estoque.db estoque_antes_restauracao.db

# 3. Restaure o backup desejado
copy backups\estoque_20241203.db estoque.db

# 4. Reinicie o Streamlit
.\venv\Scripts\python.exe -m streamlit run main.py
```

---

## 📊 Verificar Integridade do Banco

Execute este script para verificar se o banco está OK:

```python
# verificar_banco.py
import sqlite3
from datetime import datetime

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

print("=" * 50)
print(f"📊 Verificação do Banco - {datetime.now()}")
print("=" * 50)

# Verifica tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = cursor.fetchall()
print(f"\n✅ Tabelas encontradas: {len(tabelas)}")
for tabela in tabelas:
    print(f"   - {tabela[0]}")

# Verifica equipamentos
cursor.execute("SELECT COUNT(*) FROM equipments")
total_equipamentos = cursor.fetchone()[0]
print(f"\n📦 Total de equipamentos: {total_equipamentos}")

# Verifica usuários
cursor.execute("SELECT COUNT(*) FROM users")
total_usuarios = cursor.fetchone()[0]
print(f"\n👥 Total de usuários: {total_usuarios}")

# Verifica estrutura da tabela equipments
cursor.execute("PRAGMA table_info(equipments)")
colunas = cursor.fetchall()
print(f"\n🗃️ Colunas da tabela equipments:")
for coluna in colunas:
    print(f"   - {coluna[1]} ({coluna[2]})")

conn.close()

print("\n" + "=" * 50)
print("✅ Verificação concluída!")
print("=" * 50)
```

Execute:
```bash
.\venv\Scripts\python.exe verificar_banco.py
```

---

## 🆘 Suporte e Problemas

### Se o banco for acidentalmente deletado:

1. **Não entre em pânico!**
2. Verifique a pasta `backups/`
3. Restaure o backup mais recente
4. Se não houver backup, o sistema criará um novo banco vazio

### Se houver corrupção de dados:

```bash
# Tente reparar com SQLite
sqlite3 estoque.db "PRAGMA integrity_check"
```

Se houver erros, restaure o backup mais recente.

---

## 📞 Contatos

Em caso de dúvidas ou problemas com o banco de dados:
- Verifique os logs do Streamlit
- Execute o script de verificação
- Consulte este guia

---

## 📝 Checklist de Segurança

- [ ] Backups automáticos configurados
- [ ] Backup testado e restaurado com sucesso
- [ ] Permissões de arquivo configuradas
- [ ] Banco em localização segura
- [ ] Sincronização com nuvem ativa
- [ ] Script de verificação testado
- [ ] Equipe treinada em restauração

---

**Lembre-se:** O sistema é seguro e permanente. Backups são apenas uma precaução adicional! ✅



