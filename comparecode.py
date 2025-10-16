from scapy.all import *
import random
import string
import numpy as np


def random_bytes(length):
    tmp_str = ''.join(random.choice(string.printable) for _ in range(length))
    return bytes(tmp_str, encoding='utf-8')


def rebuild(
    grp_size,
    X,
    groupList,
    # tmp_pcap_file
):
    newList = []

    # This print statement can be removed if you wish, but it's helpful for now.
    print("\n--- [DEBUG] Entering Rebuilder Function ---")

    for i in range(grp_size):
        
        # This print statement can also be removed later.
        try:
            packet_summary = groupList[i].summary()
            print(f"[DEBUG] Processing original packet index {i}: {packet_summary}")
        except Exception as e:
            print(f"[DEBUG] Could not get summary for packet index {i}. Error: {e}")

        for j in range(int(round(X.mal[i][1]))):
            pkt = copy.deepcopy(groupList[i])
            
            # --- MODIFICATION STARTS HERE ---
            if round(X.craft[i][j][1]) == 1:
                # If the packet has an Ether layer, remove its payload. Otherwise, do nothing.
                if pkt.haslayer(Ether):
                    pkt[Ether].remove_payload()

            elif round(X.craft[i][j][1]) == 2:
                # If the packet has a network layer, remove its payload. Otherwise, do nothing.
                if pkt.haslayer(IP):
                    pkt[IP].remove_payload()
                elif pkt.haslayer(IPv6):
                    pkt[IPv6].remove_payload()
                elif pkt.haslayer(ARP):
                    pkt[ARP].remove_payload()

            elif round(X.craft[i][j][1]) == 3:
                # If the packet has a transport layer, remove its payload. Otherwise, do nothing.
                if pkt.haslayer(ICMP):
                    pkt[ICMP].remove_payload()
                elif pkt.haslayer(TCP):
                    pkt[TCP].remove_payload()
                elif pkt.haslayer(UDP):
                    pkt[UDP].remove_payload()
            # --- MODIFICATION ENDS HERE --- (The `else: raise RuntimeError` blocks were removed)

            # The rest of the logic remains the same
            # Ensure the payload length is not negative before adding
            payload_len = int(round(X.craft[i][j][2]))
            if payload_len < 0:
                payload_len = 0
            pkt.add_payload(random_bytes(payload_len))
            
            pkt.time = X.mal[i][0] - X.craft[i][j][0]
            newList.append(pkt)

        mal_pkt = copy.deepcopy(groupList[i])
        mal_pkt.time = X.mal[i][0]
        newList.append(mal_pkt)

    return newList