import serial

# Configuration de la communication série
comport = 'COM6'  # Remplacez par le port correct
baudrate = 9600
ser = serial.Serial(comport, baudrate, timeout=1)

# Dictionnaire pour stocker l'état des LEDs
led_pins = {
    1: 'd:13:o',
    2: 'd:12:o',
    3: 'd:11:o',
    4: 'd:10:o',
    5: 'd:9:o'
}

# Fonction pour mettre à jour les LEDs en fonction du nombre total de doigts
def update_leds(total):
    for i in range(1, 6):
        if i <= total:
            # Activer la LED correspondante
            ser.write(f"{led_pins[i]}=1\n".encode())
        else:
            # Désactiver la LED correspondante
            ser.write(f"{led_pins[i]}=0\n".encode())

try:
    while True:
        if ser.in_waiting > 0:
            # Lire la valeur envoyée par le script principal en mode binaire
            line = ser.readline()
            print(f"Raw data received: {line}")  # Affiche les données brutes pour débogage
            try:
                # Convertir les octets en chaîne de caractères en utilisant l'encodage ASCII
                line = line.decode('ascii').strip()
                total = int(line)
                # Mettre à jour les LEDs en fonction du nombre total de doigts
                update_leds(total)
            except (ValueError, UnicodeDecodeError):
                print("Erreur de conversion ou de décodage : donnée invalide")
except KeyboardInterrupt:
    print("Interruption par l'utilisateur")
finally:
    ser.close()


