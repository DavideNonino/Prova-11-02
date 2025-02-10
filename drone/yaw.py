import time
import math
import connect
from pymavlink import mavutil


def set_yaw( the_connection, yaw: float, yaw_speed: float = 10, direction: int = 0, abs_rel: int = 1 ): # direction: 1 senso orario e -1 per l'antiorario
    
    try:
        
        the_connection.mav.command_long_send(
            the_connection.target_system,
            the_connection.target_component,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,0,yaw,yaw_speed,direction,abs_rel,0,0,0
        )


        print(f"Comando inviato con angolo YAW:{yaw}° e velocità: {yaw_speed}")
        
        set_yaw_ack = the_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=10)
        if set_yaw_ack:
            print(f"Set Yaw ACK:  {set_yaw_ack}")

        else:
            print("Errore, YAW ACK non ricevuto")

        
    except Exception as e:
        print(f"Errore nell'invio del comando di YAW:{e}")


if __name__ == "__main__":
    the_connection = connect.connect('udpin:127.0.0.1:5760',10)
    set_yaw(the_connection,270)