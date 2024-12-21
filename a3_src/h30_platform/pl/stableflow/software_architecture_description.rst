================================================
Software Architecture Description (SAD)
================================================


1. Scope
--------


1.1 Identification
^^^^^^^^^^^^^^^^^^

This Software Architecture Description (SAD) applies
to the Stableflow framework, a platform for designing
and operating distributed systems. The framework is
primarily implemented in Python and focuses on data
flow-oriented architectures.


1.2 System overview
^^^^^^^^^^^^^^^^^^^

Stableflow is a framework for designing and operating distributed systems, particularly suited for continuously operating systems composed of data flows or data processing pipelines. The framework enables:

* Model driven design
* Design workflow automation
* Product line engineering
* Deterministic simulation and re-simulation
* Automatic transformation of system architecture specifications
* Automatic optimization of system design parameters

It is conceptually similar to tools like Simulink, Labview, or Ptolemy, but with a greater focus on interoperability with modern ML/AI models and tools.

Key use cases include:
* Distributed "cyber-physical" systems
* Systems of cooperating "agents"
* Systems requiring rigorous testing and simulation
* Building families of related systems with shared architecture
* Projects where architectural exploration and optimization are key concerns


1.3 Document overview
^^^^^^^^^^^^^^^^^^^^^

This document describes the software architecture of the Stableflow framework, including its approach, design decisions, rationale, and tradeoffs. It provides diagrams and text documenting various architectural views and serves as the basis for detailed design.


1.4 Relationship to other documents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This SAD is related to the following documents:
* Software Design Description (SDD)
* Requirements Specification
* Writing Style Guide
* Glossary


2. Referenced documents
-----------------------

* Stableflow Requirements Specification
* Stableflow Software Design Description
* Stableflow Writing Style Guide
* Stableflow Glossary


3. Software architecture plans and processes
--------------------------------------------


3.1 Software architecture plans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The software architecture is developed following a layered approach with clear separation of concerns:

* Core Engine Layer: Provides essential capabilities
* Model Layer: Defines system structure and behavior
* Transformation Layer: Implements advanced features
* Application Layer: Implements specific system functionality


3.2 Software architecture processes and tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The architecture is developed using:
* Python as the primary implementation language
* YAML/JSON for configuration
* UML and similar diagrams for architecture representation
* Model transformation tools for system variant generation
* Testing and simulation infrastructure


4. Software architecture requirements and approach
--------------------------------------------------


4.1 Software architecture critical and driving requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Critical requirements:
* Support for distributed data flow systems
* Deterministic execution capability
* Model-driven development support
* System variant generation
* Rigorous testing and simulation support

Driving requirements:
* Message passing infrastructure
* Node lifecycle management
* Graph representation and manipulation
* Execution control primitives


4.2 Software architecture approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The architecture follows these key principles:

* Minimal Engine: Core platform provides only essential capabilities
* Model Transformation: System functionality implemented through configuration
* Application Layer Features: Complex capabilities built as transformations
* Separation of Concerns: Clear separation between engine, model, and transformations


4.3 Software architecture evaluations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Architecture evaluation focuses on:
* Deterministic execution capabilities
* System variant generation effectiveness
* Testing and simulation support
* Performance and scalability
* Security and reliability


4.4 Software architecture risks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Key risks include:
* Memory management in Kahn Process Networks
* Network reliability in distributed deployments
* Scalability of model transformations
* Complexity of system variant management


5. Overall software architecture description
--------------------------------------------

The Stableflow architecture is built around these core concepts:

* System: The highest level entity representing the system of interest
* Host: Physical or virtual processor running execution contexts
* Process: Sequential execution context running on a host
* Node: Basic computational unit processing data
* Edge: Connection carrying data between nodes
* Functional Chain: Connected sequence of nodes implementing specific features

Key architectural views:

Logical View:
┌──────────────────────┐
│                      │
│      Configure       │
│   (load settings)    │
│                      │
└───────────┬──────────┘
            │
            │ start
            │
            ▼
┌──────────────────────┐
│                      │
│        Reset         │
│ (allocate resources) │
│                      │
└───────────┬──────────┘
            │
            │ start
            │
            ▼
┌──────────────────────┐      pause     ┌───────────────┐
│                      │───────────────►│               │
│         Run          │                │     Pause     │
│     (main loop)      │◄───────────────│               │
│                      │     start      └──┬────────────┘
└───────────┬──────────┘                   │         ▲
            │                              │         │
            │ stop                         │  step   │
            │                              └─────────┘
            ▼
┌──────────────────────┐
│                      │
│         Stop         │
│  (cleanup/dispose)   │
│                      │
└──────────────────────┘

The architecture supports multiple computational models:

1. Kahn Process Networks (Primary):
   * Deterministic behavior
   * Non-blocking writes, blocking reads
   * Suitable for testing and simulation

2. Actor Model (Planned):
   * Non-deterministic behavior
   * Higher performance
   * Suitable for production systems

3. CSP Model (Under Consideration):
   * Synchronized communication
   * Suitable for tightly coupled processes


6. Software item architecture description
-----------------------------------------

6.1 Core Engine
^^^^^^^^^^^^^^^

The core engine provides:
* Message passing infrastructure
* Node lifecycle management
* Resource coordination
* Basic state management

6.2 Model Layer
^^^^^^^^^^^^^^^

The model layer handles:
* System topology definition
* Node and edge configuration
* Process and host assignments
* Implementation bindings

6.3 Transformation Layer
^^^^^^^^^^^^^^^^^^^^^^^

The transformation layer enables:
* System variant generation
* Testing and monitoring
* Performance optimization
* Debug support


7. Notes
--------


7.1 Abbreviations and acronyms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* KPN: Kahn Process Network
* CSP: Communicating Sequential Processes
* SOI: System of Interest
* SAD: Software Architecture Description
* SDD: Software Design Description


7.2 Glossary
^^^^^^^^^^^^

See separate Stableflow Glossary document for detailed term definitions.


7.3 General information
^^^^^^^^^^^^^^^^^^^^^^^

The architecture is designed to be extensible through model transformations while maintaining a minimal core engine. This approach enables both system flexibility and maintainability.


A. Appendices
-------------

A.1 Example Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^

See example configuration files in the codebase for reference implementations.

A.2 Implementation Examples
^^^^^^^^^^^^^^^^^^^^^^^^^

See software design description for detailed implementation examples. 