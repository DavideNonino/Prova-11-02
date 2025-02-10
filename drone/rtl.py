import connect
import math
from pymavlink import mavutil

def rtl( the_connection ):

    try:
        the_connection.mav.command_long_send(
            the_connection.target_system,
            the_connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
            0,
            0, 0, 0, 0, 0, 0, 0
        )

        msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=10)
        if msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
            print("Drone torna al punto di lancio!!")
    except Exception as e:
        print(f"Errore nel tornare al punto di lancio: {e}")


def set_home( the_connection, lat, long, alt):
    
    try:
        the_connection.mav.command_long_send(
            the_connection.target_system,  # ID del sistema
            the_connection.target_component,  # ID del componente
            mavutil.mavlink.MAV_CMD_DO_SET_HOME,  # Comando per impostare il punto di lancio
            0,  # Attendi conferma
            0, #usa location specifica
            0,
            0,
            0,
            lat*1e7,  # Parametro2: latitudine del nuovo punto di lancio
            long*1e7,  # Parametro3: longitudine del nuovo punto di lancio
            alt*1000  # Parametro4: altitudine del nuovo punto di lancio
        )

    except Exception as e:
        print(f"Errore nel tornare al punto di lancio: {e}")


if __name__ == "__main__":
    the_connection = connect.connect('udpin:127.0.0.1:5760',10)
    #rtl( the_connection )
    set_home(the_connection,45.9344232, 13.107989,100)