from scapy.all import PcapReader
from collections import Counter
import json

def generer_statistikk(filsti):
    stats = {
        "totalt_antall_pakker": 0,
        "protokoller": Counter(),
        "kilde_iper": Counter(),
        "destinasjon_iper": Counter(),
        "destinasjon_porter": Counter(),
        "start_tid": None,
        "slutt_tid": None
    }

    with PcapReader(filsti) as reader:
        for pkt in reader:
            stats["totalt_antall_pakker"] += 1
            
            # Tidsstyring
            if stats["start_tid"] is None:
                stats["start_tid"] = float(pkt.time)
            stats["slutt_tid"] = float(pkt.time)

            # Protokoller og IP-analyse
            if pkt.haslayer('IP'):
                stats["kilde_iper"][pkt['IP'].src] += 1
                stats["destinasjon_iper"][pkt['IP'].dst] += 1
                stats["protokoller"][pkt['IP'].proto] += 1

                if pkt.haslayer('TCP'):
                    stats["destinasjon_porter"][pkt['TCP'].dport] += 1
                elif pkt.haslayer('UDP'):
                    stats["destinasjon_porter"][pkt['UDP'].dport] += 1

    # Gjør Counter-objektene om til vanlige, lesbare topp-10 lister for LLM
    kompakt_oversikt = {
        "totalt_pakker": stats["totalt_antall_pakker"],
        "varighet_sekunder": stats["slutt_tid"] - stats["start_tid"],
        "topp_kilde_ip": dict(stats["kilde_iper"].most_common(10)),
        "topp_dest_ip": dict(stats["destinasjon_iper"].most_common(10)),
        "topp_porter": dict(stats["destinasjon_porter"].most_common(10))
    }
    
    return json.dumps(kompakt_oversikt, indent=2)

# 1. Generer oversikten via Python
oversikt_tekst = generer_statistikk("min_dump.pcapng")

# 2. Send denne oversikt_tekst inn i prompten til LLM-en din:
# "Her er en statistisk oversikt over en PCAP-fil. Lag et sammendrag for brukeren: [oversikt_tekst]"