def kalkulacka():
    print("=== Kalkulačka ===")
    print("Operace: +, -, *, /")
    
    while True:
        try:
            a = float(input("První číslo: "))
            op = input("Operace (+, -, *, /): ")
            b = float(input("Druhé číslo: "))
            
            if op == "+":
                print(f"Výsledek: {a + b}")
            elif op == "-":
                print(f"Výsledek: {a - b}")
            elif op == "*":
                print(f"Výsledek: {a * b}")
            elif op == "/":
                if b == 0:
                    print("Nelze dělit nulou!")
                else:
                    print(f"Výsledek: {a / b}")
            else:
                print("Neznámá operace")
                
        except ValueError:
            print("Zadej platné číslo")
            
        dalsi = input("Počítat dál? (a/n): ")
        if dalsi.lower() == "n":
            break

kalkulacka()

