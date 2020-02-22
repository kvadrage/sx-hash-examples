# sx-lag-hash
A script to configure custom LAG Hash parameters for Mellanox Spectrum Switches using
Mellanox SX SDK API.

# Requirements
Mellanox Spectrum Switches running NOS with SDK API access:
- Onyx
- Cumulus
- SONiC

## Install
Copy this `sx_lag_hash.py` to Mellanox switch in an environment with SDK API access.

For example, a [docker container with SDK libs](https://community.mellanox.com/s/article/getting-started-with-docker-container-over-mlnx-os-sdk-interfaces) in Onyx.

Then create LAG hash configuration file: `vi /etc/sx_hash/sx_lag_hash.json`

# Usage
This script reads custom LAG hash configuration from `/etc/sx_hash/sx_lag_hash.json` file and applies new LAG Hash parameters using Mellanox SX SDK API.

## Considerations
There're two different LAG Hash configuration modes upported in Mellanox SX SDK API for Spectrum switches:
- **Global configuration mode (legacy API)** - allows configuring only limited number of packet fields for LAG hashing 
- **Port configuration mode (new API)** - allows very flexible LAG Hash configuration with ~50 different packet fields for hashing

Usually a **Global configuration mode** is enabled by default (Onyx, Cumulus).

> **IMPORTANT NOTE:** 
>
> Switching from Global mode to Port mode is supported.
>
> However, ***switching back from Port mode to Global mode is not supported***. Need to reboot the device or reload SDK.

## Configuration examples

You can find more examples [here](./examples/).

### Legacy global LAG Hash mode

```json
{
    "lag_global_hash": {
        "hash_params": {
            "hash_type": "SX_LAG_HASH_TYPE_CRC",
            "symmetric_hash": false,
            "seed": 98335670
        },
        "hash_fields": [
            "SX_LAG_HASH_INGRESS_PORT",
            "SX_LAG_HASH_SMAC_IP",
            "SX_LAG_HASH_SMAC_NON_IP",
            "SX_LAG_HASH_DMAC_IP",
            "SX_LAG_HASH_DMAC_NON_IP",
            "SX_LAG_HASH_ETHER_IP",
            "SX_LAG_HASH_ETHER_NON_IP",
            "SX_LAG_HASH_VID_IP",
            "SX_LAG_HASH_VID_NON_IP",
            "SX_LAG_HASH_S_IP",
            "SX_LAG_HASH_D_IP",
            "SX_LAG_HASH_L4_SPORT",
            "SX_LAG_HASH_L4_DPORT"
        ]
    }
}
```

### New per-port LAG Hash mode

#### Configuration custom hashing for all ports
```json
{
    "lag_port_hash": {
        "all": {
            "hash_params": {
                "hash_type": "SX_LAG_HASH_TYPE_CRC",
                "symmetric_hash": true,
                "seed": 98335670
            },
            "hash_fields_enable": [
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_NON_IP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_IPV6",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV4_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV4_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV6_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L4_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L4_IPV6",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L2_NON_IP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L2_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L2_IPV6",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV4_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV6_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV6_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L4_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L4_IPV6"            
            ],
            "hash_fields": [
                "SX_LAG_HASH_OUTER_SMAC",
                "SX_LAG_HASH_OUTER_DMAC",
                "SX_LAG_HASH_OUTER_ETHERTYPE",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_0",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_1",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_2",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_3",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_0",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_1",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_2",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_3",
                "SX_LAG_HASH_OUTER_IPV4_PROTOCOL",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_8",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_9",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_10",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_11",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_12",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_13",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_14",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_15",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_8",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_9",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_10",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_11",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_12",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_13",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_14",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_15",
                "SX_LAG_HASH_OUTER_IPV6_NEXT_HEADER",
                "SX_LAG_HASH_INNER_SMAC",
                "SX_LAG_HASH_INNER_DMAC",
                "SX_LAG_HASH_INNER_ETHERTYPE",
                "SX_LAG_HASH_INNER_IPV4_SIP_BYTE_0",
                "SX_LAG_HASH_INNER_IPV4_SIP_BYTE_1",
                "SX_LAG_HASH_INNER_IPV4_SIP_BYTE_2",
                "SX_LAG_HASH_INNER_IPV4_SIP_BYTE_3",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_0",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_1",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_2",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_3",
                "SX_LAG_HASH_INNER_IPV4_PROTOCOL",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTES_0_TO_7",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_8",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_9",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_10",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_11",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_12",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_13",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_14",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_15",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTES_0_TO_7",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_8",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_9",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_10",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_11",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_12",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_13",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_14",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_15"
            ]
        }
    }
}
```

#### Configuration random hashing for all ports
```json
{
    "lag_port_hash": {
        "all": {
            "hash_params": {
                "hash_type": "SX_LAG_HASH_TYPE_RANDOM"
            },
            "hash_fields_enable": [
            ],
            "hash_fields": [
            ]
        }
    }
}
```

#### Configuration for specific ports
```json
{
    "lag_port_hash": {
        "1": {
            "hash_params": {
                "hash_type": "SX_LAG_HASH_TYPE_CRC",
                "symmetric_hash": true,
                "seed": 98335670
            },
            "hash_fields_enable": [
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_NON_IP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_IPV6",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV4_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV4_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV6_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L4_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L4_IPV6",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L2_NON_IP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L2_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L2_IPV6",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV4_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV6_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV6_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L4_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L4_IPV6"            
            ],
            "hash_fields": [
                "SX_LAG_HASH_OUTER_SMAC",
                "SX_LAG_HASH_OUTER_DMAC",
                "SX_LAG_HASH_OUTER_ETHERTYPE",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_0",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_1",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_2",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_3",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_0",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_1",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_2",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_3",
                "SX_LAG_HASH_OUTER_IPV4_PROTOCOL",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_8",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_9",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_10",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_11",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_12",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_13",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_14",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_15",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_8",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_9",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_10",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_11",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_12",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_13",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_14",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_15",
                "SX_LAG_HASH_OUTER_IPV6_NEXT_HEADER",
                "SX_LAG_HASH_INNER_SMAC",
                "SX_LAG_HASH_INNER_DMAC",
                "SX_LAG_HASH_INNER_ETHERTYPE",
                "SX_LAG_HASH_INNER_IPV4_SIP_BYTE_0",
                "SX_LAG_HASH_INNER_IPV4_SIP_BYTE_1",
                "SX_LAG_HASH_INNER_IPV4_SIP_BYTE_2",
                "SX_LAG_HASH_INNER_IPV4_SIP_BYTE_3",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_0",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_1",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_2",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_3",
                "SX_LAG_HASH_INNER_IPV4_PROTOCOL",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTES_0_TO_7",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_8",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_9",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_10",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_11",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_12",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_13",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_14",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_15",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTES_0_TO_7",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_8",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_9",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_10",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_11",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_12",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_13",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_14",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_15"
            ]
        },
        "2": {
            "hash_params": {
                "hash_type": "SX_LAG_HASH_TYPE_CRC",
                "symmetric_hash": true,
                "seed": 98335670
            },
            "hash_fields_enable": [
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_NON_IP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_IPV6",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV4_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV4_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV6_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L4_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_OUTER_L4_IPV6",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L2_NON_IP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L2_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L2_IPV6",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV4_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV6_NON_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_IPV6_TCP_UDP",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L4_IPV4",
                "SX_LAG_HASH_FIELD_ENABLE_INNER_L4_IPV6"            
            ],
            "hash_fields": [
                "SX_LAG_HASH_OUTER_SMAC",
                "SX_LAG_HASH_OUTER_DMAC",
                "SX_LAG_HASH_OUTER_ETHERTYPE",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_0",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_1",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_2",
                "SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_3",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_0",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_1",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_2",
                "SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_3",
                "SX_LAG_HASH_OUTER_IPV4_PROTOCOL",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_8",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_9",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_10",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_11",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_12",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_13",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_14",
                "SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_15",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_8",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_9",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_10",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_11",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_12",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_13",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_14",
                "SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_15",
                "SX_LAG_HASH_OUTER_IPV6_NEXT_HEADER",
                "SX_LAG_HASH_INNER_SMAC",
                "SX_LAG_HASH_INNER_DMAC",
                "SX_LAG_HASH_INNER_ETHERTYPE",
                "SX_LAG_HASH_allINNER_IPV4_SIP_BYTE_2",
                "SX_LAG_HASH_INNER_IPV4_SIP_BYTE_3",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_0",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_1",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_2",
                "SX_LAG_HASH_INNER_IPV4_DIP_BYTE_3",
                "SX_LAG_HASH_INNER_IPV4_PROTOCOL",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTES_0_TO_7",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_8",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_9",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_10",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_11",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_12",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_13",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_14",
                "SX_LAG_HASH_INNER_IPV6_SIP_BYTE_15",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTES_0_TO_7",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_8",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_9",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_10",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_11",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_12",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_13",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_14",
                "SX_LAG_HASH_INNER_IPV6_DIP_BYTE_15"
            ]
        }
    }
}
```

## Supported LAG Hash types

**enum sx_lag_hash_type**
- SX_LAG_HASH_TYPE_CRC 	
- SX_LAG_HASH_TYPE_XOR 	
- SX_LAG_HASH_TYPE_RANDOM 	
- SX_LAG_HASH_TYPE_CRC2 	

## Supported LAG Hash fields

### Legacy global LAG Hash mode

**enum sx_lag_hash_bit_number**
sx_lag_hash_bit_number_t enum is used for indicating bit numbers of the hash flow parameters setting in API sx_api_lag_hash_flow_params_set:

- SX_LAG_HASH_INGRESS_PORT 
- SX_LAG_HASH_SMAC_IP 
- SX_LAG_HASH_SMAC_NON_IP 
- SX_LAG_HASH_DMAC_IP 
- SX_LAG_HASH_DMAC_NON_IP 
- SX_LAG_HASH_ETHER_IP 
- SX_LAG_HASH_ETHER_NON_IP 
- SX_LAG_HASH_VID_IP 
- SX_LAG_HASH_VID_NON_IP 
- SX_LAG_HASH_S_IP 
- SX_LAG_HASH_D_IP 
- SX_LAG_HASH_L4_SPORT 
- SX_LAG_HASH_L4_DPORT 
- SX_LAG_HASH_L3_PROTO 
- SX_LAG_HASH_IPV6_FLOW_LABEL 
- SX_LAG_HASH_SID 
- SX_LAG_HASH_DID 
- SX_LAG_HASH_OXID 
- SX_LAG_HASH_D_QP 

### New port-based LAG Hash mode

#### hash_fields_enable

**enum sx_lag_hash_field_enable**
- SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_NON_IP 
- SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_IPV4 
- SX_LAG_HASH_FIELD_ENABLE_OUTER_L2_IPV6 
- SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV4_NON_TCP_UDP 
- SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV4_TCP_UDP 
- SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV6_NON_TCP_UDP 
- SX_LAG_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP 
- SX_LAG_HASH_FIELD_ENABLE_OUTER_L4_IPV4 
- SX_LAG_HASH_FIELD_ENABLE_OUTER_L4_IPV6 
- SX_LAG_HASH_FIELD_ENABLE_OUTER_FIRST 
- SX_LAG_HASH_FIELD_ENABLE_INNER_L2_NON_IP 
- SX_LAG_HASH_FIELD_ENABLE_INNER_L2_IPV4 
- SX_LAG_HASH_FIELD_ENABLE_INNER_L2_IPV6 
- SX_LAG_HASH_FIELD_ENABLE_INNER_IPV4_NON_TCP_UDP 
- SX_LAG_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP 
- SX_LAG_HASH_FIELD_ENABLE_INNER_IPV6_NON_TCP_UDP 
- SX_LAG_HASH_FIELD_ENABLE_INNER_IPV6_TCP_UDP 
- SX_LAG_HASH_FIELD_ENABLE_INNER_L4_IPV4 
- SX_LAG_HASH_FIELD_ENABLE_INNER_L4_IPV6 

#### hash_fields

**enum sx_lag_hash_field**
sx_lag_hash_field_t enumerated type is used to store the specific layer fields and fields that should be included in the hash calculation, for both the outer header and the inner header.

- SX_LAG_HASH_OUTER_SMAC 	
- SX_LAG_HASH_OUTER_DMAC 	
- SX_LAG_HASH_OUTER_ETHERTYPE 	
- SX_LAG_HASH_OUTER_OVID 	
- SX_LAG_HASH_OUTER_OPCP
- SX_LAG_HASH_OUTER_ODEI
- SX_LAG_HASH_OUTER_IVID
- SX_LAG_HASH_OUTER_IPCP
- SX_LAG_HASH_OUTER_IDEI
- SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_0 	
- SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_1 	
- SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_2 	
- SX_LAG_HASH_OUTER_IPV4_SIP_BYTE_3 	
- SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_0 	
- SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_1 	
- SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_2 	
- SX_LAG_HASH_OUTER_IPV4_DIP_BYTE_3 	
- SX_LAG_HASH_OUTER_IPV4_PROTOCOL 	
- SX_LAG_HASH_OUTER_IPV4_DSCP 	
- SX_LAG_HASH_OUTER_IPV4_ECN 	
- SX_LAG_HASH_OUTER_IPV4_IP_L3_LENGTH 	
- SX_LAG_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7 	
- SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_8 	
- SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_9 	
- SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_10 	
- SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_11 	
- SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_12 	
- SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_13 	
- SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_14 	
- SX_LAG_HASH_OUTER_IPV6_SIP_BYTE_15 	
- SX_LAG_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7 	
- SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_8 	
- SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_9 	
- SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_10 	
- SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_11 	
- SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_12 	
- SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_13 	
- SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_14 	
- SX_LAG_HASH_OUTER_IPV6_DIP_BYTE_15 	
- SX_LAG_HASH_OUTER_IPV6_NEXT_HEADER 	
- SX_LAG_HASH_OUTER_IPV6_DSCP 	
- SX_LAG_HASH_OUTER_IPV6_ECN 	
- SX_LAG_HASH_OUTER_IPV6_IP_L3_LENGTH 	
- SX_LAG_HASH_OUTER_IPV6_FLOW_LABEL 	
- SX_LAG_HASH_OUTER_MPLS_LABEL_0 	
- SX_LAG_HASH_OUTER_MPLS_LABEL_1 	
- SX_LAG_HASH_OUTER_MPLS_LABEL_2 	
- SX_LAG_HASH_OUTER_MPLS_LABEL_3 	
- SX_LAG_HASH_OUTER_MPLS_LABEL_4 	
- SX_LAG_HASH_OUTER_MPLS_LABEL_5 	
- SX_LAG_HASH_OUTER_TCP_UDP_SPORT 	
- SX_LAG_HASH_OUTER_TCP_UDP_DPORT 	
- SX_LAG_HASH_OUTER_BTH_DQPN 	
- SX_LAG_HASH_OUTER_BTH_PKEY 	
- SX_LAG_HASH_OUTER_BTH_OPCODE 	
- SX_LAG_HASH_OUTER_DETH_QKEY 	
- SX_LAG_HASH_OUTER_DETH_SQPN 	
- SX_LAG_HASH_OUTER_VNI 	
- SX_LAG_HASH_OUTER_NVGRE_FLOW 	
- SX_LAG_HASH_OUTER_NVGRE_PROTOCOL	
- SX_LAG_HASH_INNER_SMAC 	
- SX_LAG_HASH_INNER_DMAC 	
- SX_LAG_HASH_INNER_ETHERTYPE 	
- SX_LAG_HASH_INNER_IPV4_SIP_BYTE_0 	
- SX_LAG_HASH_INNER_IPV4_SIP_BYTE_1 	
- SX_LAG_HASH_INNER_IPV4_SIP_BYTE_2 	
- SX_LAG_HASH_INNER_IPV4_SIP_BYTE_3 	
- SX_LAG_HASH_INNER_IPV4_DIP_BYTE_0 	
- SX_LAG_HASH_INNER_IPV4_DIP_BYTE_1 	
- SX_LAG_HASH_INNER_IPV4_DIP_BYTE_2 	
- SX_LAG_HASH_INNER_IPV4_DIP_BYTE_3 	
- SX_LAG_HASH_INNER_IPV4_PROTOCOL 	
- SX_LAG_HASH_INNER_IPV6_SIP_BYTES_0_TO_7 	
- SX_LAG_HASH_INNER_IPV6_SIP_BYTE_8 	
- SX_LAG_HASH_INNER_IPV6_SIP_BYTE_9 	
- SX_LAG_HASH_INNER_IPV6_SIP_BYTE_10 	
- SX_LAG_HASH_INNER_IPV6_SIP_BYTE_11 	
- SX_LAG_HASH_INNER_IPV6_SIP_BYTE_12 	
- SX_LAG_HASH_INNER_IPV6_SIP_BYTE_13 	
- SX_LAG_HASH_INNER_IPV6_SIP_BYTE_14 	
- SX_LAG_HASH_INNER_IPV6_SIP_BYTE_15 	
- SX_LAG_HASH_INNER_IPV6_DIP_BYTES_0_TO_7 	
- SX_LAG_HASH_INNER_IPV6_DIP_BYTE_8 	
- SX_LAG_HASH_INNER_IPV6_DIP_BYTE_9 	
- SX_LAG_HASH_INNER_IPV6_DIP_BYTE_10 	
- SX_LAG_HASH_INNER_IPV6_DIP_BYTE_11 	
- SX_LAG_HASH_INNER_IPV6_DIP_BYTE_12 	
- SX_LAG_HASH_INNER_IPV6_DIP_BYTE_13 	
- SX_LAG_HASH_INNER_IPV6_DIP_BYTE_14 	
- SX_LAG_HASH_INNER_IPV6_DIP_BYTE_15 	
- SX_LAG_HASH_INNER_IPV6_NEXT_HEADER 	
- SX_LAG_HASH_INNER_IPV6_FLOW_LABEL 	
- SX_LAG_HASH_INNER_TCP_UDP_SPORT 	
- SX_LAG_HASH_INNER_TCP_UDP_DPORT 	
- SX_LAG_HASH_INNER_ROCE_BTH_DQPN 	
- SX_LAG_HASH_INNER_ROCE_BTH_PKEY 	
- SX_LAG_HASH_INNER_ROCE_BTH_OPCODE 	
- SX_LAG_HASH_INNER_ROCE_DETH_QKEY 	
- SX_LAG_HASH_INNER_ROCE_DETH_SQPN 		
- SX_LAG_HASH_GENERAL_FIELDS_INGRESS_PORT 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_0 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_1 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_2 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_3 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_4 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_5 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_6 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_7 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_8 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_9 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_10 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_11 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_12 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_13 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_14 	
- SX_LAG_HASH_GENERAL_FIELDS_CUSTOM_BYTE_15 	
 