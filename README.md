# 📦 Dashboard de Estoque v2.0

Sistema completo de gerenciamento de estoque desenvolvido em Python com Streamlit, SQLAlchemy e Plotly.

## 🚀 Funcionalidades

- **Sistema de Login**: Autenticação segura com bcrypt e dois tipos de usuário
- **Dashboard Interativo**: 
  - Gráficos dinâmicos (pizza e barras)
  - Estatísticas em tempo real
  - Filtros avançados de busca
  - Lista completa de equipamentos com timestamps
- **Gerenciamento Inteligente**: 
  - Adicionar equipamentos ou atualizar quantidades automaticamente
  - Remover por quantidade (parcial ou total)
  - Separação de equipamentos NOVO e USADO por código
  - Registro de datas de adição e atualização
- **Banco de Dados**: SQLite com SQLAlchemy ORM e migrations automáticas
- **Interface Moderna**: Design responsivo com CSS personalizado

## 📋 Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

1. Execute a aplicação:
```bash
streamlit run main.py
```

2. Acesse no navegador a URL exibida (geralmente `http://localhost:8501`)

3. Faça login com uma das contas padrão:
   - **Admin**: 
     - Usuário: `admin`
     - Senha: `admin123`
   - **Usuário**: 
     - Usuário: `usuario`
     - Senha: `usuario123`

## 👥 Permissões

### Admin
- ✅ Visualizar dashboard completo com filtros
- ✅ Adicionar equipamentos ou atualizar quantidades
- ✅ Remover equipamentos (parcial ou total)
- ✅ Ver histórico de datas (adição e atualização)

### Usuário
- ✅ Visualizar dashboard completo (apenas leitura)
- ✅ Usar filtros de busca
- ✅ Ver todas as estatísticas e gráficos
- ❌ Não pode adicionar equipamentos
- ❌ Não pode remover equipamentos

## ✨ Novidades da v2.0

### 📊 Dashboard Aprimorado
- **5 métricas principais**: Itens no banco, quantidade total, NOVO, USADO e códigos únicos
- **Gráfico de pizza**: Visualização da proporção NOVO vs USADO
- **Top 5 equipamentos**: Gráfico de barras horizontal dos itens mais abundantes
- **Lista completa**: Tabela com todos os equipamentos e suas informações
- **Filtros avançados**: Busca por tipo, código ou nome
- **Timestamps**: Data de adição e última atualização de cada item

### ➕ Adicionar Equipamentos Melhorado
- **Atualização automática**: Se código+tipo já existem, aumenta a quantidade automaticamente
- **Separação NOVO/USADO**: Mesmo código pode ter versões NOVO e USADO distintas
- **Feedback detalhado**: Mensagens informando quantidade anterior, adicionada e atual
- **Registro de timestamp**: Data/hora de quando foi adicionado ou atualizado
- **Validações**: Campos obrigatórios e mensagens claras

### ➖ Remover Equipamentos Melhorado
- **Remoção por quantidade**: Escolha quantas unidades remover
- **Remoção parcial**: Reduz quantidade mantendo o item no sistema
- **Remoção total**: Opção para deletar completamente o equipamento
- **Proteções**: Não permite remover mais do que disponível
- **Feedback completo**: Informa quantidade anterior, removida e restante

### 🎨 Melhorias Visuais
- **CSS personalizado**: Elementos com sombras e bordas arredondadas
- **Cores consistentes**: Verde para NOVO (#2ecc71) e vermelho para USADO (#e74c3c)
- **Ícones**: Emojis para melhor identificação visual
- **Layout responsivo**: Colunas adaptativas e melhor uso do espaço
- **Mensagens formatadas**: Success/error boxes com formatação markdown
- **Animações**: Balões ao adicionar equipamentos com sucesso

## 📊 Estrutura do Projeto

```
novodb/
├── main.py              # Aplicação principal Streamlit
├── models.py            # Modelos SQLAlchemy (User, Equipment)
├── database.py          # Configuração do banco de dados
├── auth.py              # Sistema de autenticação
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
└── estoque.db          # Banco de dados SQLite (criado automaticamente)
```

## 🌐 Deploy no Streamlit.io

1. Crie uma conta no [Streamlit Cloud](https://streamlit.io/cloud)

2. Conecte seu repositório GitHub

3. Configure o app:
   - **Main file**: `main.py`
   - **Python version**: 3.8+

4. O banco de dados SQLite será criado automaticamente no primeiro acesso

## 🔒 Segurança

- Senhas são armazenadas com hash usando bcrypt
- Validação de código único para equipamentos
- Controle de acesso baseado em roles

## 📝 Notas Importantes

- O banco de dados é **permanente e seguro**
- Sistema de migrations automático preserva todos os dados
- **Mesmo código pode ter versões NOVO e USADO separadas** (ex: EQ001 NOVO e EQ001 USADO)
- Se código+tipo já existem → quantidade é **somada automaticamente**
- O banco de dados é criado automaticamente na primeira execução
- Os usuários padrão são criados automaticamente se não existirem
- **Backup recomendado**: Execute `python backup.py` regularmente
- **Migration automática** corrige problemas de constraint ao iniciar

## 🔐 Segurança e Backup dos Dados

### O banco de dados é permanente!

✅ Todos os dados são salvos em `estoque.db`  
✅ Sistema de migrations automático preserva dados existentes  
✅ Nunca perde informações em atualizações  
✅ Ideal para uso empresarial  

### Scripts de manutenção incluídos:

1. **`backup.py`** - Cria backup com data/hora
   ```bash
   .\venv\Scripts\python.exe backup.py
   ```

2. **`verificar_banco.py`** - Verifica integridade e estatísticas
   ```bash
   .\venv\Scripts\python.exe verificar_banco.py
   ```

3. **`agendar_backup.bat`** - Agenda backup automático diário (Windows)
   - Execute como Administrador
   - Cria tarefa para backup diário às 23:00

### Consulte o guia completo:
📖 **[MANUTENCAO.md](MANUTENCAO.md)** - Guia completo de backup e segurança

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web
- **SQLAlchemy**: ORM para Python
- **SQLite**: Banco de dados leve e portátil
- **Plotly**: Gráficos interativos
- **Pandas**: Manipulação de dados
- **bcrypt**: Hash de senhas

## 📧 Suporte

Para dúvidas ou problemas, verifique os logs de erro no console ou entre em contato com o administrador do sistema.

