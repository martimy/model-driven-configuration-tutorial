# NETCONF vs gNMI

NETCONF and gNMI embody distinct approaches to network management. NETCONF for traditional device-centric control and gNMI for modern, API-based automation.

## Design Philosophy

NETCONF is device-focused and built for structured configuration with transactional integrity and explicit datastore management.

gNMI, produced by the OpenConfig Working Group, centers on APIs, telemetry, streaming, and automation for distributed systems.

## Management Model

NETCONF structures device management as configuration retrieval, modification, commit, and datastore maintenance.

gNMI treats configuration as part of a broader data operation set—state, telemetry, and updates—with a focus on continuous visibility.

## Operational Focus

NETCONF prioritizes configuration accuracy with safety mechanisms and suits intent-based deployments.

gNMI excels in scalable data collection and real-time telemetry for observability and automation.

## System Integration Approach

NETCONF integrates with NMS and config management (e.g., orchestration, provisioning).

gNMI aligns with telemetry pipelines and modern automation platforms.

## Ecosystem Alignment

NETCONF: IETF standards, traditional tools, configuration platforms.

gNMI: Cloud-native tools, streaming telemetry, SDN infrastructure.

Both rely on YANG but apply it differently.

## Strategic Perspective

| Perspective           | NETCONF                       | gNMI                   |
|-----------------------|------------------------------|------------------------|
| Era                   | Post-CLI automation          | Cloud-scale automation |
| Primary goal          | Reliable configuration       | Scalable telemetry     |
| Mindset               | Network management           | Distributed APIs       |

## Takeaway

NETCONF excels at safe configuration management, while gNMI supports large-scale, telemetry-driven automation. They complement each other in modern networks.


