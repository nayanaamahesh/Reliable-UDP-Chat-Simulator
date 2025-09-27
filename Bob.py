import sys
import struct
import socket

MAX_PACKET_SIZE = 64
HEADER_SIZE = 4  # 1B sequence number + 2B checksum + 1B data length
MAX_DATA_SIZE = MAX_PACKET_SIZE - HEADER_SIZE  # 60 bytes
WINDOW_SIZE = 5


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


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 Bob.py <rcvPort>")
        sys.exit(1)
    
    recv_port = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', recv_port))
    
    expected_seq = 0
    window = {}
    
    while True:
        data, sender_address = sock.recvfrom(1024)
        if not data:
            continue
        
        seq_num, checksum, length = struct.unpack("!B H B", data[:HEADER_SIZE])
        payload = data[HEADER_SIZE:HEADER_SIZE + length]
        #print(f"recv: {seq_num}")
        if checksum != calculate_checksum(payload):
            #print("error")
            continue
        
        # Store packet in the window
        window[seq_num] = payload.decode()
    
        # Send ACK for the received sequence number
        #print(f"sent: {seq_num}")
        ack_message = struct.pack("!B", seq_num)
        sock.sendto(ack_message, sender_address)

        # Print messages in order when the window is full
        while expected_seq in window:
            print(window[expected_seq], end="")
            del window[expected_seq]
            expected_seq += 1
        

if __name__ == "__main__":
    main()

