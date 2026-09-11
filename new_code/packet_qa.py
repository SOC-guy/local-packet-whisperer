def hent_relevante_pakker(filsti, søke_ip=None, søke_port=None, maks_pakker=50):
    """
    Strømmer gjennom PCAP-en og henter KUN pakker som matcher det brukeren spør om.
    Konverterer disse til tekst slik at LLM-en kan svare på spesifikke spørsmål.
    """
    relevante_pakker = []
    
    with PcapReader(filsti) as reader:
        for pkt in reader:
            if len(relevante_pakker) >= maks_pakker:
                break
                
            if pkt.haslayer('IP'):
                # Sjekk om pakken matcher LLM/brukerens søkekriterier
                match_ip = (søke_ip is None) or (pkt['IP'].src == søke_ip or pkt['IP'].dst == søke_ip)
                
                match_port = True
                if søke_port:
                    match_port = (pkt.haslayer('TCP') and (pkt['TCP'].sport == søke_port or pkt['TCP'].dport == søke_port)) or \
                                 (pkt.haslayer('UDP') and (pkt['UDP'].sport == søke_port or pkt['UDP'].dport == søke_port))
                
                if match_ip and match_port:
                    # Konverter KUN denne matchende pakken til et lesbart tekstformat
                    pakke_info = {
                        "tid": float(pkt.time),
                        "src": pkt['IP'].src,
                        "dst": pkt['IP'].dst,
                        "lengde": len(pkt)
                    }
                    if pkt.haslayer('TCP'):
                        pakke_info["type"] = "TCP"
                        pakke_info["flags"] = str(pkt['TCP'].flags)
                    
                    relevante_pakker.append(pakke_info)
                    
    return json.dumps(relevante_pakker, indent=2)
