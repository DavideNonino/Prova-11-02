from pymavlink import mavutil
import connect

mode_dict = {
    0: 'STABILIZE', 
    1: 'ACRO', 
    2: 'ALT_HOLD', 
    3: 'AUTO', 
    4: 'GUIDED', 
    5: 'LOITER', 
    6: 'RTL', 
    7: 'CIRCLE', 
    9: 'LAND', 
    11: 'DRIFT', 
    13: 'SPORT', 
    14: 'FLIP', 
    15: 'AUTOTUNE', 
    16: 'POSHOLD', 
    17: 'BRAKE', 
    18: 'THROW', 
    19: 'AVOID_ADSB', 
    20: 'GUIDED_NOGPS', 
    21: 'SMART_RTL', 
    22: 'FLOWHOLD', 
    23: 'FOLLOW', 
    24: 'ZIGZAG', 
    25: 'SYSTEMID', 
    26: 'AUTOROTATE', 
    27: 'AUTO_RTL', 
    28: 'TURTLE'
    }

def set_mode(the_connection, mode):
    if mode not in the_connection.mode_mapping():
            print(f'Modalità sconosciuta : {mode}')
            print(f"Modalità disponibili: {list(the_connection.mode_mapping().keys())}")
            return

    print(f"Cambio modalità in {mode}")

    try:
        mode_id = the_connection.mode_mapping()[mode]
    
        the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_DO_SET_MODE,
                                0, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode_id, 0, 0, 0, 0, 0)
        print("attesa ACK...")
        ack_msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=10)
        #print(ack_msg)
        if ack_msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
            print(f"modalità cambiata in {mode}")
            print(ack_msg)
        else:
            print("Errore, ACK non ricevuto")
    
    except Exception as e:
        print(f"Errore durante il cambio di modalità: {e}")
        return

def get_mode(the_connection):
    heartbeat = the_connection.recv_match(type='HEARTBEAT', blocking=True)
    
    # Estrai la modalità corrente dal messaggio HEARTBEAT
    mode = heartbeat.custom_mode
    autopilot = heartbeat.autopilot
    print(f"modalità attuale: {mode_dict[mode]}")
    return mode_dict[mode]

if __name__ == "__main__":
    
    the_connection = connect.connect('udpin:127.0.0.1:5760',10)
    set_mode( the_connection, "AUTO" )
    get_mode(the_connection)
