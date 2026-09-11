from scapy.all import PcapReader
import streamlit as st
import os
import json
from collections import Counter
from lpw_init import getLpwPath

os.chdir(os.path.expanduser("~/pcap-tmp"))


def generer_statistikk(filsti):
    """
    Generer statistikk fra PCAP-fil for å gi LLM oversikt over innholdet.
    Returnerer kompakt JSON-format som er optimalt for Ollama.
    
    Args:
        filsti: Sti til PCAP/PCAPNG-fil
        
    Returns:
        JSON-string med statistikk som kan sendes direkte til LLM
    """
    stats = {
        "totalt_antall_pakker": 0,
        "protokoller": Counter(),
        "kilde_iper": Counter(),
        "destinasjon_iper": Counter(),
        "destinasjon_porter": Counter(),
        "start_tid": None,
        "slutt_tid": None
    }

    try:
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

        # Konverter Counter-objekter til lesbare topp-10 lister for Ollama
        kompakt_oversikt = {
            "totalt_pakker": stats["totalt_antall_pakker"],
            "varighet_sekunder": round(stats["slutt_tid"] - stats["start_tid"], 2) if stats["slutt_tid"] else 0,
            "topp_kilde_ip": dict(stats["kilde_iper"].most_common(10)),
            "topp_dest_ip": dict(stats["destinasjon_iper"].most_common(10)),
            "topp_porter": dict(stats["destinasjon_porter"].most_common(10))
        }
        
        return json.dumps(kompakt_oversikt, indent=2)
    
    except FileNotFoundError:
        error_msg = {"error": f"PCAP-fil ikke funnet: {filsti}"}
        return json.dumps(error_msg)
    except Exception as e:
        error_msg = {"error": f"Feil ved lesing av PCAP-fil: {str(e)}"}
        return json.dumps(error_msg)


def hent_relevante_pakker(filsti, søke_ip=None, søke_port=None, maks_pakker=50):
    """
    Strømmer gjennom PCAP-fil og henter KUN pakker som matcher søkekriterier.
    Returnerer kompakt JSON-format optimalt for Ollama.
    
    Args:
        filsti: Sti til PCAP/PCAPNG-fil
        søke_ip: IP-adresse å søke etter (source eller destination)
        søke_port: Port-nummer å søke etter (TCP/UDP)
        maks_pakker: Maksimalt antall pakker å returnere
        
    Returns:
        JSON-string med matchende pakker
    """
    relevante_pakker = []
    
    try:
        with PcapReader(filsti) as reader:
            for pkt in reader:
                if len(relevante_pakker) >= maks_pakker:
                    break
                    
                if pkt.haslayer('IP'):
                    # Sjekk om pakken matcher søkekriterier
                    match_ip = (søke_ip is None) or (pkt['IP'].src == søke_ip or pkt['IP'].dst == søke_ip)
                    
                    match_port = True
                    if søke_port:
                        match_port = (pkt.haslayer('TCP') and (pkt['TCP'].sport == søke_port or pkt['TCP'].dport == søke_port)) or \
                                     (pkt.haslayer('UDP') and (pkt['UDP'].sport == søke_port or pkt['UDP'].dport == søke_port))
                    
                    if match_ip and match_port:
                        # Konverter matchende pakke til lesbart format
                        pakke_info = {
                            "tid": round(float(pkt.time), 2),
                            "src": pkt['IP'].src,
                            "dst": pkt['IP'].dst,
                            "lengde": len(pkt)
                        }
                        
                        if pkt.haslayer('TCP'):
                            pakke_info["type"] = "TCP"
                            pakke_info["src_port"] = pkt['TCP'].sport
                            pakke_info["dst_port"] = pkt['TCP'].dport
                            pakke_info["flags"] = str(pkt['TCP'].flags)
                        elif pkt.haslayer('UDP'):
                            pakke_info["type"] = "UDP"
                            pakke_info["src_port"] = pkt['UDP'].sport
                            pakke_info["dst_port"] = pkt['UDP'].dport
                        elif pkt.haslayer('ICMP'):
                            pakke_info["type"] = "ICMP"
                        
                        relevante_pakker.append(pakke_info)
                        
        return json.dumps(relevante_pakker, indent=2)
    
    except FileNotFoundError:
        error_msg = {"error": f"PCAP-fil ikke funnet: {filsti}"}
        return json.dumps(error_msg)
    except Exception as e:
        error_msg = {"error": f"Feil ved lesing av PCAP-fil: {str(e)}"}
        return json.dumps(error_msg)


@st.cache_data
def getPcapData(input_file: str = "", filter: str = "", decode_info: dict = {}):
    """
    Henter og prosesserer PCAP-data. Brukes som kompatibilitetslag for eksisterende kode.
    Returnerer statistikk som kan brukes av Ollama.
    
    Args:
        input_file: Sti til PCAP-fil
        filter: Displayfilter (brukes ikke i denne versjonen, men beholdt for kompatibilitet)
        decode_info: Decode-info (brukes ikke i denne versjonen, men beholdt for kompatibilitet)
        
    Returns:
        JSON-string med PCAP-statistikk
    """
    if not input_file:
        error_msg = {"error": "Ingen PCAP-fil spesifisert"}
        return json.dumps(error_msg)
    
    return generer_statistikk(input_file)