import sys
import socket
import struct

MAX_PACKET_SIZE = 64
HEADER_SIZE = 4
MAX_DATA_SIZE = MAX_PACKET_SIZE - HEADER_SIZE
WINDOW_SIZE = 5
TIMEOUT = 0.05  # 50ms timeout

def calculate_checksum(data):
    """Compute a 16-bit one's complement checksum."""
    if len(data) % 2 == 1:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + (data[i + 1])
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    return ~checksum & 0xFFFF

def create_packet(seq_num, message):
    """Create a UDP packet with a sequence number and checksum."""
    message = message.encode()
    checksum = calculate_checksum(message)
    header = struct.pack("!B H B", seq_num, checksum, len(message))
    return header + message

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 Alice.py <unreliNetPort>")
        sys.exit(1)

    unreli_net_port = int(sys.argv[1])
    server_address = ('localhost', unreli_net_port)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    try:
        # Read full input from stdin (preserves newlines)
        data = sys.stdin.read()
        message_chunks = [data[i:i + MAX_DATA_SIZE] for i in range(0, len(data), MAX_DATA_SIZE)]
        total_chunks = len(message_chunks)
        #print(message_chunks)
        #print(f"Total Chunks: {total_chunks}")

        last_unacked_packet = 0

        while last_unacked_packet < total_chunks:
            # Send up to WINDOW_SIZE packets
            for i in range(WINDOW_SIZE):
                seq_num = last_unacked_packet + i
                if seq_num >= total_chunks:
                    break  # No more data to send

                chunk = message_chunks[seq_num]
                packet = create_packet(seq_num, chunk)
                sock.sendto(packet, server_address)

            # Wait for ACKs
            while True:
                try:
                    packet_recv, _ = sock.recvfrom(64)

                    ack = struct.unpack("!B", packet_recv)[0]  # Convert bytes to integer

                    if ack == last_unacked_packet:
                        last_unacked_packet = ack + 1  # Slide window forward
                except socket.timeout:
                    break  # Timeout -> retransmit
  
    finally:
        sock.close()

if __name__ == "__main__":
    main()

