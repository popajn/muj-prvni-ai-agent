#!/bin/bash
# Toto je "shebang" - říká systému, že má použít Bash

SERVERY=("google.com" "seznam.cz" "idnes.cz")

for SERVER in "${SERVERY[@]}"
do
    echo "Kontroluji server: $SERVER"
    # Vytáhneme jen řádek s názvem serveru z hlavičky
    curl -I -s "https://$SERVER" | grep -i "Server"
    echo "--------------------------"
done
