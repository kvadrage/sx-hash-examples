#!/usr/bin/python
'''
This script is setting custom LAG Hash fields for Mellanox Switches.
It tries to read and apply LAG Hash configuration from /etc/sx_hash/sx_lag_hash.json.
'''

import sys
import errno
import json
import argparse

sys.path.append('/lib/python2.7/dist-packages/python_sdk_api/')
sys.path.append('/lib/python2.7/site-packages/python_sdk_api/')
sys.path.append('/usr/lib/python2.7/dist-packages/python_sdk_api/')
sys.path.append('/usr/lib/python2.7/site-packages/python_sdk_api/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/python_sdk_api/')
sys.path.append('/usr/local/lib/python2.7/site-packages/python_sdk_api/')
try:
    import sx_api as sx
except:
    print("Error: can't import SX SDK API Python library!")
    sys.exit(-1)
 
DEFAULT_LAG_HASH_CFG = "/etc/sx_hash/sx_lag_hash.json"

SX_LAG_HASH_TYPES = {name: num for name, num in vars(sx).items() if name.startswith("SX_LAG_HASH_TYPE")}
SX_LAG_HASH_FIELDS_ENABLE = {name: num for name, num in vars(sx).items() if name.startswith("SX_LAG_HASH_FIELD_ENABLE")}
SX_LAG_HASH_FIELDS = {name: num for name, num in vars(sx).items() if name.startswith("SX_LAG_HASH")}

PORT_TYPE_NVE = 8
PORT_TYPE_VPORT = 2
PORT_TYPE_OFFSET = 28
PORT_TYPE_MASK = 0xF0000000

def check_vport(port):
    port_type = (port & PORT_TYPE_MASK) >> PORT_TYPE_OFFSET
    return port_type & PORT_TYPE_VPORT

def check_nve(port):
    port_type = (port & PORT_TYPE_MASK) >> PORT_TYPE_OFFSET
    return port_type & PORT_TYPE_NVE

def get_lag_hash_type_by_name(hash_type_name):
    return SX_LAG_HASH_TYPES.get(hash_type_name, None)

def get_lag_hash_field_enable_by_name(hash_field_enable_name):
    return SX_LAG_HASH_FIELDS_ENABLE.get(hash_field_enable_name, None)

def get_lag_hash_field_by_name(hash_field_name):
    return SX_LAG_HASH_FIELDS.get(hash_field_name, None)

def set_port_lag_hash_params(log_port, lag_hash_params, hash_field_enable_list, hash_field_list):
    lag_hash_params_p = sx.new_sx_lag_port_hash_params_t_p()
    lag_hash_params_p.lag_hash_type = lag_hash_params.lag_hash_type
    lag_hash_params_p.lag_seed = lag_hash_params.lag_seed
    lag_hash_params_p.is_lag_hash_symmetric = lag_hash_params.is_lag_hash_symmetric
    
    hash_field_enable_list_cnt = len(hash_field_enable_list)
    hash_field_enable_list_arr = sx.new_sx_lag_hash_field_enable_t_arr(hash_field_enable_list_cnt)
    
    hash_field_list_cnt = len(hash_field_list)
    hash_field_list_arr = sx.new_sx_lag_hash_field_t_arr(hash_field_list_cnt)
    
    for i, field_enable_name in enumerate(hash_field_enable_list):
        field_enable_id = get_lag_hash_field_enable_by_name(field_enable_name)
        if field_enable_id is not None:
            sx.sx_lag_hash_field_enable_t_arr_setitem(hash_field_enable_list_arr, i, field_enable_id)
        else:
            print("[--] Unknown hash field enable name: %s" % field_enable_name)

    for i, field_name in enumerate(hash_field_list):
        field_id = get_lag_hash_field_by_name(field_name)
        if field_id is not None:
            sx.sx_lag_hash_field_t_arr_setitem(hash_field_list_arr, i, field_id)
        else:
            print("[--] Unknown hash field name: %s" % field_name)
        
    rc = sx.sx_api_lag_port_hash_flow_params_set(handle, sx.SX_ACCESS_CMD_SET, log_port, lag_hash_params_p, hash_field_enable_list_arr, hash_field_enable_list_cnt, hash_field_list_arr, hash_field_list_cnt)

    return rc

    
def print_global_lag_hash_params(lag_hash_params):
    if rc != 0:
        print("[-] Error getting Global LAG hash params: %d" % rc)
        return rc
    print("LAG Hash params:")
    print("    %-20s %s" % ("LAG Hash Type:", lag_hash_params.lag_hash_type))
    print("    %-20s %d" % ("Seed:", lag_hash_params.seed))
    print("    %-20s %d" % ("LAG Hash:", lag_hash_params.lag_hash))
    print("LAG Hash fields:")
    for name, bit in SX_LAG_HASH_FIELDS:
        print("    %-40s %s" % (name, (lag_hash_params.lag_hash & bit) != 0))
    return rc

def get_global_lag_hash_params(handle):
    lag_hash_params = sx.sx_lag_hash_param_t()
    rc = sx.sx_api_lag_hash_flow_params_get(handle, lag_hash_params)
    if rc != 0:
        return rc, None
    return rc, lag_hash_params


def set_global_lag_hash_params(handle, lag_hash_params):
    rc = sx.sx_api_lag_hash_flow_params_set(handle, lag_hash_params)
    return rc
            

def apply_global_lag_hash_cfg(handle, global_hash_config):
    new_hash_params = sx.sx_lag_hash_param_t()
    print("[+] Applying legacy global LAG Hash configuration")
    rc, curr_hash_params = get_global_lag_hash_params(handle)
    if rc != 0:
        print("[--] Error getting legacy global LAG hash params: %d" % rc)
        print("[--] Probably new per-port LAG Hash mode is already configured")
        return rc
    
    global_hash_params = global_hash_config.get("hash_params", {})
  
    hash_type_name = global_hash_params.get("hash_type")
    if hash_type_name:
        hash_type_id = get_lag_hash_type_by_name(hash_type_name)
        if hash_type_id is not None:
            new_hash_params.lag_hash_type = hash_type_id
        else:
            print("[--] Unknown hash type: %s" % hash_type_name)

    new_hash_params.lag_seed = global_hash_params.get("seed", curr_hash_params.lag_seed)   
    new_hash_params.is_lag_hash_symmetric = global_hash_params.get("symmetric_hash", curr_hash_params.is_lag_hash_symmetric)
    
    hash_fields = global_hash_config.get("hash_fields")
    if hash_fields:
        lag_hash = 0
        for field_name in hash_fields:
            field_id = get_lag_hash_field_by_name(field_name)
            if field_id is not None:
                lag_hash |= field_id
            else:
                print("[--] Unknown hash field name: %s" % field_name)
        new_hash_params.lag_hash = lag_hash
    else:
        new_hash_params.lag_hash = curr_hash_params.lag_hash

    return set_global_lag_hash_params(handle, new_hash_params)

def process_single_port_lag_hash_cfg(handle, log_port, port_hash_config, global_hash_params=None):
    port_hash_params_t_p = sx.new_sx_lag_port_hash_params_t_p()
    if global_hash_params:
        port_hash_params_t_p.lag_hash_type = global_hash_params.lag_hash_type
        port_hash_params_t_p.lag_seed = global_hash_params.lag_seed
        port_hash_params_t_p.is_lag_hash_symmetric = global_hash_params.is_lag_hash_symmetric
    
    hash_params = port_hash_config.get("hash_params", {})
    hash_type_name = hash_params.get("hash_type")
    hash_type_id = get_lag_hash_type_by_name(hash_type_name)
    if hash_type_id is not None:
        port_hash_params_t_p.lag_hash_type = hash_type_id
    else:
        print("[--] Unknown hash field name: %s" % hash_type_name)
    
    seed = hash_params.get("seed", port_hash_params_t_p.lag_seed)
    port_hash_params_t_p.lag_seed = seed
    
    symmetric_hash = hash_params.get("symmetric_hash", port_hash_params_t_p.is_lag_hash_symmetric)
    port_hash_params_t_p.is_lag_hash_symmetric = symmetric_hash
    
    hash_fields_enable = port_hash_config.get("hash_fields_enable")
    hash_fields = port_hash_config.get("hash_fields")
    if hash_fields_enable is None or hash_fields is None:
        print("[--] No 'hash_fields_enable' or 'hash_fields' section found in the configuration")
        return -1
    
    rc = set_port_lag_hash_params(log_port, port_hash_params_t_p, hash_fields_enable, hash_fields)
    
    return rc

def apply_port_lag_hash_cfg(handle, port_hash_config):
    ports_map = []
    port_num_max = 128
    port_attributes_list = sx.new_sx_port_attributes_t_arr(port_num_max)
    port_cnt_p = sx.new_uint32_t_p()
    sx.uint32_t_p_assign(port_cnt_p, port_num_max)

    print("[+] Applying new port-based LAG Hash configuration")

    # dump all device ports information
    rc = sx.sx_api_port_device_get(handle, 1, 0, port_attributes_list, port_cnt_p)
    if rc != 0:
        print("[--] Error getting switchs ports information")
        return rc
    port_cnt = sx.uint32_t_p_value(port_cnt_p)

    # populate port name (label name) to log_port mapping
    for i in range(port_cnt):
        port_attributes = sx.sx_port_attributes_t_arr_getitem(port_attributes_list, i)
        is_vport = check_vport(int(port_attributes.log_port))
        is_nve = check_nve(int(port_attributes.log_port))
        if is_nve or is_vport:
            continue    
        port_name = "%d" % (port_attributes.port_mapping.module_port + 1)
        ports_map.append((port_name, port_attributes.log_port))
    
    # try to get existing global LAG hash configuration
    rc, curr_global_hash_params = get_global_lag_hash_params(handle)
    if rc == 0:
        print("[++] Legacy global LAG Hash mode is currently configured")
        print("[++] Overriding it with new per-port LAG Hash configuration")
    
    # check if aggregate configuration for all ports is available
    all_ports_cfg = port_hash_config.get("all")
    if all_ports_cfg:
        print("[++] Applying single LAG Hash configuration to all ports")
        result = 0
        for port_name, log_port in ports_map:
            print("[+++] Applying LAG Hash configuration to port %s (log_port %x)" % (port_name, log_port))
            rc = process_single_port_lag_hash_cfg(handle, log_port, all_ports_cfg, curr_global_hash_params)
            if rc != 0:
                print("[---] Error applying LAG Hash config on port %s (log_port %x)" % (port_name, log_port))
                result = rc
        return result
    
    result = 0
    # iterate all specific ports in the config
    for port_name, hash_config in port_hash_config.items(): 
        ports = [(port_name, log_port) for name,log_port in ports_map if name == port_name]
        if not ports:
            print("[--] Port %s doesn't exist" % port_name)
            continue
        for port_name, log_port in ports:
            print("[++] Applying LAG Hash configuration to port %s (log_port %x)" % (port_name, log_port))
            rc = process_single_port_lag_hash_cfg(handle, log_port, hash_config, curr_global_hash_params)
            if rc != 0:
                print("[--] Error applying LAG Hash config on port %s (log_port %x)" % (port_name, log_port))
                result = rc
    return result

def apply_lag_hash_cfg(handle, config):
    if not config:
        print("[-] Config undefined")
        return -1
    
    global_hash_config = config.get("lag_global_hash")
    if global_hash_config:
        return apply_global_lag_hash_cfg(handle, global_hash_config)
        
    port_hash_config = config.get("lag_port_hash")
    if port_hash_config:
        return apply_port_lag_hash_cfg(handle, port_hash_config)
        
    print("[-] No LAG Hash config provided")
    return -1

def read_lag_hash_cfg(filename):
    config = None
    try:
        with open(filename) as fh:
            config = json.loads(fh.read())
    except IOError as e:
        print("[-] Error reading config file: %s" % e)
    except ValueError as e:
        print("[-] Error parsing config file: %s" % e)
    return config


def parse_args():
    parser = argparse.ArgumentParser(description="Mellanox LAG Hash configuration tool")
    parser.add_argument("-c", "--config-file", help="Configuration file (json)", default=DEFAULT_LAG_HASH_CFG)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    print("[+] Reading LAG hash configuration from '%s'" % args.config_file)
    config = read_lag_hash_cfg(args.config_file)

    if not config:
        sys.exit(-1)
    
    print("[+] opening sdk")
    rc, handle = sx.sx_api_open(None)
    if rc != 0:
        print("[-] Error opening SDK API: %d" % rc)
        sys.exit(rc)

    rc = apply_lag_hash_cfg(handle, config)
    if rc == 0:
        print("[+] LAG Hash configuration applied successfully!")
    else:
        print("[-] Error applying LAG Hash configuration: %d" % rc)

    print("[+] closing sdk")
    sx.sx_api_close(handle)
    sys.exit(rc)
