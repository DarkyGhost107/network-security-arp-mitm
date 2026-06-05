# ARP MitM Attack - Laboratorio de Seguridad de Redes

**Ambiente:** GNS3 (Controlado) | **Herramienta:** Python 3 + Scapy | **Capa OSI:** Capa 2/3

## Aviso Legal

Uso **exclusivamente educativo** en laboratorio controlado (GNS3). El uso no autorizado es **ilegal**.

## 1. Objetivo del Laboratorio

Demostrar el ataque ARP Spoofing para lograr un Man-in-the-Middle (MitM): el atacante envenena las caches ARP de la victima y del gateway haciendo que todo el trafico entre ambos pase por la maquina del atacante.

## 2. Objetivo del Script

`arp_mitm.py` realiza ARP Spoofing bidireccional:
- Le dice a la **victima** que la MAC del gateway es la del atacante.
- Le dice al **gateway** que la MAC de la victima es la del atacante.

## 3. Parametros del Script

| Parametro | Flag | Tipo | Default | Descripcion |
|-----------|------|------|---------|-------------|
| IP Victima | `-v` | str | requerido | IP del host victima |
| IP Gateway | `-g` | str | requerido | IP del gateway/router |
| Interfaz | `-i` | str | eth0 | Interfaz de red |
| Intervalo | `--interval` | float | 1.5 | Segundos entre re-envios ARP |

### Ejemplo de uso

```bash
sudo python3 arp_mitm.py -v 192.168.1.10 -g 192.168.1.1
sudo python3 arp_mitm.py -v 192.168.1.10 -g 192.168.1.1 -i eth1 --interval 1.0
```
![Texto alternativo](https://github.com/DarkyGhost107/network-security-arp-mitm/blob/main/screenshots/ejemplo%20mitm.png)

## 4. Requisitos

```bash
Python 3.8+
pip install scapy
root (sudo)
echo 1 > /proc/sys/net/ipv4/ip_forward  # El script lo hace automaticamente
```

## 5. Funcionamiento del Script

1. Resolucion de MACs via ARP Request (victima y gateway)
2. Bucle de envenenamiento:
   - ARP Reply a victima: "gateway = MAC atacante"
   - ARP Reply a gateway: "victima = MAC atacante"
   - IP Forwarding activo para no interrumpir trafico
3. Restauracion al detener (Ctrl+C)

```
ANTES:  Victima ─────────────────── Gateway
DURANTE: Victima ─ Atacante (MitM) ─ Gateway
                        (captura/modifica trafico)
```

## 6. Topologia de Red (GNS3)

![Texto alternativo](https://github.com/DarkyGhost107/network-security-arp-mitm/blob/main/screenshots/topologia%20arp.png)

### Direccionamiento IP

| Dispositivo | IP | Rol |
|-------------|-----|-----|
| Victima | 192.168.1.10/24 | Host objetivo |
| Atacante (Kali) | 192.168.1.50/24 | Maquina atacante |
| Gateway | 192.168.1.1/24 | Router |

## 7. Contramedidas

| Contramedida | Comando Cisco IOS | Descripcion |
|---|---|---|
| ARP Inspection Dinamica (DAI) | `ip arp inspection vlan 1` | Valida ARP contra tabla DHCP Snooping |
| Entradas ARP estaticas | `arp -s <IP> <MAC>` | Previene envenenamiento en hosts criticos |
| DHCP Snooping | `ip dhcp snooping` | Tabla de confianza base para DAI |

```cisco
ip dhcp snooping
ip dhcp snooping vlan 1
interface GigabitEthernet0/1
 ip dhcp snooping trust
ip arp inspection vlan 1
interface GigabitEthernet0/2
 ip arp inspection limit rate 100
```

## 8. Referencias

- [MITRE ATT&CK T1557.002 - ARP Cache Poisoning](https://attack.mitre.org/techniques/T1557/002/)
- [RFC 826 - Address Resolution Protocol](https://datatracker.ietf.org/doc/html/rfc826)

## 9.Enlace:
Video: https://youtu.be/YeEULVo7HAI


---
*Laboratorio de Seguridad de Redes | GNS3 | Uso educativo exclusivo*
