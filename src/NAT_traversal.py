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
print(IPs)
print(puertos)
print(tipo)
counter1 = Counter(IPs)
counter2 = Counter(puertos)
counter3 = Counter(tipo)
a, *extra1 = counter1.most_common()
b, *extra2= counter2.most_common()
c, *extra3= counter3.most_common()

if b[1] != len(puertos):
 print("Nat Simetrica, no se puede ejecutar")
else:
  print("La NAT no es simetrica")
  print("Tu IP y puerto son:")
  print(a[0])
  print(b[0])

#print(a)
#print(b)
#print(c)