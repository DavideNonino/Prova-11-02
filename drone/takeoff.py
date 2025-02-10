from pymavlink import mavutil
import connect
import mode
import arm
import time

# Modalità di volo consentite per il decollo
mode_en = ['STABILIZE', 'GUIDED', 'LOITER', 'POSHOLD']

def takeoff(the_connection, altitude):
    
    mode_act = mode.get_mode(the_connection)
    
    if mode_act in mode_en:
        if arm.check_if_arm(the_connection):
            print("Eseguo il decollo...")

            try:
                the_connection.mav.command_long_send(
                    the_connection.target_system,
                    the_connection.target_component,
                    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                    0,
                    0, 0, 0, 0, 0, 0,
                    altitude  # Altitudine di takeoff
                )

                msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=10)
                if msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                    print(f"Decollo accettato. Il drone sta salendo fino a {altitude} metri.")
                    print(msg)
                    monitor_takeoff(the_connection,altitude)
                else:
                    print("Errore, ACK non ricevuto.")
    
            except Exception as e:
                print(f"Errore durante il takeoff: {e}")

        else:
            print("Errore, armare il drone prima di decollare!!")    

    else:
        print("La modalità di volo attuale non consente il decollo")    


def monitor_takeoff(the_connection,altitude):
    
    print("Monitoraggio del decollo...")
    
    while True:
        msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
        if msg:
            act_altitude = msg.relative_alt / 1000  # In metri
            print(f"Altitudine corrente: {act_altitude}m")
            if act_altitude >= (altitude *0.95): 
                print("Drone decollato con successo!")
                break
        time.sleep(1)


if __name__ == "__main__":
    the_connection = connect.connect('udpin:127.0.0.1:5760',10)
    arm.arm( the_connection )
    mode.set_mode(the_connection,"GUIDED")
    takeoff(the_connection,20)