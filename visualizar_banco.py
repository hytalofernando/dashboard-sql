#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Visualizar Informações do Banco de Dados
Mostra localização, tamanho e conteúdo do banco
"""

import os
import sqlite3
from datetime import datetime
from database import engine, DATABASE_URL

def visualizar_info_banco():
    """Mostra informações sobre o banco de dados"""
    
    print("\n" + "=" * 70)
    print("INFORMACOES DO BANCO DE DADOS")
    print("=" * 70)
    
    # Informações de conexão
    print(f"\nURL de Conexao: {DATABASE_URL}")
    
    # Extrai o caminho do arquivo do DATABASE_URL
    if "sqlite:///" in DATABASE_URL:
        db_path = DATABASE_URL.replace("sqlite:///", "")
        # Remove ./ se existir
        db_path = db_path.replace("./", "")
        
        # Se não tiver caminho absoluto, usa o diretório atual
        if not os.path.isabs(db_path):
            db_path = os.path.join(os.getcwd(), db_path)
        
        print(f"\nCaminho Completo do Banco: {db_path}")
        
        # Verifica se o arquivo existe
        if os.path.exists(db_path):
            print(f"Status do Arquivo: EXISTE")
            
            # Tamanho do arquivo
            tamanho_bytes = os.path.getsize(db_path)
            tamanho_kb = tamanho_bytes / 1024
            print(f"Tamanho do Arquivo: {tamanho_kb:.2f} KB ({tamanho_bytes} bytes)")
            
            # Data de criação/modificação
            data_modificacao = datetime.fromtimestamp(os.path.getmtime(db_path))
            print(f"Ultima Modificacao: {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
            
            # Conecta e verifica conteúdo
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                print("\n" + "=" * 70)
                print("CONTEUDO DO BANCO")
                print("=" * 70)
                
                # Usuários
                cursor.execute("SELECT COUNT(*) FROM users")
                total_usuarios = cursor.fetchone()[0]
                print(f"\nTotal de Usuarios: {total_usuarios}")
                
                cursor.execute("SELECT username, role FROM users")
                usuarios = cursor.fetchall()
                for username, role in usuarios:
                    print(f"  - {username} ({role})")
                
                # Equipamentos
                cursor.execute("SELECT COUNT(*) FROM equipments")
                total_equipamentos = cursor.fetchone()[0]
                print(f"\nTotal de Equipamentos: {total_equipamentos}")
                
                if total_equipamentos > 0:
                    cursor.execute("""
                        SELECT codigo, nome, tipo, quantidade 
                        FROM equipments 
                        ORDER BY id
                    """)
                    equipamentos = cursor.fetchall()
                    
                    print("\nLista de Equipamentos:")
                    print("-" * 70)
                    for codigo, nome, tipo, qtd in equipamentos:
                        print(f"  Codigo: {codigo:<10} | Nome: {nome:<30} | Tipo: {tipo:<6} | Qtd: {qtd}")
                
                # Estatísticas
                print("\n" + "=" * 70)
                print("ESTATISTICAS")
                print("=" * 70)
                
                cursor.execute("SELECT tipo, COUNT(*), SUM(quantidade) FROM equipments GROUP BY tipo")
                stats = cursor.fetchall()
                
                for tipo, count, total_qtd in stats:
                    print(f"\n{tipo}:")
                    print(f"  - Registros: {count}")
                    print(f"  - Quantidade Total: {total_qtd if total_qtd else 0}")
                
                conn.close()
                
            except Exception as e:
                print(f"\nErro ao ler banco: {str(e)}")
        else:
            print(f"Status do Arquivo: NAO EXISTE")
            print(f"O banco sera criado na primeira execucao do sistema")
    else:
        print(f"\nTipo de Banco: PostgreSQL ou outro (nao SQLite)")
        print(f"Os dados estao armazenados no servidor externo configurado")
    
    print("\n" + "=" * 70)
    print("FIM DA VISUALIZACAO")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    visualizar_info_banco()


