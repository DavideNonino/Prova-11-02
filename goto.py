from pymavlink import mavutil
import connect
import mode
import arm
import takeoff
import time
import math

mode_en = ['GUIDED','AUTO']

def goto(the_connection, lat, lon, alt):
     
    mode_act = mode.get_mode(the_connection)
    
    if mode_act in mode_en:
        if arm.check_if_arm(the_connection):
            print("Eseguo il movimento...")

            try:
                the_connection.mav.set_position_target_global_int_send(
                    0,  # Tempo di sistema in secondi (di solito 0)
                    the_connection.target_system,   # ID del veicolo (di solito 0 per il primo drone)
                    0, # Sistema di riferimento (0 per la Terra)
                    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,  # Sistema di riferimento (altitudine relativa alla posizione di casa)
                    0b110111111000,  # Tipo di parametri di movimento (posizione e velocità)
                    int(lat * 1e7),  # Latitudine in 1E7
                    int(lon * 1e7),  # Longitudine in 1E7
                    alt,  # Altitudine in millimetri
                    0,        # Velocità lungo X (cm/s)
                    0,        # Velocità lungo Y (cm/s)
                    0,        # Velocità lungo Z (cm/s)
                    0,               
                    0,
                    0,
                    0,
                    0
                )

                time.sleep(5)

                print(f"Comando inviato per spostare il drone a ({lat}, {lon}) con altitudine {alt}m.")

                while True:
                    msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
                    if msg:
                        current_lat = msg.lat / 10**7
                        current_lon = msg.lon / 10**7
                        current_alt = msg.relative_alt / 1000
                        print(f"Posizione attuale: lat={current_lat}, lon={current_lon}, alt={current_alt}")

                        if is_at_target(current_lat,current_lon,lat,lon):
                            print("Posizione raggiunta con successo!!")
                            break

            except Exception as e:
                print(f"Errore durante il movimento: {e}")

        else:
            print("Errore, armare il drone prima di muovere il drone!!")    

    else:
        print("La modalità di volo attuale non consente il movimento del drone")

# Funzione per calcolare la distanza tra due coordinate geografiche (in metri)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Raggio della Terra in metri
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distanza in metri

def is_at_target(current_lat, current_lon, target_lat, target_lon, threshold=1.0):
    dist = haversine(current_lat, current_lon, target_lat, target_lon)
    return dist <= threshold



if __name__ == "__main__":
    the_connection = connect.connect('udpin:127.0.0.1:5760',10)
    goto(the_connection, 45.935230, 13.108997, 20 )