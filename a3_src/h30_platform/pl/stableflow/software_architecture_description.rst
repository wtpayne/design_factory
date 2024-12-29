============================================
Stableflow software architecture description
============================================


1. Scope
--------


1.1 Identification
^^^^^^^^^^^^^^^^^^

This software architecture description document
describes the Stableflow framework, a platform
for designing and operating distributed systems.

The stableflow framework is a core part of the 
"Design factory", an opinionated approach to the
design and development of software intensive
systems.

Design factory
  https://github.com/wtpayne/design_factory/

Stableflow
  https://github.com/wtpayne/design_factory/tree/main/a3_src/h30_platform/pl/stableflow


1.2 System overview
^^^^^^^^^^^^^^^^^^^

Stableflow is a framework for designing and operating
distributed systems. 

It is most suited to continuously operating systems
that can be easily described in terms of data flows
or data processing pipelines. Such systems include
sensor data processing, autonomous vehicle control,
business process automation, "digital twin" simulation,
and other similar data-intensive systems.

The framework enables:

* Model driven design
* Design workflow automation
* Product line engineering
* Deterministic simulation and re-simulation
* Automatic transformation of system architecture specifications
* Automatic optimization of system design parameters

It is conceptually similar to tools like Simulink,
Labview, or Ptolemy, but with a greater focus on
interoperability with modern ML/AI models and tools.

Key use cases include:

* Distributed "cyber-physical" systems
* Systems of cooperating "agents"
* Systems requiring rigorous testing and simulation
* Building families of related systems with shared architecture
* Projects where architectural exploration and optimization are key concerns
* Teams adopting model-driven development practices
* Projects requiring systematic validation across configurations

The framework is particularly valuable for:

* Early-stage technology demonstrators that need to be rapidly assembled
* Independent development of components towards design maturity
* Bridging gaps between research and product development teams
* Supporting automation of various aspects of the engineering process
* Enabling systems to make arguments about their safety and design decisions

The ideas behind stableflow have been developed 
since the late 2000s and early 2010s and are based
on experiences developing machine vision systems
for aerospace, automative and maritime autonomy
applications.

Experiences with using MATLAB, Simulink and rational
Rhapsody for model driven engineering highlighted 
some critical issues with these tools, including:

* Restrictions placed on system architecture and
  engineering team structure in order to work around
  the lack of support for usable textual diffing
  and merging of system designs in Simulink.
* Developers attempting to reverse engineer the
  model design from the desired generated code
  because of a lack of transparency and direct
  developer control over the generated code in
  both Rhapsody and Simulink.
* Difficulty in integrating the latest technical
  developments from the public domain due to
  the awkwardness of Python/MATLAB inter-operability.
* Administrative overhead associated with licensing
  and compliance for MATLAB and Simulink.
* RSI due to the heavy use of mouse-based interaction
  in Simulink.

On the other hand, attempting to do away with MDE
tools like Simulink and Rhapsody, coding directly
in C++ highlighted a different set of issues, including:

* Difficulty in communicating the architectural
  design to non-technical stakeholders without a
  "native" graphical representation. 
* Lack of support for simulation or resimulation
  making testing exceedingly difficult.
* Lack of a systematic approach to component composition
  and the generation of system variants for testing
  and simulation.

These experiences and lessons learned have informed
the development of Stableflow, which is mainly
intended to provide some of the benefits of MDE
without these drawbacks. Initially envisaged as
a sort of "Simulink-but-for-Python", as it has
developed, certain design decisions have pointed
towards a slightly more refined approach to MDE.

TODO: Discuss the influence of spinnaker, and the
      idea of the model as the equivalent of an
      HDL netlist, emphasiszing the importance of
      model transformations to achieve engineering
      goals.

TODO: Discuss automated / search-based optimization
      and the use of model transformations to help
      achieve this.

TODO: Discuss future plans for the project.


1.3 Document overview
^^^^^^^^^^^^^^^^^^^^^

This document describes the software architecture
of the Stableflow framework, including its approach,
design decisions, rationale, and tradeoffs. It
provides diagrams and text documenting various
architectural views and serves as the basis for
detailed design.

This document follows the Software Architecture 
Description template as specified in the Software
Development Standard for Mission Critical Systems
(SDSMCS).

This document is released into the public domain
under the Apache license, version 2.0.

License
  http://www.apache.org/licenses/LICENSE-2.0


1.4 Relationship to other documents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This SAD is related to the following documents:
* Requirements Specification: Defines the system requirements that drive the architecture
* Writing Style Guide: Provides documentation standards
* Glossary: Defines key terms and concepts


2. Referenced documents
-----------------------

* IEEE 1016-2009 - Software Design Description standard
* Kahn, G.: The semantics of a simple language for parallel programming
* Hewitt et al.: A universal modular ACTOR formalism for artificial intelligence
* Hoare, C.A.R.: Communicating Sequential Processes
* Stableflow Requirements Specification
* Stableflow Writing Style Guide
* Stableflow Glossary


3. Software architecture plans and processes
--------------------------------------------


3.1 Software architecture plans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stableflow is part of the design factory project. 
The design factory seeks to explore how highly 
automated systems design techniques can be applied 
to product development and contract systems
engineering.

Stableflow provides a simulation engine and
development platform that enbables and facilitates
the development automation techniques of the
design factory.

Both stableflow and the design factory are open
source projects started by myself (W. Payne) and
developed and maintained by the stableflow team. 

The design factory is being developed organically 
and iteratively. Whenever possible, it is used to 
solve real problems, and the lessons learned are
used to improve and extend the software with the 
goal of building a transformational capability 
over time.


3.2 Software architecture processes and tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The architecture is developed using:

* Python as the rapid development language
* C++ for performance critical components
* YAML, JSON, XML or TOML for configuration

The design factory is being developed alongside
stableflow, so processes and tools are being
bootstrapped as the project progresses. Processes
are documented in the design factory repository
under a3_src/h90_internal/processes.

Tools for process automation are considered
to be part of the design factory project, and
systems for continuous integration, continuous
test and other forms of design and development
automation are generally implemented using the
stableflow framework itself, dogfooding and
bootstrapping the design factory capability as
the project progresses.

TODO: Create an initial draft of a Software Development Plan
TODO: Decide how the stableflow architecture
      is documented.
TODO: Decide how consistency analysis is performed.
TODO: Decide how requirements are mapped to 
      architectural components. This will be done
      using controlled item identifiers as defined 
      in a3_src/h10_resource/registry/idclass.register.yaml
TODO: Describe how stableflow architecture design
      decisions flow down from high level requirements
      and high level design decisions down to lower
      level requirements and design decisions.
TODO: Decide what the scope of the stableflow 
      architecture is.


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
* Support for multiple computational models
* Separation of core engine from advanced features


4.2 Software architecture approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The architecture follows these key principles:

* Minimal Engine: Core platform provides only essential capabilities

  * Basic lifecycle management (Start/Stop/Step)
  * Deterministic message passing (Kahn process network model)
  * Nondeterministic message passing (Actor model)
  * Allocation of responsibility for resource management

* Model Transformation: System functionality implemented through

  * Configuration generation/modification
  * Node composition and connection
  * Edge implementation selection

* Application Layer Features: Complex capabilities built as transformations

  * Testing and monitoring
  * Deployment variants
  * Performance optimization
  * Debug support

* Separation of Concerns:

  * Engine: Message passing and lifecycle
  * Model: System structure and behavior
  * Transformations: Feature implementation


4.3 Software architecture evaluations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Architecture evaluation focuses on:

* Deterministic execution capabilities
* System variant generation effectiveness
* Testing and simulation support
* Performance and scalability
* Security and reliability

Evaluation methods include:

* Model checking for deterministic behavior
* Performance testing of message passing
* Scalability testing of transformations
* Security analysis of distributed components


4.4 Software architecture risks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Key risks include:

* Memory management in Kahn Process Networks
* Network reliability in distributed deployments
* Scalability of model transformations
* Complexity of system variant management
* Security in distributed environments


5. Overall software architecture description
--------------------------------------------


The software architecture is developed following 
a layered approach with clear separation of concerns:

* Core Engine Layer: Provides minimum essential capabilities

  * Message passing infrastructure
  * Node lifecycle management

* Model Layer: Defines base system structure and behavior

  * Definition of system data-flow topology
  * Definition of data types for serialization and deserialization
  * Definition of runtime environments for deployment
  * Allocation of design parameters to individual nodes
  * Allocation of concrete implementations to individual nodes
  * Allocation of nodes to Processes
  * Allocation of processes to hosts
  * Allocation of labels to nodes and edges

* Transformation Layer: Defines system variant structure and behavior

  * Programmatic generation of development and testing variants 
  * Programmatic generation of product line variants
  * Numerical optimisation of design parameters of individual nodes
  * Numerical optimisation of system-wide parameters



The Stableflow architecture is built around these core concepts:

* System: The highest level entity representing the system of interest
* Host: Physical or virtual processor running execution contexts
* Process: Sequential execution context running on a host
* Node: Basic computational unit processing data
* Edge: Connection carrying data between nodes
* Functional Chain: Connected sequence of nodes implementing specific features

Component Views:

1. Logical View:

   * System Component: Orchestrates overall execution and system-level commands
   * Host Component: Manages local resources, processes, and inter-process communications
   * Process Component: Provides execution context and main loop for independently running processes
   * Node Component: Processes data and manages queue interfaces
   * Edge Component: Manages data flow
   * Configuration Component: Handles reading, writing, and enrichment of configuration data
   * Interface Generator: Generates serialization/deserialization logic
   * Queue Handler: Provides consistent queue interfaces across different implementations

2. Process View:

   * Main System Process: Coordinates overall execution
   * Node Processes: Execute node implementations
   * Monitor Process: System observation and control

3. Physical View:

   * Same Process Communication: Direct memory transfer
   * Inter-Process Communication: Shared memory queues
   * Inter-Host Communication: Network protocols (e.g., ZeroMQ)

4. Development View:

   * Core Engine Implementation
   * Model Transformation Tools
   * Configuration Management
   * Testing Infrastructure

Configuration Structure:

The system configuration is hierarchical with six main sections:

* system: System-wide configuration settings
* host: Maps host IDs to host-specific configurations
* process: Maps process IDs to process-specific configurations
* node: Maps node IDs to node-specific configurations
* edge: List of edge configurations defining connectivity
* data: Maps type IDs to data type specifications

This structure is designed to minimize merge conflicts in branch-and-merge engineering processes,
with changes to containment structure and connectivity requiring minimal, localized changes.

System Lifecycle::

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
   * Nodes communicate through unbounded FIFO channels
   * Reading blocks until data available
   * Writing never blocks
   * Guarantees deterministic behavior

2. Actor Model (Planned):

   * Non-deterministic behavior
   * Higher performance
   * Suitable for production systems
   * Asynchronous message passing
   * Non-blocking operations

3. CSP Model (Under Consideration):

   * Synchronized communication
   * Suitable for tightly coupled processes
   * Blocking read/write operations
   * Direct node-to-node communication


6. Software item architecture description
-----------------------------------------


6.1 Core Engine
^^^^^^^^^^^^^^^

The core engine provides:

* Message Passing Infrastructure:

  * Direct memory transfer (same process)
  * Shared memory queues (different processes)
  * Network communication (different hosts)
  * Support for multiple queue implementations via adapters

* Node Lifecycle Management:

  * Configuration
  * Reset
  * Run
  * Pause
  * Stop
  * Data persistence between steps

* Resource Coordination:

  * Process allocation
  * Memory management
  * Network resources
  * Remote process deployment via SSH

* Basic State Management:

  * Input message buffers
  * Output message buffers
  * Implementation state container
  * Recording and replay capabilities


6.2 Model Layer
^^^^^^^^^^^^^^^

The model layer handles:

* System Topology Definition:

  * Node definitions (inputs/outputs)
  * Edge connections
  * Process assignments
  * Host mappings

* Configuration Management:

  * Node implementation references
  * Edge implementation selection
  * Data type specifications

* State Management:

  * Recording nodes
  * Replay nodes
  * Monitor nodes
  * Checkpoint nodes


6.3 Transformation Layer
^^^^^^^^^^^^^^^^^^^^^^^^

The transformation layer enables:

* System Variant Generation:

  * Development variants
  * Test variants
  * Production variants

* Testing and Monitoring:

  * Data capture
  * Playback
  * State inspection
  * Performance monitoring

* Debug Support:

  * Step execution
  * State inspection
  * Error handling
  * Logging


7. Notes
--------


7.1 Abbreviations and acronyms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* KPN: Kahn Process Network
* CSP: Communicating Sequential Processes
* SOI: System of Interest
* SAD: Software Architecture Description
* MDD: Model Driven Development
* PLE: Product Line Engineering


7.2 Glossary
^^^^^^^^^^^^

See separate Stableflow Glossary document for detailed 
term definitions.


7.3 General information
^^^^^^^^^^^^^^^^^^^^^^^

The architecture is designed to be extensible through 
model transformations while maintaining a minimal 
core engine. This approach enables both system 
flexibility and maintainability.


A. Appendices
-------------


A.1 Example Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^

See example configuration files in the codebase
for reference implementations.


A.2 Implementation Examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simple Counter Node Example:

.. code-block:: python

    def step(inputs, state, outputs):
        if 'count' not in state:
            state['count'] = 0
        else:
            state['count'] += 1
        outputs['output']['count'] = state['count']
        return (None,)  # Continue signal 

