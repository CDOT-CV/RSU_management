import sys
sys.path.append("../automation/")
import csv
import os

from unittest.mock import MagicMock, patch

from automation import configrsu_msgfwd

def test_ip_to_hex_little_endian():
  ip = '8.8.8.8'
  hex = configrsu_msgfwd.ip_to_hex(ip, 0)
  assert hex == '00000000000000000000000008080808'

def test_ip_to_hex_big_endian():
  ip = '8.8.8.8'
  hex = configrsu_msgfwd.ip_to_hex(ip, 1)
  assert hex == '08080808000000000000000000000000'

@patch.object(os, 'system')
def test_rsu_status_off(system):
  os.system = MagicMock(return_value='')
  rsu_ip = '0.0.0.0'
  
  configrsu_msgfwd.set_rsu_status(rsu_ip, False)
  os.system.assert_called_with('snmpset -v 3 -u None -a SHA -A None -x AES -X None -l authNoPriv 0.0.0.0 RSU-MIB:rsuMode.0 i 2')

@patch.object(os, 'system')
def test_rsu_status_on(system):
  os.system = MagicMock(return_value='')
  rsu_ip = '0.0.0.0'
  
  configrsu_msgfwd.set_rsu_status(rsu_ip, True)
  os.system.assert_called_with('snmpset -v 3 -u None -a SHA -A None -x AES -X None -l authNoPriv 0.0.0.0 RSU-MIB:rsuMode.0 i 4')

@patch.object(os, 'system')
@patch.object(configrsu_msgfwd, 'set_rsu_status')
@patch.object(configrsu_msgfwd, 'ip_to_hex')
def test_main(ip_to_hex, set_rsu_status, system):
  configrsu_msgfwd.set_rsu_status = MagicMock(return_value='')
  configrsu_msgfwd.ip_to_hex = MagicMock(return_value='08080808000000000000000000000000')
  os.system = MagicMock(return_value='')

  real_path = os.path.realpath(__file__)
  dir_path = os.path.dirname(real_path)
  file = os.path.join(dir_path, 'test_files', 'snmp_test.csv')
  dest_ip = '8.8.8.8'
  msg_type = 'bsm'
    
  with open(file, newline='') as csvfile:
    doc = csv.reader(csvfile, delimiter=',')
    configrsu_msgfwd.main(doc, dest_ip, msg_type)
  
  os.system.assert_called_with('snmpwalk -v 3 -u None -a SHA -A None -x AES -X None -l authNoPriv 172.16.28.190 1.0.15628.4.1 | grep 4.1.7')

def test_unsupported_message_type():
  real_path = os.path.realpath(__file__)
  dir_path = os.path.dirname(real_path)
  file = os.path.join(dir_path, 'test_files', 'snmp_test.csv')
  dest_ip = '8.8.8.8'
  msg_type = 'test'
    
  with open(file, newline='') as csvfile:
    doc = csv.reader(csvfile, delimiter=',')
    assert configrsu_msgfwd.main(doc, dest_ip, msg_type) == -1
