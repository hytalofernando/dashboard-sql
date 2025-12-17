import sqlite3
import os

def corrigir_banco():
    """Corrige a constraint UNIQUE do campo codigo"""
    
    banco = 'estoque.db'
    
    if not os.path.exists(banco):
        print("Banco de dados nao encontrado!")
        return False
    
    print("\n" + "=" * 70)
    print("CORRECAO DA CONSTRAINT UNIQUE")
    print("=" * 70)
    
    try:
        conn = sqlite3.connect(banco)
        cursor = conn.cursor()
        
        # Verifica estrutura atual
        print("\n1. Verificando estrutura atual...")
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='equipments'")
        table_sql = cursor.fetchone()
        
        if table_sql:
            print("\nEstrutura atual:")
            print(table_sql[0])
            
            if 'UNIQUE' in table_sql[0].upper() and 'CODIGO' in table_sql[0].upper():
                print("\nPROBLEMA DETECTADO: Campo 'codigo' tem constraint UNIQUE")
                print("Iniciando correcao...\n")
                
                # Faz backup dos dados
                print("2. Fazendo backup dos dados...")
                cursor.execute("SELECT * FROM equipments")
                dados = cursor.fetchall()
                print(f"OK - {len(dados)} registro(s) copiado(s)")
                
                # Cria nova tabela sem UNIQUE
                print("\n3. Criando nova estrutura...")
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
                print("OK - Nova tabela criada")
                
                # Copia dados
                print("\n4. Copiando dados para nova estrutura...")
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
                print(f"OK - {cursor.rowcount} registro(s) copiado(s)")
                
                # Remove tabela antiga
                print("\n5. Removendo tabela antiga...")
                cursor.execute("DROP TABLE equipments")
                print("OK - Tabela antiga removida")
                
                # Renomeia nova tabela
                print("\n6. Renomeando nova tabela...")
                cursor.execute("ALTER TABLE equipments_new RENAME TO equipments")
                print("OK - Tabela renomeada")
                
                # Cria índice
                print("\n7. Criando indice (nao-unico)...")
                cursor.execute("CREATE INDEX IF NOT EXISTS ix_equipments_codigo ON equipments (codigo)")
                print("OK - Indice criado")
                
                # Commit
                conn.commit()
                
                # Verifica nova estrutura
                print("\n8. Verificando nova estrutura...")
                cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='equipments'")
                new_table_sql = cursor.fetchone()
                print("\nNova estrutura:")
                print(new_table_sql[0])
                
                # Verifica dados
                print("\n9. Verificando dados...")
                cursor.execute("SELECT COUNT(*) FROM equipments")
                total = cursor.fetchone()[0]
                print(f"OK - Total de registros: {total}")
                
                print("\n" + "=" * 70)
                print("CORRECAO CONCLUIDA COM SUCESSO!")
                print("=" * 70)
                print("\nAgora voce pode adicionar o mesmo codigo com tipos diferentes!")
                print("Exemplo: EQ001 NOVO e EQ001 USADO sao permitidos.\n")
                
                return True
            else:
                print("\nBanco ja esta correto! Nao ha constraint UNIQUE no campo codigo.")
                return True
        else:
            print("Tabela 'equipments' nao encontrada!")
            return False
            
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    print("\nSCRIPT DE CORRECAO DO BANCO DE DADOS")
    corrigir_banco()
    input("\nPressione ENTER para sair...")


