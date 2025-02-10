from pymavlink import mavutil
import time

def connect(connection_str : str, timeout : float = 10 ):
    """
    connect permette di stabilire una connessione con il drone

    Args:
        connection_str (str): Stringa di connessione, obbligatoria
        timeout (float, opzionale): tempo massimo per aspettare la connessione
    Returns:
        mavutil.mavlink_connection: oggetto connesso al drone se la connessione avviene con successo
        altrimenti ritorna None

    """
    print("Connettendo al drone...")

    try:
        the_connection = mavutil.mavlink_connection(connection_str,timeout=timeout)
        print("Connessione stabilita, attesa heartbeat...")
    except Exception as e:
        print(f"Connessione fallita: {e}")
        return 

    try:
        the_connection.wait_heartbeat(timeout = timeout)
        print(f"Heartbeat ricevuto dal sistema {the_connection.target_system} componente {the_connection.target_component}")
        return the_connection
    except Exception as e:
        print(f"Timeout! Nessun heartbeat ricevuto in {timeout} secondi: {e}")

def close_connection( the_connection ):
    the_connection.close()
    print("Connessione chiusa correttamente")


if __name__ == "__main__":
    connect('udpin:127.0.0.1:5760',10)
    

