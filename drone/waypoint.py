from pymavlink import mavutil
import connect
import mode
import arm
import time
import math
import json
import connect

mode_en = ["AUTO", "GUIDED", "RTL"]

# Funzione per leggere e convertire il file di missione da TXT a JSON
def convert_mission_txt_to_json(txt_file, json_file):
    mission_items = []

    # Apri il file TXT per leggere le righe
    with open(txt_file, 'r') as file:
        for line in file:
            # Rimuovi spazi bianchi extra e salta le righe vuote
            if not line or "seq" in line:
                continue
            
            # Estrai i valori separati da virgola
            parts = line.split()
            if len(parts) < 8:
                continue  # Salta le righe con formato errato
            # Mappa i valori nel formato richiesto
            mission_item = {
                'seq': int(parts[0]),  # Sequenza
                'frame': int(parts[2]),  # Imposta il tipo di coordinate come MAV_FRAME_GLOBAL_RELATIVE_ALT
                'command': int(parts[3]),  # Tipo di comando (es. 16 per waypoint)
                'current': 1 if int(parts[0]) == 0 else 0,  # Il primo waypoint è il "current"
                'autocontinue': int(parts[11]),  # Imposta l'auto-continuazione
                'x': float(parts[8]),  # Latitudine
                'y': float(parts[9]),  # Longitudine
                'z': float(parts[10]),   # Altitudine
                'p1': float(parts[4]),   #parametri aggiuntivi
                'p2': float(parts[5]),
                'p3': float(parts[6]),
                'p4': float(parts[7])
            }
            mission_items.append(mission_item)

    # Scrivi il risultato in un file JSON
    with open(json_file, 'w') as output_file:
        json.dump({"mission_items": mission_items}, output_file, indent=4)

    print(f"Missione convertita e salvata in {json_file}")


# chiamata missione
def mission(the_connection, json_fl):
    with open(json_fl,'r') as file:
        data = json.load(file)

    print(data)
    upload_mission(the_connection,data["mission_items"])


# caricamento missione

def upload_mission(the_connection, mission_items):

    act_mode = mode.get_mode(the_connection)

    if act_mode in mode_en:
    
        mission_items_count = len(mission_items)
    
        if mission_items_count > 0:

            print(f"invio di {mission_items_count} elementi")

            try:
                the_connection.mav.mission_count_send(
                    the_connection.target_system,
                    the_connection.target_component,
                    mission_items_count
                )

                msg = the_connection.recv_match(type='MISSION_REQUEST', blocking=True, timeout=10)
                print(msg)
            except Exception as e:
                print(f"Errore: {e}")
            
            if msg:
                for item in mission_items:
                    the_connection.mav.mission_item_send(
                        the_connection.target_system,
                        the_connection.target_component,
                        item['seq'],
                        item['frame'],
                        item['command'],
                        item['current'],
                        item['autocontinue'],
                        item['p1'],
                        item['p2'],
                        item['p3'],
                        item['p4'],
                        item['x'],
                        item['y'],
                        item['z'],
                    )
                    if item['seq'] != mission_items_count-1:
                        msg_item = the_connection.recv_match(type='MISSION_REQUEST', blocking=True, timeout=10)
                        print(msg_item)
                    else:
                        ack = the_connection.recv_match(type='MISSION_ACK', blocking=True, timeout=10)
                        print(ack)
    else:
        print("La modalità attuale non permette il caricamento della missione")   

def clear_mission( the_connection ):
    
    try:
        the_connection.mav.mission_clear_all_send(
            the_connection.target_system,
            the_connection.target_component
        )

        msg_ack = the_connection.recv_match(type='MISSION_ACK', blocking=True, timeout=10)
        if msg_ack:
            if msg_ack.type == 0:
                print("Missione cancellata!!")
            else:
                print("Missione NON cancellata!!")
        else:
            print("Errore nella ricezione dell'ACK") 
    except Exception as e:
        print(f"Errore nella cancellazione della missione: {e}")

# Esegui la conversione (specifica il percorso del file di input e di output)
the_connection = connect.connect('udpin:127.0.0.1:5760',10)
convert_mission_txt_to_json('rally-items.txt', 'converted_mission.json')
mission(the_connection, 'converted_mission.json')
clear_mission(the_connection)
