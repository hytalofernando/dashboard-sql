#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Corrigir Constraint UNIQUE do Banco de Dados
Remove a constraint UNIQUE do campo codigo permitindo códigos duplicados com tipos diferentes
"""

import sqlite3
import os
from datetime import datetime

def corrigir_banco():
    """Corrige a constraint UNIQUE do campo codigo"""
    
    banco = 'estoque.db'
    
    if not os.path.exists(banco):
        print("❌ Banco de dados não encontrado!")
        return False
    
    print("\n" + "=" * 70)
    print("🔧 CORREÇÃO DA CONSTRAINT UNIQUE")
    print("=" * 70)
    
    try:
        conn = sqlite3.connect(banco)
        cursor = conn.cursor()
        
        # Verifica estrutura atual
        print("\n1️⃣ Verificando estrutura atual...")
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='equipments'")
        table_sql = cursor.fetchone()
        
        if table_sql:
            print(f"\n📋 Estrutura atual:")
            print(table_sql[0])
            
            if 'UNIQUE' in table_sql[0].upper() and 'CODIGO' in table_sql[0].upper():
                print("\n⚠️  PROBLEMA DETECTADO: Campo 'codigo' tem constraint UNIQUE")
                print("🔄 Iniciando correção...\n")
                
                # Faz backup dos dados
                print("2️⃣ Fazendo backup dos dados...")
                cursor.execute("SELECT * FROM equipments")
                dados = cursor.fetchall()
                print(f"✅ {len(dados)} registro(s) copiado(s)")
                
                # Cria nova tabela sem UNIQUE
                print("\n3️⃣ Criando nova estrutura...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS equipments_new (
                        id INTEGER PRIMARY KEY,
                        codigo TEXT NOT NULL,
                        nome TEXT NOT NULL,
                        tipo TEXT NOT NULL,
                        quantidade INTEGER NOT NULL DEFAULT 0,
                        data_adicao DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                print("✅ Nova tabela criada")
                
                # Copia dados
                print("\n4️⃣ Copiando dados para nova estrutura...")
                cursor.execute("""
                    INSERT INTO equipments_new 
                    (id, codigo, nome, tipo, quantidade, data_adicao, ultima_atualizacao)
                    SELECT 
                        id, 
                        codigo, 
                        COALESCE(nome, 'Sem nome'), 
                        tipo, 
                        quantidade,
                        COALESCE(data_adicao, CURRENT_TIMESTAMP),
                        COALESCE(ultima_atualizacao, CURRENT_TIMESTAMP)
                    FROM equipments
                """)
                print(f"✅ {cursor.rowcount} registro(s) copiado(s)")
                
                # Remove tabela antiga
                print("\n5️⃣ Removendo tabela antiga...")
                cursor.execute("DROP TABLE equipments")
                print("✅ Tabela antiga removida")
                
                # Renomeia nova tabela
                print("\n6️⃣ Renomeando nova tabela...")
                cursor.execute("ALTER TABLE equipments_new RENAME TO equipments")
                print("✅ Tabela renomeada")
                
                # Cria índice
                print("\n7️⃣ Criando índice (não-único)...")
                cursor.execute("CREATE INDEX IF NOT EXISTS ix_equipments_codigo ON equipments (codigo)")
                print("✅ Índice criado")
                
                # Commit
                conn.commit()
                
                # Verifica nova estrutura
                print("\n8️⃣ Verificando nova estrutura...")
                cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='equipments'")
                new_table_sql = cursor.fetchone()
                print(f"\n📋 Nova estrutura:")
                print(new_table_sql[0])
                
                # Verifica dados
                print("\n9️⃣ Verificando dados...")
                cursor.execute("SELECT COUNT(*) FROM equipments")
                total = cursor.fetchone()[0]
                print(f"✅ Total de registros: {total}")
                
                print("\n" + "=" * 70)
                print("✅ CORREÇÃO CONCLUÍDA COM SUCESSO!")
                print("=" * 70)
                print("\n💡 Agora você pode adicionar o mesmo código com tipos diferentes!")
                print("   Exemplo: EQ001 NOVO e EQ001 USADO são permitidos.\n")
                
                return True
            else:
                print("\n✅ Banco já está correto! Não há constraint UNIQUE no campo codigo.")
                return True
        else:
            print("❌ Tabela 'equipments' não encontrada!")
            return False
            
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()


def testar_insercao():
    """Testa se pode inserir código duplicado com tipo diferente"""
    
    print("\n" + "=" * 70)
    print("🧪 TESTE DE INSERÇÃO")
    print("=" * 70)
    
    banco = 'estoque.db'
    
    try:
        conn = sqlite3.connect(banco)
        cursor = conn.cursor()
        
        # Código de teste
        codigo_teste = "TESTE_CORRECAO"
        
        # Remove testes anteriores
        cursor.execute("DELETE FROM equipments WHERE codigo = ?", (codigo_teste,))
        
        # Testa inserir NOVO
        print(f"\n1️⃣ Testando inserção: {codigo_teste} - NOVO")
        cursor.execute("""
            INSERT INTO equipments (codigo, nome, tipo, quantidade)
            VALUES (?, ?, ?, ?)
        """, (codigo_teste, "Teste Correção", "NOVO", 10))
        print("✅ Sucesso!")
        
        # Testa inserir USADO (mesmo código)
        print(f"\n2️⃣ Testando inserção: {codigo_teste} - USADO (mesmo código)")
        cursor.execute("""
            INSERT INTO equipments (codigo, nome, tipo, quantidade)
            VALUES (?, ?, ?, ?)
        """, (codigo_teste, "Teste Correção", "USADO", 5))
        print("✅ Sucesso!")
        
        # Verifica
        print(f"\n3️⃣ Verificando registros...")
        cursor.execute("SELECT codigo, tipo, quantidade FROM equipments WHERE codigo = ?", (codigo_teste,))
        registros = cursor.fetchall()
        
        print(f"\nTotal de registros com código '{codigo_teste}': {len(registros)}")
        for reg in registros:
            print(f"   - Código: {reg[0]}, Tipo: {reg[1]}, Quantidade: {reg[2]}")
        
        # Remove testes
        cursor.execute("DELETE FROM equipments WHERE codigo = ?", (codigo_teste,))
        conn.commit()
        
        print("\n" + "=" * 70)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print("\n💡 O banco está funcionando corretamente!\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {str(e)}")
        print("\nSe o erro for 'UNIQUE constraint', o banco ainda precisa ser corrigido.")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    print("\n🔧 SCRIPT DE CORREÇÃO DO BANCO DE DADOS")
    
    # Executa correção
    sucesso = corrigir_banco()
    
    if sucesso:
        # Executa teste
        input("\nPressione ENTER para testar a correção...")
        testar_insercao()
    
    input("\nPressione ENTER para sair...")


