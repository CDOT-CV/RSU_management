import sys
sys.path.append("../automation/")
import csv
import os

from automation import configrsu_msgfwd

os.environ['SNMP_USERNAME'] = 'testUsertest'
os.environ['SNMP_PASSWORD'] = 'testpasswordtest'

def test_ip_to_hex_little_endian():
  ip = '8.8.8.8'
  hex = configrsu_msgfwd.ip_to_hex(ip, 0)
  assert hex == '00000000000000000000000008080808'

def test_ip_to_hex_big_endian():
  ip = '8.8.8.8'
  hex = configrsu_msgfwd.ip_to_hex(ip, 1)
  assert hex == '08080808000000000000000000000000'

def test_rsu_status_off():
  rsu_ip = '0.0.0.0'
  
  # Since there is no snmp server, simply running the shell command successfully should suffice
  try:
    configrsu_msgfwd.set_rsu_status(rsu_ip, False)
    assert True
  except Exception as e:
    print('Encountered issue: {}'.format(e))
    assert False

def test_rsu_status_on():
  rsu_ip = '0.0.0.0'
  
  # Since there is no snmp server, simply running the shell command successfully should suffice
  try:
    configrsu_msgfwd.set_rsu_status(rsu_ip, True)
    assert True
  except Exception as e:
    print('Encountered issue: {}'.format(e))
    assert False

def test_main():
  real_path = os.path.realpath(__file__)
  dir_path = os.path.dirname(real_path)
  file = os.path.join(dir_path, 'test_files', 'snmp_test.csv')
  dest_ip = '8.8.8.8'
  udp_port = 46800
  rsu_index = 20
  
  # Since there is no snmp server, simply running the shell commands successfully should suffice
  try:
    with open(file, newline='') as csvfile:
      doc = csv.reader(csvfile, delimiter=',')
      configrsu_msgfwd.main(doc, dest_ip, udp_port, rsu_index, 0)
    assert True
  except Exception as e:
    print('Encountered issue: {}'.format(e))
    assert False
