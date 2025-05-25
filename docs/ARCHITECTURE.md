# Access Control Simulation Suite - Architecture

## Overview

This system provides a comprehensive simulation of modern access control systems with:

- **Zero Trust Architecture** implementation
- **Risk-Based Adaptive Authentication**
- **Policy Conflict Resolution**
- **Real-Time Threat Detection**
- **Professional API Design**

## Components

### 1. Policy Decision Point (PDP)

The core authorization engine that evaluates access requests against policies using:

- Multiple combining algorithms (deny-overrides, permit-overrides, first-applicable)
- Attribute-based conditions
- Temporal constraints

### 2. Policy Administration Point (PAP)

Management interface for:

- CRUD operations on policies
- Policy versioning
- Conflict detection

### 3. Policy Information Point (PIP)

Gathers additional context for decisions:

- User attributes
- Resource metadata
- Environmental factors (location, time, device)

### 4. Policy Enforcement Point (PEP)

API gateway that:

- Intercepts requests
- Gathers context
- Enforces PDP decisions

## Data Flow

1. User makes request → PEP intercepts
2. PEP gathers context → PIP provides additional attributes
3. PDP evaluates request against policies
4. Threat detector analyzes patterns
5. PEP enforces decision
6. Audit logger records event