import json
from openai import OpenAI

# Připojení k lokálnímu LLM (např. Ollama běžící na portu 11434)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama klíč nevyžaduje, ale knihovna ho potřebuje vyplnit
)

# 1. Definice nástroje (Tool), který má agent k dispozici
def scitej_cisla(a, b):
    print(f"  [NÁSTROJ]: Spouštím kalkulačku pro {a} + {b}")
    return a + b

# 2. Systémový prompt, který definuje pravidla hry pro agenta
SYSTEM_PROMPT = """
Jsi užitečný AI agent. Máš k dispozici jeden nástroj pro sčítání čísel: 'scitej_cisla'.
Pokud ti uživatel zadá matematický úkol na sčítání, musíš odpovědět ve formátu JSON, abys zavolal tento nástroj.

Formát pro zavolání nástroje:
{
    "action": "scitej_cisla",
    "parameters": {"a": 5, "b": 10}
}

Jakmile dostaneš výsledek z nástroje, napiš uživateli finální odpověď.
"""

def spust_agenta(vstup_uzivatele):
    print(f"Uživatel: {vstup_uzivatele}\n")
    
    # Historie konverzace, kterou agentovi posíláme
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": vstup_uzivatele}
    ]
    
    # --- KROK 1: Uvažování agenta a rozhodnutí o akci ---
    response = client.chat.completions.create(
        model="llama3", # Nahraďte modelem, který máte stažený v Ollama
        messages=messages,
        temperature=0
    )
    
    odpoved_llm = response.choices[0].message.content
    print(f"Agent (Myšlení): {odpoved_llm}\n")
    
    # --- KROK 2: Analýza odpovědi a spuštění nástroje (Execution) ---
    try:
        # Zkusíme, zda agent vrátil JSON pro zavolání nástroje
        data = json.loads(odpoved_llm)
        if data.get("action") == "scitej_cisla":
            params = data.get("parameters", {})
            
            # Spuštění reálné Python funkce
            vysledek_nastroje = scitej_cisla(params["a"], params["b"])
            
            # Přidáme výsledek do historie pro agenta (Pozorování)
            messages.append({"role": "assistant", "content": odpoved_llm})
            messages.append({"role": "user", "content": f"Výsledek nástroje: {vysledek_nastroje}"})
            
            # --- KROK 3: Finální odpověď uživateli ---
            final_response = client.chat.completions.create(
                model="llama3",
                messages=messages,
                temperature=0
            )
            print(f"\nAgent (Finální odpověď): {final_response.choices[0].message.content}")
            
    except json.JSONDecodeError:
        # Pokud agent nevrátil JSON, znamená to, že rovnou odpověděl textem
        print(f"Agent (Přímá odpověď): {odpoved_llm}")

# Spuštění testu
spust_agenta("Kolik je 2548 + 7452?")
