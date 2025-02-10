from pymavlink import mavutil
import connect
import mode
import arm
import takeoff
import time
import math

mode_en = ['GUIDED','AUTO']

def moveXYZ(the_connection, x = 0, y = 0, z = 0, vx = 0, vy = 0, vz = 0):
     
    mode_act = mode.get_mode(the_connection)
    
    if mode_act in mode_en:
        if arm.check_if_arm(the_connection):
            print("Eseguo il movimento...")
            
            pos = act_pos( the_connection )
            target_pos = [pos[0] + x, pos[1] + y, pos[2] + z]

            try:

                the_connection.mav.set_position_target_local_ned_send(
                    0,  # Time boot ms
                    the_connection.target_system,  # System ID
                    the_connection.target_component,  # Component ID
                    mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,  # NED frame 
                    0b110000000000 ,  # Flags (posizione 3D e velocità)
                    x, y, z,  # Posizione target X=distance, Y=0, Z=0
                    vx,vy,vz,  # Velocità (0 in X, Y, Z)
                    0, 0, 0,   # Acceleration (opzionale)
                    0,0 #Yaw
                )
                print(f"Comando inviato per spostare il drone.")


            
            except Exception as e:
                print(f"Errore durante il movimento: {e}")

        else:
            print("Errore, armare il drone prima di muoverlo!!")    

    else:
        print("La modalità di volo attuale non consente il movimento del drone")


def moveNED(the_connection, x = 0, y = 0, z = 0,vx = 0, vy = 0, vz = 0):
     
    mode_act = mode.get_mode(the_connection)
    
    if mode_act in mode_en:
        if arm.check_if_arm(the_connection):
            print("Eseguo il movimento...")
            
            pos = act_pos( the_connection )
            target_pos = [pos[0] + x, pos[1] + y, pos[2] + z]

            try:
                
                the_connection.mav.set_position_target_local_ned_send(
                    0,  # Time boot ms
                    the_connection.target_system,  # System ID
                    the_connection.target_component,  # Component ID
                    mavutil.mavlink.MAV_FRAME_LOCAL_OFFSET_NED,  # NED frame 
                    0b110000000000 ,  # Flags (posizione 3D e velocità)
                    x, y, z,  # Posizione target X=distance, Y=0, Z=0
                    vx,vy,vz,  # Velocità (0 in X, Y, Z)
                    0, 0, 0,   # Acceleration (opzionale)
                    0,0    #Yaw
                )

                print(f"Comando inviato per spostare il drone.")

                time.sleep(5)
                while True:
                    msg = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
                    if msg:
                        current_pos = [msg.x, msg.y, msg.z]
                        print(f"Posizione attuale: N = {current_pos[0]}m,E = {current_pos[1]}m,Down = {current_pos[2]}m")
                        print(f"Posizione target: N = {target_pos[0]}m,E = {target_pos[1]}m,Down = {target_pos[2]}m")

                        if is_at_target(current_pos, target_pos):
                            print("Posizione raggiunta con successo!!")
                            break

            except Exception as e:
                print(f"Errore durante il movimento: {e}")

        else:
            print("Errore, armare il drone prima di muoverlo!!")    

    else:
        print("La modalità di volo attuale non consente il movimento del drone")


def distance(current_pos, target_pos):
    north_diff = target_pos[0] - current_pos[0]
    east_diff = target_pos[1] - current_pos[1]
    down_diff = target_pos[2] - current_pos[2]
    
    # Calcolo della distanza Euclidea in 3D
    print(math.sqrt(north_diff**2 + east_diff**2 + down_diff**2))
    return math.sqrt(north_diff**2 + east_diff**2 + down_diff**2)

def is_at_target(current_pos,target_pos,threshold = 1):
    dist = distance(current_pos,target_pos)
    return dist <= threshold

def act_pos( the_connection ):
    msg = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
    if msg:
        current_pos = [msg.x, msg.y, msg.z]
        return current_pos


if __name__ == "__main__":
    the_connection = connect.connect( 'udpin:127.0.0.1:5760',10 )
    #mode.set_mode(the_connection,"GUIDED")
    #time.sleep(10)
    #arm.arm( the_connection )
    #time.sleep(2)
    #takeoff.takeoff(the_connection,20)
    #time.sleep(30)
    moveXYZ( the_connection, y = 35 )

