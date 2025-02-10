from pymavlink import mavutil
import connect
import mode
import time 

mode_en = ['STABILIZE','GUIDED','ACRO','ALT_HOLD','LOITER','POSHOLD']

armed = False

def arm(the_connection):
    mode_act = mode.get_mode(the_connection)
    
    global armed
    armed = False

    if not check_if_arm(the_connection):
        if mode_act in mode_en:
            print("Armo il drone...")

            try:
                the_connection.mav.command_long_send(
                    the_connection.target_system,
                    the_connection.target_component,
                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                    0,
                    1,   #arma il drone 
                    0, 0, 0, 0, 0, 0
                )
        
                msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=10 )
                if msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                    print("Drone armato!!")
                    print(msg)
                    armed = True
                else:
                    print("Errore, ACK non ricevuto")
                    
            except Exception as e:
                print(f"Errore durante l'armamento drone: {e}")
        else:
            print("Cambiare modalità di volo per armare il drone")
            return 
    else:
        print("Drone già armato!!")

def disarm(the_connection):
    mode_act = mode.get_mode(the_connection)
    
    global armed
    

    if check_if_arm(the_connection):
        if mode_act in mode_en:
            print("DIsarmo il drone...")

            try:
                the_connection.mav.command_long_send(
                    the_connection.target_system,
                    the_connection.target_component,
                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                    0,
                    0,   #disarma il drone 
                    0, 0, 0, 0, 0, 0
                )
        
                msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=10 )
                if msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                    print("Drone disarmato!!")
                    armed = False
                else:
                    print("Errore, ACK non ricevuto")
                    
            except Exception as e:
                print(f"Errore durante il disarmo del drone: {e}")
        else:
            print("Cambiare modalità di volo per disarmare il drone")
            return 
    else:
        print("Drone già disarmato!!")

def check_if_arm(the_connection):
    msg = the_connection.recv_match(type = 'HEARTBEAT',blocking = True)
    if msg:
        system_status = msg.system_status
        if system_status == mavutil.mavlink.MAV_STATE_ACTIVE or armed:
            return True
    
    return False


if __name__ == "__main__":
    the_connection = connect.connect('udpin:127.0.0.1:5760',10)
    arm( the_connection )


