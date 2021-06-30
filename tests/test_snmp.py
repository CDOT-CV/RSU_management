from automation import configrsu_msgfwd
from unittest.mock import MagicMock, call, patch
import os
import csv
import sys
sys.path.append("../automation/")


def test_ip_to_hex_little_endian():
    ip = '8.8.8.8'
    hex = configrsu_msgfwd.ip_to_hex(ip, 0)
    assert hex == '00000000000000000000FFFF08080808'


def test_ip_to_hex_big_endian():
    ip = '8.8.8.8'
    hex = configrsu_msgfwd.ip_to_hex(ip, 1)
    assert hex == '08080808000000000000000000000000'


@patch.object(os, 'system')
def test_rsu_status_off(system):
    os.system = MagicMock(return_value='')
    rsu_ip = '0.0.0.0'

    configrsu_msgfwd.set_rsu_status(rsu_ip, False)
    os.system.assert_called_with(
        'snmpset -v 3 -u None -a SHA -A None -x AES -X None -l authNoPriv 0.0.0.0 RSU-MIB:rsuMode.0 i 2')


@patch.object(os, 'system')
def test_rsu_status_on(system):
    os.system = MagicMock(return_value='')
    rsu_ip = '0.0.0.0'

    configrsu_msgfwd.set_rsu_status(rsu_ip, True)
    os.system.assert_called_with(
        'snmpset -v 3 -u None -a SHA -A None -x AES -X None -l authNoPriv 0.0.0.0 RSU-MIB:rsuMode.0 i 4')


@patch.object(configrsu_msgfwd, 'config_msgfwd')
def test_main(config_msgfwd):
    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    file = os.path.join(dir_path, 'test_files', 'snmp_test.csv')
    dest_ip = '8.8.8.8'
    msg_type = 'bsm'
    index = 1

    with open(file, newline='') as csvfile:
        doc = csv.reader(csvfile, delimiter=',')
        configrsu_msgfwd.main(doc, dest_ip, msg_type, index)

    # we mocked the config_msgfwd message, and we know the csv has 4 entries. verify our mock was called once for each
    assert configrsu_msgfwd.config_msgfwd.call_count == 4


@patch.object(os, 'system')
@patch.object(configrsu_msgfwd, 'set_rsu_status')
@patch.object(configrsu_msgfwd, 'ip_to_hex')
def test_config_msgfwd(ip_to_hex, set_rsu_status, system):
    configrsu_msgfwd.set_rsu_status = MagicMock(return_value='')
    configrsu_msgfwd.ip_to_hex = MagicMock(
        return_value='08080808000000000000000000000000')
    os.system = MagicMock(return_value='')

    rsu_ip = '172.16.28.221'
    dest_ip = '10.10.10.11'
    udp_port = '46800'
    rsu_index = 1
    psid = 20
    endian = 1

    configrsu_msgfwd.config_msgfwd(
        rsu_ip, dest_ip, udp_port, rsu_index, psid, endian)
    
    snmp_call = 'snmpset -v 3 -u None -a SHA -A None -x AES -X None -l authNoPriv 172.16.28.221 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdStatus.1 i 4 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdPsid.1 x 20 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdDestIpAddr.1 x 08080808000000000000000000000000 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdDestPort.1 i 46800 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdProtocol.1 i 2 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdRssi.1 i -100 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdMsgInterval.1 i 1 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdDeliveryStart.1 x 0C1F07B21100 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdDeliveryStop.1 x 0C1F07F41100 '
    snmp_call += 'RSU-MIB:rsuDsrcFwdEnable.1 i 1'

    calls = []
    calls.append(call(snmp_call))
    os.system.assert_has_calls(calls)

def test_unsupported_message_type():
    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    file = os.path.join(dir_path, 'test_files', 'snmp_test.csv')
    dest_ip = '8.8.8.8'
    msg_type = 'test'
    index = 1

    with open(file, newline='') as csvfile:
        doc = csv.reader(csvfile, delimiter=',')
        assert configrsu_msgfwd.main(doc, dest_ip, msg_type, index) == -1
