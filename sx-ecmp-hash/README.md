# sx-ecmp-hash
A script to configure custom ECMP Hash parameters for Mellanox Spectrum Switches using
Mellanox SX SDK API.

# Requirements
Mellanox Spectrum Switches running NOS with SDK API access:
- Onyx
- Cumulus
- SONiC

## Install
Copy this `sx_ecmp_hash.py` to Mellanox switch in an environment with SDK API access.

For example, a [docker container with SDK libs](https://community.mellanox.com/s/article/getting-started-with-docker-container-over-mlnx-os-sdk-interfaces) in Onyx.

Then create ECMP hash configuration file: `vi /etc/sx_hash/sx_ecmp_hash.json`

# Usage
This script reads custom ECMP hash configuration from `/etc/sx_hash/sx_ecmp_hash.json` file and applies new ECMP Hash parameters using Mellanox SX SDK API.

## Docker build
You can also create a docker image with this script inside to be launched on container start.

To create a docker image run: `./build.sh <VERSION>`

Example:
```
$ git clone https://github.com/kvadrage/sx-hash-examples/
$ cd sx-hash-examples/sx-ecmp-hash
$ ./build.sh 0.1
Sending build context to Docker daemon  56.32kB
Step 1/6 : FROM ubuntu:bionic
 ---> 72300a873c2c
Step 2/6 : RUN apt update && apt --no-install-recommends -y install python
 ---> Running in 30a514d9d07a
<...>
Successfully built dc4f5dd2ea05
Successfully tagged sx-ecmp-hash:0.1
$ ls sx_ecmp_hash_0.1.tar.gz 
sx_ecmp_hash_0.1.tar.gz
```

## Running Docker container in Onyx
Example how to run a docker image with this script inside Mellanox Onyx:

```
sw1 [standalone: master] (config) # image fetch scp://user@x.x.x.x/home/user/sx_ecmp_hash_0.1.tar.gz
Password (if required): *******
 100.0%  [#################################################################]  
sw1 [standalone: master] (config) # docker 
sw1 [standalone: master] (config docker) # no shutdown
sw1 [standalone: master] (config docker) # load sx_ecmp_hash_0.1.tar.gz 
cc4590d6a718: Loading layer  65.58MB/65.58MB
8c98131d2d1d: Loading layer  991.2kB/991.2kB
03c9b9f537a4: Loading layer  15.87kB/15.87kB
1852b2300972: Loading layer  3.072kB/3.072kB
772ff43086fb: Loading layer  59.08MB/59.08MB
19be54c09e5f: Loading layer  14.85kB/14.85kB
acfe33f3edee: Loading layer  3.584kB/3.584kB
Loaded image: sx-ecmp-hash:0.1

# run temporary container and copy SX SDK API libraries into it
sw1 [standalone: master] (config docker) # start sx-ecmp-hash 0.1 sx-ecmp-hash-temp now privileged sdk
Attempting to start docker container. Please wait (this can take a minute)...
sw1 [standalone: master] (config docker) # copy-sdk sx-ecmp-hash-temp to /
Copying SDK files to docker container. Please wait (this can take a minute)...

# commit these changes and create final image with SX SDK libraries inside
sw1 [standalone: master] (config docker) # commit sx-ecmp-hash-temp sx-ecmp-hash-sdk 0.1
committing docker container. Please wait (this can take a minute)...

# run new container from the final image and enable autostart for it
sw1 [standalone: master] (config docker) # start sx-ecmp-hash-sdk 0.1 sx-ecmp-hash now-and-init privileged sdk
Attempting to start docker container. Please wait (this can take a minute)...

# remove the temporary container from configuration
sw1 [standalone: master] (config docker) # no start sx-ecmp-hash-temp 
Stopping docker container. Please wait (this can take a minute)...
sw1 [standalone: master] (config docker) # exit
sw1 [standalone: master] (config) # wr mem
sw1 [standalone: master] (config) # 


# Verifying that container with sx-ecmp-hash script correctly starts after switch boot
sw1 [standalone: master] (config) # reload
## Reconnect to switch after it's booted
sw1 [standalone: master] > en
sw1 [standalone: master] # conf t
sw1 [standalone: master] (config) # show docker ps
-------------------------------------------------------------------------------------------
Container           Image:Version           Created                Status                  
-------------------------------------------------------------------------------------------
sx-ecmp-hash        sx-ecmp-hash-sdk:0.1    8 minutes ago          Exited (0) 2 minutes ago
sw1 [standalone: master] (config) # 
```

## Considerations
There're two different ECMP Hash configuration modes upported in Mellanox SX SDK API for Spectrum switches:
- **Global configuration mode (legacy API)** - allows configuring only limited number of packet fields for ECMP hashing 
- **Port configuration mode (new API)** - allows very flexible ECMP Hash configuration with ~50 different packet fields for hashing

Cumulus Linux 3.x is using **Global configuration mode** by default.

> **IMPORTANT NOTE:** 
>
> Switching from Global mode to Port mode is supported.
>
> However, ***switching back from Port mode to Global mode is not supported***. Need to reboot the device or reload SDK.

## Configuration examples

You can find more examples [here](./examples/).

### Legacy global ECMP Hash mode

```json
{
    "router_global_hash": {
        "hash_params": {
            "hash_type": "SX_ROUTER_ECMP_HASH_TYPE_CRC",
            "symmetric_hash": false,
            "seed": 98335670
        },
        "hash_fields": [
            "SX_ROUTER_ECMP_HASH_SRC_IP",
            "SX_ROUTER_ECMP_HASH_DST_IP",
            "SX_ROUTER_ECMP_HASH_TCLASS",
            "SX_ROUTER_ECMP_HASH_FLOW_LABEL",
            "SX_ROUTER_ECMP_HASH_TCP_UDP",
            "SX_ROUTER_ECMP_HASH_TCP_UDP_SRC_PORT",
            "SX_ROUTER_ECMP_HASH_TCP_UDP_DST_PORT",
            "SX_ROUTER_ECMP_HASH_SMAC",
            "SX_ROUTER_ECMP_HASH_DMAC",
            "SX_ROUTER_ECMP_HASH_ETH_TYPE",
            "SX_ROUTER_ECMP_HASH_VID",
            "SX_ROUTER_ECMP_HASH_PCP",
            "SX_ROUTER_ECMP_HASH_DEI"
        ]
    }
}
```

### New per-port ECMP Hash mode

#### Configuration for all ports
```json
{
    "router_port_hash": {
        "all": {
            "hash_params": {
                "hash_type": "SX_ROUTER_ECMP_HASH_TYPE_CRC",
                "symmetric_hash": true,
                "seed": 98335670
            },
            "hash_fields_enable": [
                "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6",
                "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP",
                "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP",
                "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV4",
                "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV6"
            ],
            "hash_fields": [
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_8",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_9",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_10",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_11",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_12",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_13",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_14",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_15",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_8",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_9",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_10",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_11",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_12",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_13",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_14",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_15",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_NEXT_HEADER",
                "SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_0",
                "SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_1",
                "SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_2",
                "SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_3",
                "SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_0",
                "SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_1",
                "SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_2",
                "SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_3",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTES_0_TO_7",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_8",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_9",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_10",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_11",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_12",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_13",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_14",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_15",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTES_0_TO_7",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_8",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_9",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_10",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_11",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_12",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_13",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_14",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_15",
                "SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_SPORT",
                "SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_DPORT",
                "SX_ROUTER_ECMP_HASH_INNER_IPV4_PROTOCOL",
                "SX_ROUTER_ECMP_HASH_INNER_IPV6_NEXT_HEADER"
            ]
        }
    }
}
```


#### Configuration for specific ports
```json
{
    "router_port_hash": {
        "swp1": {
            "hash_params": {
                "hash_type": "SX_ROUTER_ECMP_HASH_TYPE_CRC",
                "symmetric_hash": true,
                "seed": 98335670
            },
            "hash_fields_enable": [
                "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6",
                "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP"
            ],
            "hash_fields": [
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_8",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_9",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_10",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_11",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_12",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_13",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_14",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_15",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_8",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_9",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_10",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_11",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_12",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_13",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_14",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_15",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL",
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_NEXT_HEADER"
            ]
        },
        "swp2": {
            "hash_params": {
                "hash_type": "SX_ROUTER_ECMP_HASH_TYPE_XOR",
                "symmetric_hash": false,
                "seed": 1
            },
            "hash_fields_enable": [
                "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6",
                "SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP"
            ],
            "hash_fields": [
                "SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL"          
            ]
        }
    }
}
```

## Supported ECMP Hash types
- SX_ROUTER_ECMP_HASH_TYPE_CRC 	
- SX_ROUTER_ECMP_HASH_TYPE_XOR 	
- SX_ROUTER_ECMP_HASH_TYPE_RANDOM	

## Supported ECMP Hash fields

### Legacy global ECMP Hash mode

**enum sx_router_ecmp_hash_bit**
sx_router_ecmp_hash_bit_t enumerated type is used to store router ECMP hash configuration bits.

- SX_ROUTER_ECMP_HASH_SRC_IP 	
- SX_ROUTER_ECMP_HASH_DST_IP 	
- SX_ROUTER_ECMP_HASH_TCLASS 	
- SX_ROUTER_ECMP_HASH_FLOW_LABEL 	
- SX_ROUTER_ECMP_HASH_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_TCP_UDP_SRC_PORT 	
- SX_ROUTER_ECMP_HASH_TCP_UDP_DST_PORT 	
- SX_ROUTER_ECMP_HASH_SMAC 	
- SX_ROUTER_ECMP_HASH_DMAC 	
- SX_ROUTER_ECMP_HASH_ETH_TYPE 	
- SX_ROUTER_ECMP_HASH_VID 	
- SX_ROUTER_ECMP_HASH_PCP 	
- SX_ROUTER_ECMP_HASH_DEI

### New port-based ECMP Hash mode

#### hash_fields_enable

**enum sx_router_ecmp_hash_field_enable**
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_NON_IP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_IPV4 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L2_IPV6 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV4_NON_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV4_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_NON_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_IPV6_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV4 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_OUTER_L4_IPV6 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_NON_IP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_IPV4 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L2_IPV6 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_NON_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV4_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV6_NON_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_IPV6_TCP_UDP 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV4 	
- SX_ROUTER_ECMP_HASH_FIELD_ENABLE_INNER_L4_IPV6 	

#### hash_fields

**enum sx_router_ecmp_hash_field**
sx_router_ecmp_hash_field_t enumerated type is used to store the specific layer fields and fields that should be included in the hash calculation, for both the outer header and the inner header.

- SX_ROUTER_ECMP_HASH_OUTER_SMAC 	
- SX_ROUTER_ECMP_HASH_OUTER_DMAC 	
- SX_ROUTER_ECMP_HASH_OUTER_ETHERTYPE 	
- SX_ROUTER_ECMP_HASH_OUTER_OVID 	            < Outer VID>
- SX_ROUTER_ECMP_HASH_OUTER_OPCP 	            < Outer PCP>
- SX_ROUTER_ECMP_HASH_OUTER_ODEI 	            < Outer DEI>
- SX_ROUTER_ECMP_HASH_OUTER_IVID 	            < Inner VID>            
- SX_ROUTER_ECMP_HASH_OUTER_IPCP 	            < Inner PCP>            
- SX_ROUTER_ECMP_HASH_OUTER_IDEI 	            < Inner DEI>            
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_0 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_1 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_2 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_SIP_BYTE_3 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_0 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_1 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_2 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DIP_BYTE_3 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_PROTOCOL 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_DSCP 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_ECN 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV4_IP_L3_LENGTH 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTES_0_TO_7 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_8 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_9 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_10 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_11 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_12 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_13 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_14 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_SIP_BYTE_15 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTES_0_TO_7 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_8 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_9 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_10 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_11 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_12 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_13 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_14 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DIP_BYTE_15 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_NEXT_HEADER 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_DSCP 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_ECN 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_IP_L3_LENGTH 	
- SX_ROUTER_ECMP_HASH_OUTER_IPV6_FLOW_LABEL 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_SIP 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_DIP 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_NEXT_PROTOCOL 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_DSCP 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_ECN 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_L3_LENGTH 	
- SX_ROUTER_ECMP_HASH_OUTER_ROCE_GRH_FLOW_LABEL 	
- SX_ROUTER_ECMP_HASH_OUTER_FCOE_SID 	
- SX_ROUTER_ECMP_HASH_OUTER_FCOE_DID 	
- SX_ROUTER_ECMP_HASH_OUTER_FCOE_OXID 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_0 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_1 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_2 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_3 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_4 	
- SX_ROUTER_ECMP_HASH_OUTER_MPLS_LABEL_5 	
- SX_ROUTER_ECMP_HASH_OUTER_TCP_UDP_SPORT 	
- SX_ROUTER_ECMP_HASH_OUTER_TCP_UDP_DPORT 	
- SX_ROUTER_ECMP_HASH_OUTER_BTH_DQPN 	
- SX_ROUTER_ECMP_HASH_OUTER_BTH_PKEY 	
- SX_ROUTER_ECMP_HASH_OUTER_BTH_OPCODE 	
- SX_ROUTER_ECMP_HASH_OUTER_DETH_QKEY 	
- SX_ROUTER_ECMP_HASH_OUTER_DETH_SQPN 	
- SX_ROUTER_ECMP_HASH_OUTER_VNI 	
- SX_ROUTER_ECMP_HASH_OUTER_NVGRE_FLOW 	
- SX_ROUTER_ECMP_HASH_OUTER_NVGRE_PROTOCOL 	
- SX_ROUTER_ECMP_HASH_OUTER_LAST 	
- SX_ROUTER_ECMP_HASH_INNER_SMAC 	
- SX_ROUTER_ECMP_HASH_INNER_DMAC 	
- SX_ROUTER_ECMP_HASH_INNER_ETHERTYPE 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_0 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_1 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_2 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_SIP_BYTE_3 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_0 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_1 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_2 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_DIP_BYTE_3 	
- SX_ROUTER_ECMP_HASH_INNER_IPV4_PROTOCOL 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTES_0_TO_7 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_8 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_9 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_10 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_11 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_12 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_13 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_14 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_SIP_BYTE_15 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTES_0_TO_7 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_8 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_9 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_10 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_11 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_12 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_13 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_14 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_DIP_BYTE_15 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_NEXT_HEADER 	
- SX_ROUTER_ECMP_HASH_INNER_IPV6_FLOW_LABEL 	
- SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_SPORT 	
- SX_ROUTER_ECMP_HASH_INNER_TCP_UDP_DPORT 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_DQPN 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_PKEY 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_BTH_OPCODE 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_DETH_QKEY 	
- SX_ROUTER_ECMP_HASH_INNER_ROCE_DETH_SQPN 	
- SX_ROUTER_ECMP_HASH_INNER_LAST 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_INGRESS_PORT_NUMBER 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_0 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_1 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_2 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_3 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_4 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_5 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_6 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_7 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_8 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_9 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_10 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_11 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_12 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_13 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_14 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_15 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_CUSTOM_BYTE_LAST 	
- SX_ROUTER_ECMP_HASH_GENERAL_FIELDS_LAST 	
- SX_ROUTER_ECMP_HASH_MIN 	
- SX_ROUTER_ECMP_HASH_MAX 
