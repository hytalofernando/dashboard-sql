#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Verificação do Banco de Dados
Verifica integridade, estatísticas e estrutura do banco
"""

import sqlite3
import os
from datetime import datetime


def verificar_banco():
    """Verifica integridade e conteúdo do banco de dados"""
    
    banco = 'estoque.db'
    
    # Verifica se o banco existe
    if not os.path.exists(banco):
        print(f"❌ Erro: Banco de dados '{banco}' não encontrado!")
        print(f"   Execute o sistema primeiro para criar o banco.")
        return False
    
    try:
        conn = sqlite3.connect(banco)
        cursor = conn.cursor()
        
        print("\n" + "=" * 70)
        print(f"📊 VERIFICAÇÃO DO BANCO DE DADOS - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 70)
        
        # Tamanho do arquivo
        tamanho = os.path.getsize(banco) / 1024  # KB
        print(f"\n📁 Arquivo: {banco}")
        print(f"📊 Tamanho: {tamanho:.2f} KB")
        
        # Verifica integridade
        print("\n🔍 Verificando integridade...")
        cursor.execute("PRAGMA integrity_check")
        integridade = cursor.fetchone()[0]
        
        if integridade == 'ok':
            print("✅ Integridade: OK")
        else:
            print(f"⚠️  Integridade: {integridade}")
        
        # Lista tabelas
        print("\n📋 TABELAS DO BANCO:")
        print("-" * 70)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tabelas = cursor.fetchall()
        
        if not tabelas:
            print("❌ Nenhuma tabela encontrada!")
            return False
        
        for i, (tabela,) in enumerate(tabelas, 1):
            print(f"{i}. {tabela}")
        
        # Verifica tabela USERS
        print("\n👥 USUÁRIOS:")
        print("-" * 70)
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            total_usuarios = cursor.fetchone()[0]
            print(f"Total de usuários: {total_usuarios}")
            
            cursor.execute("SELECT username, role FROM users")
            usuarios = cursor.fetchall()
            for usuario, role in usuarios:
                print(f"  - {usuario} ({role})")
        except Exception as e:
            print(f"❌ Erro ao verificar usuários: {str(e)}")
        
        # Verifica tabela EQUIPMENTS
        print("\n📦 EQUIPAMENTOS:")
        print("-" * 70)
        try:
            cursor.execute("SELECT COUNT(*) FROM equipments")
            total_equipamentos = cursor.fetchone()[0]
            print(f"Total de equipamentos: {total_equipamentos}")
            
            # Estatísticas por tipo
            cursor.execute("SELECT tipo, COUNT(*), SUM(quantidade) FROM equipments GROUP BY tipo")
            stats = cursor.fetchall()
            
            if stats:
                print("\nEstatísticas por tipo:")
                for tipo, count, total_qtd in stats:
                    print(f"  - {tipo}: {count} registro(s), {total_qtd if total_qtd else 0} unidade(s)")
            
            # Últimos 5 equipamentos adicionados
            cursor.execute("""
                SELECT codigo, nome, tipo, quantidade, data_adicao 
                FROM equipments 
                ORDER BY id DESC 
                LIMIT 5
            """)
            ultimos = cursor.fetchall()
            
            if ultimos:
                print("\nÚltimos equipamentos cadastrados:")
                for codigo, nome, tipo, qtd, data in ultimos:
                    data_formatada = data if data else 'N/A'
                    print(f"  - {codigo}: {nome} ({tipo}) - Qtd: {qtd} - Data: {data_formatada}")
        
        except Exception as e:
            print(f"❌ Erro ao verificar equipamentos: {str(e)}")
        
        # Estrutura da tabela equipments
        print("\n🗃️  ESTRUTURA DA TABELA EQUIPMENTS:")
        print("-" * 70)
        try:
            cursor.execute("PRAGMA table_info(equipments)")
            colunas = cursor.fetchall()
            
            print(f"{'ID':<5} {'Nome':<25} {'Tipo':<15} {'Not Null':<10} {'Default':<15}")
            print("-" * 70)
            for col in colunas:
                col_id, nome, tipo, notnull, default, pk = col
                notnull_str = "SIM" if notnull else "NÃO"
                default_str = str(default) if default else "-"
                print(f"{col_id:<5} {nome:<25} {tipo:<15} {notnull_str:<10} {default_str:<15}")
        
        except Exception as e:
            print(f"❌ Erro ao verificar estrutura: {str(e)}")
        
        # Fecha conexão
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70 + "\n")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao conectar ao banco: {str(e)}")
        return False


def verificar_migracao():
    """Verifica se todas as colunas necessárias existem"""
    banco = 'estoque.db'
    
    if not os.path.exists(banco):
        print("❌ Banco não encontrado")
        return
    
    try:
        conn = sqlite3.connect(banco)
        cursor = conn.cursor()
        
        print("\n🔄 VERIFICAÇÃO DE MIGRATIONS:")
        print("-" * 70)
        
        cursor.execute("PRAGMA table_info(equipments)")
        colunas = [col[1] for col in cursor.fetchall()]
        
        colunas_necessarias = ['id', 'codigo', 'nome', 'tipo', 'quantidade', 'data_adicao', 'ultima_atualizacao']
        
        for coluna in colunas_necessarias:
            if coluna in colunas:
                print(f"✅ Coluna '{coluna}' existe")
            else:
                print(f"❌ Coluna '{coluna}' NÃO existe")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")


if __name__ == "__main__":
    print("\n🔧 SISTEMA DE VERIFICAÇÃO - ESTOQUE")
    
    # Verifica banco
    sucesso = verificar_banco()
    
    if sucesso:
        # Verifica migrations
        verificar_migracao()
        
        print("\n💡 RECOMENDAÇÕES:")
        print("   1. Faça backup regularmente usando: python backup.py")
        print("   2. Execute esta verificação mensalmente")
        print("   3. Monitore o tamanho do banco de dados")
    
    print()



