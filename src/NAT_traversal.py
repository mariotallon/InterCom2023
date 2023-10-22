#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
from minimal import *
import stun

def get_external_endpoint():
    nat_type, external_ip, external_port = stun.get_ip_info(stun_host='stun.l.google.com')
    return nat_type, external_ip, external_port

nat_type, external_ip, external_port = get_external_endpoint()

if nat_type is not None:
 print(external_ip)
 print(external_port)

def get_external_endpoint():
   nat_type, external_ip, external_port = stun.get_ip_info(stun_host='stun.12connect.com')
   return nat_type, external_ip, external_port

nat_type, external_ip, external_port = get_external_endpoint()

if nat_type is not None:
 print(external_ip)
 print(external_port)

def get_external_endpoint():
    nat_type, external_ip, external_port = stun.get_ip_info(stun_host='stun.12voip.com')
    return nat_type, external_ip, external_port

nat_type, external_ip, external_port = get_external_endpoint()

if nat_type is not None:
 print(external_ip)
 print(external_port)

 def get_external_endpoint():
    nat_type, external_ip, external_port = stun.get_ip_info(stun_host='stun.voippro.com')
    return nat_type, external_ip, external_port

nat_type, external_ip, external_port = get_external_endpoint()

if nat_type is not None:
 print(external_ip)
 print(external_port)