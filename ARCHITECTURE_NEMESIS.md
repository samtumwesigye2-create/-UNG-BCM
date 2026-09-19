# UNG-NEMESIS — Emergency Management Architecture

UNG-NEMESIS is the standalone emergency-management and incident-coordination system in the UNG portfolio.

## Command chain

UNG-PRESIDENT → ORION → NEMESIS

NEMESIS ↔ NEPTUNE for military-support coordination during emergencies. NEMESIS remains the emergency-management authority; NEPTUNE retains military command-and-control responsibilities.

## Integration backbone

- NEXUS — interoperability and service integration
- PULSAR — event/data relay
- JANUS — identity, authentication and role/clearance context
- VAULT — protected records and sensitive emergency information
- DRACO — intelligence and situational collection inputs
- CONSTELLATION — sensor/remote observation inputs
- HERMES — communications
- UGAMAP — location, routing and geographic support
- NOVA — analytics and recovery KPIs

## Executive integration contract

NEMESIS exposes executive-safe incident summaries upward to ORION/UNG-PRESIDENT. Executive interfaces do not replace NEMESIS incident operations.

## Military-support integration contract

NEMESIS may create, track, update and close military-support requests to NEPTUNE. Requests must carry a unique request ID, incident ID, requesting identity, timestamps, status and audit history. NEPTUNE response/command data remains under NEPTUNE authority.

## Security boundary

All integrations are authenticated through JANUS-derived identity/service authorization, sensitive records are protected through VAULT policy, and cross-system exchanges are routed through NEXUS/PULSAR where applicable. Auditability is mandatory for create/update/close/escalate actions.

## Naming

Product name: **UNG-NEMESIS**.
Legacy repository name `-UNG-BCM` is retained temporarily for source continuity; application-facing naming should use UNG-NEMESIS.
