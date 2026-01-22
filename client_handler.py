import time
import socket

def handle_client(conn, addr, proc, logger, stats):
    buffer = ""
    timed_out = False   # 🔹 TADY – inicializace flagu

    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                timed_out = False   # 🔹 TADY – klient zase komunikuje

                buffer += data.decode("utf-8", errors="ignore")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    req = line.strip()
                    if not req:
                        continue

                    start = time.time()
                    resp = proc(req)
                    dur = int((time.time() - start) * 1000)

                    stats.record(req[:2], dur)
                    logger.info(
                        client_ip=addr[0],
                        command=req[:2],
                        request_raw=req,
                        response_raw=resp,
                        duration_ms=dur
                    )

                    conn.sendall((resp + "\n").encode("utf-8"))

            except socket.timeout:
                if not timed_out:   # 🔹 TADY – ochrana proti spamu
                    logger.error(client_ip=addr[0], message="Timeout")
                    conn.sendall(b"ER Timeout\n")
                    timed_out = True
                continue
