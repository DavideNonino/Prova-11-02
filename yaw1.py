import time
import math
import connect
from pymavlink import mavutil


def target( the_connection, yaw ):
    try:
	    att = the_connection.recv_match(type='ATTITUDE',blocking =True,timeout=10)
	    act_yaw = att.yaw * 180 / 3.14159265 
	    target_yaw = calculate_yaw (act_yaw, yaw)
	    return target_yaw
    except Exception as e:
	    print(f"Errore durante il calcolo del target: {e}")

def calculate_yaw( act_yaw, yaw):
    if act_yaw >= 0:
	    target_y = act_yaw + yaw
    else: 
	    target_y = act_yaw - yaw

    if target_y > 180:
	    target_y = (target_y - 180) * (-1)
    elif target_y < -180:
	    target_y = (target_y + 180) * (-1)
    return target_y

def set_yaw( the_connection, yaw: float, yaw_speed: float = 10, direction: int = 0, abs_rel: int = 1 ): # direction: 1 senso orario e -1 per l'antiorario
    yaw_target = int(target(the_connection,yaw))   
    print(yaw_target)
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
            while True:
                # Ricevi i dati di attitudine
                msg = the_connection.recv_match(type='ATTITUDE', blocking=True, timeout=10)
                
                # Ottieni il valore di yaw (in radianti, quindi convertilo in gradi)
                current_yaw = int(msg.yaw * 180 / 3.14159265)  # Converti da radianti a gradi
                
                print(current_yaw)
                if current_yaw == yaw_target:
                    print("Yaw raggiunto")
                    break
                
                

        else:
            print("Errore, YAW ACK non ricevuto")

        
    except Exception as e:
        print(f"Errore nell'invio del comando di YAW:{e}")


if __name__ == "__main__":
    the_connection = connect.connect('udpin:127.0.0.1:14550',10)
    set_yaw(the_connection,90)
