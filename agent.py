import json
import re  # Přidáváme regulární výrazy na čištění textu
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def scitej_cisla(a, b):
    print(f"  [NÁSTROJ V AKCI]: Python právě sčítá {a} + {b}")
    return a + b

# Zpřísněný prompt – model má zakázáno psát cokoliv kromě JSONu
SYSTEM_PROMPT = """
Jsi užitečný AI agent. Máš k dispozici jeden nástroj pro sčítání čísel: 'scitej_cisla'.

Pokud ti uživatel zadá úkol na sčítání, tvá odpověď MUSÍ být POUZE čistý JSON objekt a nic jiného. 
Napiš POUZE JSON, žádný text před ním, žádný text po něm.

Formát JSONu:
{
    "action": "scitej_cisla",
    "parameters": {"a": 5, "b": 10}
}

Pokud již máš v historii všechny podklady a znáš konečný výsledek, tvá odpověď NESMÍ být JSON. 
V tom případě napiš lidskou řečí finální odpověď pro uživatele (např. Výsledek je 42).
"""

def vycisti_a_najdi_json(text):
    """Pomocná funkce, která najde JSON v textu, i když model psal kecy okolo."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    return text

def spust_agenta(vstup_uzivatele):
    print(f"Uživatel: {vstup_uzivatele}\n")
    print("🤖 START AGENTNÍ SMYČKY 🤖\n")
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": vstup_uzivatele}
    ]
    
    kolo = 1
    while True:
        print(f"--- KOLO {kolo} ---")
        response = client.chat.completions.create(
            model="llama3",
            messages=messages,
            temperature=0  # Nula zaručuje nejvyšší možnou stabilitu a logiku
        )
        
        odpoved_llm = response.choices[0].message.content
        print(f"Agent (Surová odpověď z LLM):\n{odpoved_llm}\n")
        
        # Pokusíme se z textu vytáhnout pouze JSON
        cisty_json_text = vycisti_a_najdi_json(odpoved_llm)
        
        try:
            data = json.loads(cisty_json_text)
            
            if data.get("action") == "scitej_cisla":
                params = data.get("parameters", {})
                
                # Spuštění našeho Python kódu
                vysledek_nastroje = scitej_cisla(params["a"], params["b"])
                print(f"  [VÝSLEDEK Z PYTHONU]: {vysledek_nastroje}")
                
                # Uložíme krok do paměti agenta
                messages.append({"role": "assistant", "content": odpoved_llm})
                messages.append({"role": "user", "content": f"Výsledek nástroje: {vysledek_nastroje}"})
                
                print("  [INFO]: Posílám výsledek zpět modelu do dalšího kola.\n")
                kolo += 1
                continue
                
        except json.JSONDecodeError:
            # Pokud to nebyl JSON ani po vyčištění, je to finální text pro uživatele
            print(f"🎉 Agent (Finální odpověď uživateli): {odpoved_llm}")
            break

# Spuštění testu se třemi čísly
spust_agenta("Tak schvalne. Kolik je 2548 + 7452 + 56?")
