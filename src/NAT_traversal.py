#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse
import sounddevice as sd
import numpy as np
import socket
import time
import psutil
import math
import struct
import threading
import minimal
import soundfile as sf
import logging
import stun
from collections import Counter

def leer_fichero():
  fichero = open("public-stun-list.txt")
  servidores = fichero.readlines()
  #print(len(servidores))
  ip=servidores[0][0:servidores[0].find(":")]
  #print(ip)
  fichero.close()
  return servidores

def get_nat():
  serv = leer_fichero()
  M=[[1,2,3]]
  for x in range(0, 15):
      direccion=serv[x][0:serv[x].find(":")]
      #print(direccion)
      nat_type, external_ip, external_port = stun.get_ip_info(stun_host=direccion)
      if external_ip is not None:
       M.append([external_ip, external_port, nat_type])
       #print(M[len(M)-1])
      #print(external_ip, external_port, nat_type, sep="\t")
      #print(external_port)
      #print(nat_type)

  IPs=[fila[0] for fila in M]
  puertos=[fila[1] for fila in M]
  tipo=[fila[2] for fila in M]
  # print(IPs)
  # print(puertos)
  # print(tipo)
  counter1 = Counter(IPs)
  counter2 = Counter(puertos)
  counter3 = Counter(tipo)
  a, *extra1 = counter1.most_common()
  b, *extra2= counter2.most_common()
  c, *extra3= counter3.most_common()

  if b[1] != len(puertos)-1:
   print("NAT Simetrica, necesitas abrir puertos manualmente")
  else:
   print("La NAT no es simetrica")
   print(f"Tu IP y puerto son: {a[0]}, {b[0]}")

print("Obteniendo tu tipo de NAT...")
get_nat()
result=input("Quieres ejecutar intercom? [y/n]: ")
if result=="y":
 print("Ejecutando intercom")
 ip_dest=input("Introduce la IP de destino (en blanco para usar localhost): ")
 port_dest=input("Introduce el puerto de destino (en blanco para usar 4444): ")
 if(port_dest != ""):
  port_dest=int(port_dest)

 minimal.parser.add_argument("-b", "--buffering_time", type=int, default=150, help="Miliseconds to buffer")

 try:
    import argcomplete  # <tab> completion for argparse.
 except ImportError:
      logging.warning("Unable to import argcomplete (optional)")

 if __name__ == "__main__":
     minimal.parser.description = __doc__

     try:
      argcomplete.autocomplete(minimal.parser)
     except Exception:
      logging.warning("argcomplete not working :-/")

     minimal.args = minimal.parser.parse_known_args()[0]
     if(ip_dest != ""):
       minimal.args.destination_address=ip_dest
     if(port_dest != ""):
       minimal.args.destination_port=port_dest
    
     if minimal.args.list_devices:
         print("Available devices:")
         print(sd.query_devices())
         quit()

     if minimal.args.show_stats or minimal.args.show_samples:
         intercom = minimal.Minimal__verbose()
     else:
         intercom = minimal.Minimal()
     try:
         intercom.run()
     except KeyboardInterrupt:
         minimal.parser.exit("\nSIGINT received")
     finally:
         intercom.print_final_averages()