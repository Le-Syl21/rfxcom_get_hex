#!/bin/env python3
from serial import Serial
from serial.tools import list_ports
from pick import pick
from time import sleep
import argparse

#RFCOM CONST + CMD
baudrate = 38400 #RFXCom factory speed
timeout = 1 #Serial Timeout
init='0d 00 00 00 00 00 00 00 00 00 00 00 00 00'
reset='0d 00 00 01 02 00 00 00 00 00 00 00 00 00'
get='0d 00 00 02 07 00 00 00 00 00 00 00 00 00'
undec='0d 00 00 03 03 53 00 80 00 00 00 00 00 00'

def get_device():
    print("Détecting Devices:")
    ports=[]
    descriptions=[]
    menu=[]
    for port in list_ports.comports():
        ports.append(port.device)
        descriptions.append(port.description)
        menu.append(f"{port.device}\t=>\t{port.description}")
    line , index = pick(menu, "Please choose your RFXCom Device: ")
    port = ports[index]
    description = descriptions[index]
    print(f"{description} -> Selected")
    return port

def get_conn(port):
    print("Opening port: ", end='')
    try:
        conn = Serial(port, baudrate, timeout=timeout)
        print("OK")
    except serial.SerialException as e:
        print(f"{port}, baudrate: {baudrate}, timeout: {timeout} ERROR: {e}")
        quit()
    return conn

def close_conn(conn):
    print("Closing port: ", end='')
    try:
        conn.close()
        print("OK")
    except serial.SerialException as e:
        print(f"{port}, baudrate: {baudrate}, timeout: {timeout} ERROR: {e}")


def send_raw(conn, ba, waitreturn = True):
    conn.write(ba)
    if waitreturn:
        return get_raw(conn)

def get_raw(conn):
    ba = bytearray()
    while True:
        data = conn.read()
        if data :
            ba += data
        else:
            if ba:
                return ba

def get_packets(ba):
    packets=[]
    first=True
    while ba:
        size = ba[0]+1
        packets.append(ba[:size])
        ba = ba[size:]
    return packets

def packet_decode(packet):
    print(f"Received RF Raw HEX: {packet.hex()}")
    print("=== Decoding ===")
    #HEAD
    size = packet[0]
    print(f"Packet Length : {size}")
    sync = packet[1]
    print(f"Sync : {sync}")
    subtype = packet[2]
    print(f"Subtype : {subtype}")
    packet_nbr = packet[3]
    print(f"Packet number : {packet_nbr}")
    repeat = packet[4]
    print(f"Repeat : {repeat}")
    #DATA
    data=[]
    bytes_data = packet[5:]
    while bytes_data:
        data.append(int.from_bytes(bytes_data[:2], byteorder='big'))
        bytes_data = bytes_data[2:]
    print(f"Decoded data: {data}")
    print("="*16)
    return sync, data

def rfx_file(name, repeat, data):
    filename = f"{name}_RFXtrx.txt"
    print(f"Creating sending file '{filename}' for RFXmngr usage (Windows program)")
    #Adding header
    data = [0, repeat] + data
    #Modify tail
    if data[-1]==0:
        data[-1]=10000
    with open(filename, 'w') as file:
        print('\n'.join(str(item) for item in data), file=file)

def packet_encode(sync, repeat, data):
    print("=== Encoding ===")
    ba = bytearray()
    #HEAD
    ba += (sync).to_bytes(1, byteorder='big')   #Add sync
    ba += (0).to_bytes(1, byteorder='big')      #Add Subtype
    ba += (1).to_bytes(1, byteorder='big')      #Add Packet number
    ba += (repeat).to_bytes(1, byteorder='big') #Add Repeat - Setting the repeat value to 7 is a recommendation from RFXCom
    #Modify tail
    if data[-1] == 0:
        data[-1] = 10000
    #Put data
    for i in data:
        ba += (i).to_bytes(2, byteorder='big')
    #Add Packet Length
    ba.insert(0, len(ba))
    print(f"Hex command for RFXcom is: {ba.hex()}")
    print("="*16)
    return ba

def hex_file(name, ba):
    filename = f"{name}_Hexcode.txt"
    print(f"Creating sending file '{filename}' for Raw usage")
    with open(filename, 'w') as file:
        print(ba.hex(), file=file)

# MAIN
#Get Args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-p', '--port', type=str, help="RFXtrx port like '/dev/ttyUSB0'")
parser.add_argument('-r', '--repeat', type=int, default=8, help="Repeat number (default=8) but if doesn't work you can try to grow up to 16, 32, 64, max 255 but no sens")
parser.add_argument('-s', '--source', type=str, help="Your own hex source string like '0x78 0x7f 0x00 0x00 0x01' or '0x78 0x7f 0x00 0x00 0x01' or '78 7f 00 00 01' or '787f000001'")
parser.add_argument('-n', '--nofiles', action='store_true', help="Don't create output files")
args = parser.parse_args()

#HEX
if args.source:
    packet=bytes.fromhex(args.source.replace(",", "").replace("0x", "").replace(" ", "").strip())
    sync, data = packet_decode(packet)
    output_ba = packet_encode(sync, args.repeat, data)
    if not args.nofiles:
        name = input("Get a name for the device (rf3_on, rf3_off, btn2): ")
        if not name:
            name = "output"
        rfx_file(name, args.repeat, data)
        hex_file(name, output_ba)
    print("Bye")
    quit()

#Get serial
if not args.port:
    port = get_device()
conn = get_conn(port)

#Init RFXCom
print("Send init")
send_raw(conn, bytes.fromhex(init), False)
sleep(1)
print("Send reset")
send_raw(conn, bytes.fromhex(reset))
print("Activating Undecoded Mode")
send_raw(conn, bytes.fromhex(undec))

#Work Loop
n=1
ended = False
while not ended:
    print("Waiting your RF input (Press your button)...")
    input_ba = get_raw(conn)
    packet = get_packets(input_ba)[0] #Select first received packet
    sync, data = packet_decode(packet)
    output_ba = packet_encode(sync, args.repeat, data)
    if not args.nofiles:
        name = input("Get a name for the device (rf3_on, rf3_off, btn2): ")
        if not name:
            name = f"output-{n}"
            n+=1
        rfx_file(name, args.repeat, data)
        hex_file(name, output_ba)
    answer = input("Do you want to try sending this RF by the RFXCom ? (y/N): ")
    if answer.lower().startswith('y'):
        print("Sending packet")
        send_raw(conn, output_ba)
    answer = input("Add an other device ? (y/N): ")
    if not answer.lower().startswith('y'):
        break
print("Bye")
quit()
