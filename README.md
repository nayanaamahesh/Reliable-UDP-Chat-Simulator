# Reliable UDP Chat Simulator



## Overview

This project implements a reliable one-way chat system over an unreliable UDP network. The program ensures that messages sent from a sender are correctly received by a receiver, even when the network randomly corrupts or drops packets.

The system consists of three main components:

1. **Alice.py** – Reads messages from standard input and sends them through the network.
2. **Bob.py** – Receives messages and prints them to standard output.
3. **UnreliNET.class / UnreliNET.java** – Simulates an unreliable network channel that may corrupt or drop packets randomly while guaranteeing in-order delivery.

Additional files for testing include `input.txt`, `1a.txt`, `1b.txt`, `2a.txt`, etc., and the testing script `RunTest.sh`.


## Features

* Implements **Selective Repeat (SR) reliable data transfer protocol** with a sliding window.
* Handles **packet corruption** and **packet loss** in both data and acknowledgment packets.
* Ensures reliable message delivery over an unreliable UDP channel.
* Each packet contains a **sequence number** and a **checksum** for error detection.
* Supports payloads up to **64 bytes per packet** (including header/trailer fields).
* Configurable **window size** and **timeout** (50ms) for retransmissions.



## Requirements

* Python 3 (tested with Python 3.10)
* Java (for UnreliNET)
* The following files are included:

```
Alice.py
Bob.py
UnreliNET.java
UnreliNET.class
UnreliNET$Forwarder.class
UnreliNET$1.class
input.txt
1a.txt, 1b.txt, 1c.txt, 1d.txt
2a.txt, 2c.txt, 2d.txt
RunTest.sh
common.sh
```


## Usage

### Running Bob

```bash
python3 Bob.py <receive_port>
```

Example:

```bash
python3 Bob.py 9001
```

### Running UnreliNET

```bash
java UnreliNET <P_DATA_CORRUPT> <P_DATA_LOSS> <P_ACK_CORRUPT> <P_ACK_LOSS> <unreliNetPort> <rcvPort>
```

Example:

```bash
java UnreliNET 0.3 0.2 0.1 0.05 9000 9001
```

### Running Alice

```bash
python3 Alice.py <unreliNetPort>
```

Example:

```bash
python3 Alice.py 9000
```

### Optional: File Redirection for Testing

```bash
python3 Alice.py 9000 < input.txt
python3 Bob.py 9001 > output.txt
cmp input.txt output.txt
```


## Implementation Notes

* Uses **Selective Repeat protocol** with a window size of 5 packets.
* Retransmits only missing or corrupted packets after a timeout.
* Alice splits messages into chunks and assigns a sequence number to each packet.
* Bob buffers out-of-order packets and prints messages in order when available.
* Checksums are computed to detect corruption.


## Testing

* Use the provided `RunTest.sh` script to validate program behavior across multiple test cases.
* Make sure to remove debug messages before running tests.


## Acknowledgements

* The **UnreliNET program** simulates the unreliable network channel.
* Protocol design is based on standard reliable data transfer mechanisms taught in networking (Selective Repeat, checksums, sliding window).


