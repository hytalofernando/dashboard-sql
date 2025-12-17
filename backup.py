#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Backup Automático do Banco de Dados
Cria backups do banco de dados estoque.db com timestamp
"""

import shutil
import os
from datetime import datetime


def criar_backup():
    """Cria backup do banco de dados com timestamp"""
    
    # Nome do banco original
    banco_original = 'estoque.db'
    
    # Verifica se o banco existe
    if not os.path.exists(banco_original):
        print(f"❌ Erro: Banco de dados '{banco_original}' não encontrado!")
        print(f"   Certifique-se de estar na pasta do projeto.")
        return False
    
    # Cria pasta de backups se não existir
    pasta_backups = 'backups'
    if not os.path.exists(pasta_backups):
        os.makedirs(pasta_backups)
        print(f"📁 Pasta '{pasta_backups}' criada")
    
    # Nome do backup com data e hora
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_nome = f"{pasta_backups}/estoque_backup_{timestamp}.db"
    
    try:
        # Copia o banco
        shutil.copy2(banco_original, backup_nome)
        
        # Informações sobre o backup
        tamanho = os.path.getsize(backup_nome) / 1024  # KB
        
        print("=" * 60)
        print("✅ BACKUP CRIADO COM SUCESSO!")
        print("=" * 60)
        print(f"📁 Arquivo: {backup_nome}")
        print(f"📊 Tamanho: {tamanho:.2f} KB")
        print(f"🕐 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
        # Lista backups existentes
        listar_backups()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar backup: {str(e)}")
        return False


def listar_backups():
    """Lista todos os backups existentes"""
    pasta_backups = 'backups'
    
    if not os.path.exists(pasta_backups):
        print("\n📭 Nenhum backup encontrado")
        return
    
    backups = [f for f in os.listdir(pasta_backups) if f.endswith('.db')]
    
    if not backups:
        print("\n📭 Nenhum backup encontrado")
        return
    
    print("\n📚 BACKUPS EXISTENTES:")
    print("-" * 60)
    
    backups.sort(reverse=True)  # Mais recentes primeiro
    
    for i, backup in enumerate(backups, 1):
        caminho = os.path.join(pasta_backups, backup)
        tamanho = os.path.getsize(caminho) / 1024  # KB
        data_mod = datetime.fromtimestamp(os.path.getmtime(caminho))
        
        print(f"{i}. {backup}")
        print(f"   Tamanho: {tamanho:.2f} KB")
        print(f"   Data: {data_mod.strftime('%d/%m/%Y %H:%M:%S')}")
        print()


def limpar_backups_antigos(dias=30):
    """Remove backups mais antigos que X dias"""
    pasta_backups = 'backups'
    
    if not os.path.exists(pasta_backups):
        return
    
    from datetime import timedelta
    limite = datetime.now() - timedelta(days=dias)
    removidos = 0
    
    for arquivo in os.listdir(pasta_backups):
        if arquivo.endswith('.db'):
            caminho = os.path.join(pasta_backups, arquivo)
            data_arquivo = datetime.fromtimestamp(os.path.getmtime(caminho))
            
            if data_arquivo < limite:
                os.remove(caminho)
                removidos += 1
                print(f"🗑️  Backup antigo removido: {arquivo}")
    
    if removidos > 0:
        print(f"\n✅ {removidos} backup(s) antigo(s) removido(s)")


if __name__ == "__main__":
    print("\n🔧 SISTEMA DE BACKUP - ESTOQUE")
    print("=" * 60)
    
    # Cria backup
    sucesso = criar_backup()
    
    if sucesso:
        # Remove backups com mais de 30 dias (opcional)
        # Descomente a linha abaixo para ativar limpeza automática
        # limpar_backups_antigos(30)
        
        print("\n💡 DICA: Configure este script para rodar automaticamente!")
        print("   Use o Agendador de Tarefas do Windows para backups diários.")
    
    print()



