from pymavlink import mavutil
import connect

def get_global_position ( the_connection ):
    
    try:

        the_connection.mav.request_data_stream_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_DATA_STREAM_POSITION, 1, 1)

        message = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True,  timeout = 10)

        lat = message.lat / 1e7  # La latitudine è in centimilionesimi di grado
        lon = message.lon / 1e7  # La longitudine è in centimilionesimi di grado
        alt = message.alt / 1000  # L'altitudine è in millimetri

        # Stampa la posizione globale
        print(f"Posizione globale: Lat: {lat}, Lon: {lon}, Alt: {alt}")

    except Exception as e:
        print(f"Errore durante la ricezione delle coordinate globali: {e}")

if __name__ == "__main__":
    the_connection = connect.connect('udpin:127.0.0.1:5760',10)
    get_global_position( the_connection )