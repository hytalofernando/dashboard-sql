import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

print("\n=== INDICES DA TABELA EQUIPMENTS ===\n")

cursor.execute("PRAGMA index_list(equipments)")
indices = cursor.fetchall()

if not indices:
    print("Nenhum indice encontrado")
else:
    for idx in indices:
        print(f"Nome: {idx[1]}, Unique: {idx[2]}")
        cursor.execute(f"PRAGMA index_info({idx[1]})")
        info = cursor.fetchall()
        for col in info:
            print(f"  - Coluna: {col[2]}")

print("\n=== ESTRUTURA DA TABELA ===\n")
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='equipments'")
print(cursor.fetchone()[0])

conn.close()


