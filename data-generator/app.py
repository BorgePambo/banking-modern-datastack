import time
import psycopg2
from decimal import Decimal, ROUND_DOWN
from faker import Faker
import random
import argparse
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Configuração do projeto
# -----------------------------
NUM_VENDAS = 50  # número de registros por iteração
PRECO_MIN = Decimal("5.00")
PRECO_MAX = Decimal("500.00")
QUANTIDADE_MIN = 1
QUANTIDADE_MAX = 10
REGIOES = ["Norte", "Sul", "Leste", "Oeste", "Centro"]

# Loop config
DEFAULT_LOOP = True
SLEEP_SECONDS = 2

# CLI override
parser = argparse.ArgumentParser(description="Gerador de dados de vendas")
parser.add_argument("--once", action="store_true", help="Executa uma vez e sai")
args = parser.parse_args()
LOOP = not args.once and DEFAULT_LOOP

# -----------------------------
# Helpers
# -----------------------------
fake = Faker()

def random_money(min_val: Decimal, max_val: Decimal) -> Decimal:
    val = Decimal(str(random.uniform(float(min_val), float(max_val))))
    return val.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

def random_quantity(min_val: int, max_val: int) -> int:
    return random.randint(min_val, max_val)

# -----------------------------
# Conexão com PostgreSQL
# -----------------------------
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)
conn.autocommit = True
cur = conn.cursor()

# -----------------------------
# Geração de dados (uma iteração)
# -----------------------------
def run_iteration():
    for _ in range(NUM_VENDAS):
        data_venda = fake.date_this_year()
        cliente = fake.name()
        produto = fake.word().capitalize()
        preco = random_money(PRECO_MIN, PRECO_MAX)
        quantidade = random_quantity(QUANTIDADE_MIN, QUANTIDADE_MAX)
        regiao = random.choice(REGIOES)

        cur.execute(
            """
            INSERT INTO vendas (data_venda, cliente, produto, preco, quantidade, regiao)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data_venda, cliente, produto, preco, quantidade, regiao),
        )

    print(f"✅ Geradas {NUM_VENDAS} vendas.")

# -----------------------------
# Loop principal
# -----------------------------
try:
    iteration = 0
    while True:
        iteration += 1
        print(f"\n--- Iteração {iteration} iniciada ---")
        run_iteration()
        print(f"--- Iteração {iteration} finalizada ---")
        if not LOOP:
            break
        time.sleep(SLEEP_SECONDS)

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário. Saindo...")

finally:
    cur.close()
    conn.close()
    sys.exit(0)
