# 🔧 Correção: Código Duplicado com Tipos Diferentes

## 🐛 Problema Identificado

### Erro reportado:
```
UNIQUE constraint failed: equipments.codigo
```

### O que acontecia:
Quando você tentava adicionar o mesmo código com tipos diferentes (NOVO e USADO), o sistema retornava erro.

**Exemplo que falhava:**
1. Adicionar: Código `1`, Nome `TESTE1`, Tipo `NOVO` ✅ Funcionava
2. Adicionar: Código `1`, Nome `TESTE1`, Tipo `USADO` ❌ Erro!

---

## 🔍 Causa Raiz

O banco de dados foi criado com uma **constraint UNIQUE** no campo `codigo`, o que impedia códigos duplicados mesmo com tipos diferentes.

### Estrutura antiga (problemática):
```sql
CREATE TABLE equipments (
    id INTEGER PRIMARY KEY,
    codigo TEXT UNIQUE,  ⬅️ PROBLEMA: UNIQUE impede duplicatas
    nome TEXT,
    tipo TEXT,
    quantidade INTEGER
)
```

### Lógica desejada do sistema:
O sistema foi projetado para permitir:
- `EQ001 - NOVO` ✅
- `EQ001 - USADO` ✅ (mesmo código, tipo diferente)

Mas o banco impedia isso por causa da constraint UNIQUE.

---

## ✅ Solução Implementada

### 1. Migration Automática

Foi adicionada uma função de migration em `database.py` que:

1. ✅ **Detecta** se a tabela tem a constraint UNIQUE problemática
2. ✅ **Cria** uma nova tabela sem a constraint
3. ✅ **Copia** todos os dados da tabela antiga
4. ✅ **Remove** a tabela antiga
5. ✅ **Renomeia** a nova tabela
6. ✅ **Preserva** 100% dos dados

### Estrutura nova (corrigida):
```sql
CREATE TABLE equipments (
    id INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL,  ⬅️ CORRIGIDO: Sem UNIQUE
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    data_adicao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### 2. Índice para Performance

Foi criado um **índice** no campo `codigo` (sem ser UNIQUE) para manter buscas rápidas:
```sql
CREATE INDEX ix_equipments_codigo ON equipments (codigo)
```

---

## 🚀 Como Aplicar a Correção

### Opção 1: Reiniciar o Streamlit (Recomendado)

A correção é aplicada automaticamente ao iniciar o sistema:

```bash
# Pare o Streamlit (Ctrl+C)

# Inicie novamente
.\venv\Scripts\python.exe -m streamlit run main.py
```

Você verá a mensagem:
```
🔄 Corrigindo constraint UNIQUE do código...
✅ Constraint corrigida! Agora você pode ter o mesmo código com tipos diferentes.
```

### Opção 2: Executar Migration Manualmente

```bash
python -c "from database import init_db; init_db()"
```

### Opção 3: Testar a Correção

Execute o script de teste:
```bash
.\venv\Scripts\python.exe testar_codigo_duplicado.py
```

Este script:
- ✅ Testa adicionar equipamento NOVO
- ✅ Testa adicionar USADO com mesmo código
- ✅ Verifica se ambos foram salvos
- ✅ Limpa os dados de teste

---

## 📊 Comportamento Após a Correção

### ✅ Agora funciona:

| Código | Nome | Tipo | Quantidade | Resultado |
|--------|------|------|------------|-----------|
| EQ001 | Notebook | NOVO | 10 | ✅ Salvo como registro 1 |
| EQ001 | Notebook | USADO | 5 | ✅ Salvo como registro 2 |

**Resultado:** 2 registros separados no banco!

### 📈 Atualização de Quantidade

Ao adicionar equipamento existente (mesmo código **E** mesmo tipo):
- Quantidade é **somada** automaticamente
- Data de atualização é registrada

**Exemplo:**
```
1º: EQ001 - Notebook - NOVO - 10 unidades
2º: EQ001 - Notebook - NOVO - 5 unidades (adiciona mais)
Resultado: EQ001 - Notebook - NOVO - 15 unidades ✅
```

---

## 🔐 Garantias de Segurança

### ✅ Dados Preservados
- Todos os equipamentos existentes são copiados
- IDs são mantidos
- Quantidades preservadas
- Nenhuma informação é perdida

### ✅ Processo Seguro
- Migration é executada dentro de uma transação
- Se der erro, nada é alterado (rollback automático)
- Tabela antiga só é deletada após nova estar pronta

### ✅ Backward Compatible
- Bancos antigos são migrados automaticamente
- Bancos novos já são criados corretos
- Não requer intervenção manual

---

## 🧪 Como Testar

### Teste 1: Via Script
```bash
.\venv\Scripts\python.exe testar_codigo_duplicado.py
```

### Teste 2: Via Interface
1. Acesse o sistema
2. Vá em "Adicionar Equipamento"
3. Adicione: Código `TESTE`, Nome `Produto X`, Tipo `NOVO`, Qtd `10`
4. Adicione: Código `TESTE`, Nome `Produto X`, Tipo `USADO`, Qtd `5`
5. ✅ Ambos devem ser salvos com sucesso!
6. Verifique no Dashboard: deve aparecer 2 registros

### Teste 3: Atualização de Quantidade
1. Adicione: Código `ABC`, Nome `Item`, Tipo `NOVO`, Qtd `10`
2. Adicione: Código `ABC`, Nome `Item`, Tipo `NOVO`, Qtd `5`
3. ✅ Deve mostrar: "Quantidade atualizada! Anterior: 10, Atual: 15"

---

## 📝 Notas Técnicas

### Por que não usar UNIQUE composto?

Poderíamos ter usado `UNIQUE(codigo, tipo)`, mas optamos por:
1. **Flexibilidade**: Permite ajustes futuros na lógica
2. **Simplicidade**: Validação na aplicação é mais clara
3. **Controle**: Aplicação gerencia regras de negócio

### Índices criados:
- `ix_equipments_codigo`: Índice simples no código (não-único)
- Melhora performance de buscas
- Permite duplicatas

---

## ✅ Verificação Final

Execute este comando para verificar a estrutura da tabela:

```bash
.\venv\Scripts\python.exe verificar_banco.py
```

Você deve ver:
```
🗃️  ESTRUTURA DA TABELA EQUIPMENTS:
ID    Nome                      Tipo            Not Null   Default        
----------------------------------------------------------------------
0     id                        INTEGER         SIM        -              
1     codigo                    TEXT            SIM        -              ⬅️ Sem UNIQUE
2     nome                      TEXT            SIM        -              
3     tipo                      TEXT            SIM        -              
4     quantidade                INTEGER         SIM        0              
5     data_adicao               DATETIME        NÃO        CURRENT_...    
6     ultima_atualizacao        DATETIME        NÃO        CURRENT_...    
```

**Importante:** A coluna `codigo` NÃO deve ter "UNIQUE" na descrição!

---

## 🆘 Solução de Problemas

### Se o erro persistir após reiniciar:

1. **Verifique se a migration rodou:**
   - Procure por mensagens: "🔄 Corrigindo constraint..." nos logs

2. **Force a migration:**
   ```bash
   python -c "from database import init_db; init_db()"
   ```

3. **Último recurso - Backup e recriação:**
   ```bash
   # 1. Faça backup
   python backup.py
   
   # 2. Delete o banco
   del estoque.db
   
   # 3. Inicie o sistema (recria o banco correto)
   .\venv\Scripts\python.exe -m streamlit run main.py
   ```

   ⚠️ **Atenção:** Opção 3 cria banco novo vazio! Use o backup para restaurar dados.

---

## 📞 Resumo

✅ **Problema identificado e corrigido**  
✅ **Migration automática implementada**  
✅ **Dados preservados com segurança**  
✅ **Sistema agora permite código duplicado com tipos diferentes**  
✅ **Testes incluídos para verificação**  

**Reinicie o Streamlit e teste!** 🚀



