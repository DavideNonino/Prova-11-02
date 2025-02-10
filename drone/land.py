import connect
import math
from pymavlink import mavutil


def land( the_connection ):

    try:
            the_connection.mav.command_long_send(
                the_connection.target_system,  # ID del sistema
                the_connection.target_component,  # ID del componente
                mavutil.mavlink.MAV_CMD_NAV_LAND,  # Comando per atterrare
                0,  # Attendi conferma
                0,  # Parametro1: Tipo di allineamento
                0,  # Parametro2: Coordinate (X, Y, Z)
                0,  # Parametro3: Distanza di atterraggio
                0,  # Parametro4: Velocità di atterraggio
                0,  # Parametro5: Angolo di pitch
                0,  # Parametro6: Angolo di roll
                0   # Parametro7: Angolo di yaw
            )

            msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=10)
            if msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                print("Sequenza di atterraggio iniziata!!")
    
    except Exception as e:
        print(f"Errore durante l'atterraggio: {e}")


if __name__ == "__main__":
    the_connection = connect.connect('udpin:127.0.0.1:5760',10)
    land( the_connection )