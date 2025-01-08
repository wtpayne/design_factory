







System Architecture
------------------

The system is composed of several key components that work together to distribute computational work across hardware resources:

1. **CLI Component**: Provides command-line control over systems, enabling start, stop, and pause functionality.

2. **System Controller**: Responsible for executing system-level commands, deploying logic to remote hosts, and managing inter-host channels.

3. **Host Controller**: Manages process host operations, configuring inter-process communications channels and process lifecycle.

4. **Process Controller**: Handles individual operating system processes, including the main execution loop and node scheduling.

5. **Node Controller**: Provides a wrapper around node logic, managing queue interfaces and data persistence between steps.

6. **Configuration Component**: Handles reading, writing, serialization, and enrichment of configuration data.

7. **Interface Generator**: Generates logic for serialization, deserialization, and validation based on configuration specs.

8. **Queue Handler**: Provides adapter classes for different queue implementations, ensuring consistent interfaces.


Configuration Structure
----------------------§

Systems can be configured either through configuration files or programmatically. The configuration structure is hierarchical with six main sections:

* **system**: System-wide configuration settings
* **host**: Maps host IDs to host-specific configurations
* **process**: Maps process IDs to process-specific configurations
* **node**: Maps node IDs to node-specific configurations
* **edge**: List of edge configurations defining connectivity
* **data**: Maps type IDs to data type specifications

Configuration can be provided in YAML, JSON, or XML formats. When using files, they should be named with appropriate extensions (.cfg.yaml, .cfg.json, or .cfg.xml).











======================================
Stableflow software design description
======================================


1. Introduction
---------------

This document provides a technical description of
the Stableflow framework

NOTE: This document is currently in DRAFT form. Many sections
are placeholders and will be expanded updated and corrected
as the document is reviewed and revised.


1.1 Purpose and Scope
^^^^^^^^^^^^^^^^^^^^^

This document provides the software design description
for Stableflow, a framework for designing and operating
distributed systems.

Stableflow is intended to enable and encourage:

* Model driven design
* Design workflow automation
* Product line engineering

To achieve this, it is designed to support:

* Deterministic simulation and re-simulation
* Automatic transformation of system architecture specifications
* Automatic optimisation of system design parameters

It is conceptually similar to tools like Simulink,
Labview or Ptolemy, but with a greater focus on
interoperability with today's ecosystem of ML/AI
models and tools.




1.3 Definitions and Acronyms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* SOI - System of Interest
* KPN - Kahn Process Network
* CSP - Communicating Sequential Processes
* MDD - Model Driven Development
* PLE - Product Line Engineering


1.4 References
^^^^^^^^^^^^^^

* IEEE 1016-2009 - Software Design Description standard
* Kahn, G.: The semantics of a simple language for parallel programming
* Hewitt et al.: A universal modular ACTOR formalism for artificial intelligence
* Hoare, C.A.R.: Communicating Sequential Processes


2. System Architecture
----------------------


2.1 Core Concepts
^^^^^^^^^^^^^^^^^

Stableflow's architecture is built around several 
foundational concepts:

* **System**: The highest level entity representing the system of interest as a whole.
* **Host**: A physical or virtual processor that can run one or more execution contexts.
* **Process**: A single sequential execution context running on a host.
* **Node**: The basic building block of system behavior, receiving and sending messages.
* **Node implementation**: The software that gives a node behaviour.
* **Edge**: Represents a flow of messages between nodes.
* **Functional chain**: Represents an interconnected sequence of nodes implementing a specific function.
* **Computational model**: An abstract model of concurrent computation.


2.2 Design Patterns and Principles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stableflow employs several key design patterns and principles:

* **Minimal Engine**: Core platform provides only essential capabilities:

  * Deterministic message passing (KPN)
  * Basic lifecycle management
  * Resource coordination

* **Model Transformation**: System functionality implemented through:

  * Configuration generation/modification
  * Node composition and connection
  * Edge implementation selection

* **Application Layer Features**: Complex capabilities built as transformations:

  * Testing and monitoring
  * Deployment variants
  * Performance optimization
  * Debug support

* **Separation of Concerns**:

  * Engine: Message passing and lifecycle
  * Model: System structure and behavior
  * Transformations: Feature implementation


2.3 System Context
^^^^^^^^^^^^^^^^^^

Stableflow operates within the context of:

* Development Environment:

  * Source code in various languages (primarily Python)
  * Build and deployment tools
  * Testing and simulation infrastructure

* Runtime Environment:

  * Operating system processes and threads
  * Network communication infrastructure
  * Hardware resources (CPU, memory, etc.)

* User Environment:

  * Command line interface
  * Configuration files
  * Monitoring and debugging tools


3. Detailed Design
------------------


3.1 Component Design
^^^^^^^^^^^^^^^^^^^^


System Component
""""""""""""""""

The System orchestrates the entire Stableflow SOI (System Of 
Interest). It manages the lifecycle of hosts and processes,
ensuring all components work together cohesively.

Key responsibilities:

* Starting and stopping the system
* Managing system-wide state
* Coordinating between hosts
* Handling system-level control signals


Host Component
""""""""""""""

A Host represents a physical or virtual processor capable of
running one or more execution contexts. Each host typically
corresponds to a single machine, device, or processor core.

Key responsibilities:

* Starting and stopping local processes
* Managing inter-process communication
* Managing local resources
* Handling control signals from the system


Process Component
"""""""""""""""""

A Process provides a single context of execution, running
nodes sequentially. Each process maps to either an operating
system process or thread (currently only OS processes are
supported).

Key responsibilities:

* Managing node execution order
* Handling inter-node communication
* Processing control signals
* Managing process-local resources


Node Component
""""""""""""""

A Node provides minimal functionality:

* Message buffer management
* Implementation invocation
* Basic lifecycle support

All higher-level capabilities (monitoring, testing, etc.) are
implemented by transforming the system model to insert
appropriate nodes.


Node Implementation
"""""""""""""""""""

Node implementations provide the actual behavior for nodes.
Currently supported in Python with two interface styles:

* **Functional**: Pure functions for lifecycle stages
* **Coroutine**: Generator functions for simpler state management


Edge Component
""""""""""""""

Edges represent message flows between nodes. Implementation
varies based on:

* Whether nodes are in same/different processes
* Whether nodes are on same/different hosts
* The computational model being used


3.2 Control Flow
^^^^^^^^^^^^^^^^


System Lifecycle
""""""""""""""""

The system progresses through several stages::

    ┌──────────────────────┐
    │                      │
    │      Configure       │
    │   (load settings)    │
    │                      │
    └───────────┬──────────┘
                │
                │ start (first part)
                │
                ▼
    ┌──────────────────────┐
    │                      │
    │        Reset         │
    │ (allocate resources) │
    │                      │
    └───────────┬──────────┘
                │
                │ start (second part)
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

Lifecycle Stages:

1. **Configure**: Process configuration data, instantiate components
2. **Reset**: Initialize all nodes and allocate resources
3. **Run**: Execute nodes according to computational model
4. **Pause**: Optional state for debugging/inspection
5. **Stop**: Cleanup and dispose of resources


Control Signals
"""""""""""""""

The system uses several types of control signals:

* **Continue**: Normal execution should proceed
* **Exit**: 

  * Immediate: Non-recoverable error, terminate immediately
  * Controlled: Graceful shutdown requested

* **Reset**: Return to initial state
* **Pause/Step**: Debug execution control


3.3 Data Flow
^^^^^^^^^^^^^


Message Passing
"""""""""""""""

Data flows between nodes through messages passed along edges.
The exact mechanism depends on node locations:

* Same Process: Direct memory transfer
* Different Processes: Shared memory queues
* Different Hosts: Network communication (e.g., ZeroMQ)


Flow Control
""""""""""""

Message flow is governed by the computational model in use:

* **Kahn Process Networks**:

  * Nodes block on reading until data available
  * Writing never blocks
  * Deterministic behavior guaranteed

* **Actor Model** (planned):

  * Non-blocking reads and writes
  * Higher performance but non-deterministic

* **CSP** (under consideration):

  * Synchronized communication
  * Both reader and writer must be ready


4. Data Design
--------------


4.1 Data Structures
^^^^^^^^^^^^^^^^^^^

The engine provides minimal core data structures, with additional
functionality implemented through model transformations.


Core Configuration Data
"""""""""""""""""""""""

Minimal configuration required by the engine:

* System topology:

  * Node definitions (inputs/outputs only)
  * Edge connections
  * Process assignments
  * Host mappings

* Implementation bindings:

  * Node implementation references
  * Edge implementation selection
  * Data type specifications

Extended configuration (e.g., for testing, monitoring, etc.) is
implemented through model transformations that augment this
basic structure.


Node State Management
"""""""""""""""""""""

Engine manages only essential node data:

* Input message buffers
* Output message buffers
* Implementation state container

Additional state management (e.g., checkpointing, debugging)
is implemented through transformed configurations that wrap
nodes with appropriate state management nodes.


4.2 Data Storage
^^^^^^^^^^^^^^^^


Engine Storage
""""""""""""""

Core engine only handles:

* In-memory message queues
* Basic node state
* Active configuration


Extended Storage
""""""""""""""""

Additional storage capabilities provided through transformations:

* Recording nodes for data capture
* Replay nodes for data playback
* Monitor nodes for state inspection
* Checkpoint nodes for state persistence


4.3 Computational Models
^^^^^^^^^^^^^^^^^^^^^^^^


Kahn Process Networks (Primary)
"""""""""""""""""""""""""""""""

* Deterministic concurrency model
* Nodes communicate through unbounded FIFO channels
* Reading blocks until data available
* Writing never blocks
* Guarantees deterministic behavior


Actor Model (Planned)
"""""""""""""""""""""

* Asynchronous message passing
* Non-blocking operations
* Higher performance
* Non-deterministic behavior


CSP Model (Under Consideration)
"""""""""""""""""""""""""""""""

* Synchronized communication
* Blocking read/write operations
* Direct node-to-node communication
* Suitable for tightly coupled processes


5. Interface Design
-------------------


5.1 External Interfaces
^^^^^^^^^^^^^^^^^^^^^^^


Command Line Interface
""""""""""""""""""""""

Primary user interface for system control:


.. code-block:: shell

    # System control
    stableflow system start --cfg-path /path/to/config
    stableflow system stop
    stableflow system pause
    stableflow system step


Configuration Interface
"""""""""""""""""""""""

* JSON/YAML configuration files
* Python-based configuration generation
* Runtime configuration modification (planned)


5.2 Internal Interfaces
^^^^^^^^^^^^^^^^^^^^^^^


Node Implementation Interface
"""""""""""""""""""""""""""""

Functional Interface:

.. code-block:: python

    def reset(runtime, cfg, inputs, state, outputs):
        """
        Initialize or reinitialize the node
        
        Args:
            runtime: Runtime support functions
            cfg: Node configuration
            inputs: Input message buffers
            state: Node state dictionary
            outputs: Output message buffers
        
        Returns:
            iter_signal: Control signal tuple
        """
        return iter_signal

    def step(inputs, state, outputs):
        """
        Perform one computational step
        
        Args:
            inputs: Input message buffers
            state: Node state dictionary
            outputs: Output message buffers
        
        Returns:
            iter_signal: Control signal tuple
        """
        return iter_signal

Coroutine Interface:

.. code-block:: python

    def coro(runtime, cfg, inputs, state, outputs):
        """
        Main node logic as a coroutine
        
        Args:
            runtime: Runtime support functions
            cfg: Node configuration
            inputs: Input message buffers
            state: Node state dictionary
            outputs: Output message buffers
        
        Yields:
            (outputs, iter_signal): Output messages and control signal
        
        Receives:
            inputs: Input messages for next step
        """
        while True:
            inputs = yield (outputs, iter_signal)


6. Component Implementation
---------------------------


6.1 Node Implementation
^^^^^^^^^^^^^^^^^^^^^^^


Implementation Approaches
"""""""""""""""""""""""""

1. Functional Implementation:

   * Separate functions for reset, step, finalize
   * Explicit state management
   * Simple to understand and port
   * Suitable for simple nodes

2. Coroutine Implementation:

   * Single generator function
   * Implicit state management
   * More natural control flow
   * Better for complex nodes


Example Implementations
"""""""""""""""""""""""

Simple Counter Node:

.. code-block:: python

    def step(inputs, state, outputs):
        if 'count' not in state:
            state['count'] = 0
        else:
            state['count'] += 1
        outputs['output']['count'] = state['count']
        return (None,)  # Continue signal


6.2 Edge Implementation
^^^^^^^^^^^^^^^^^^^^^^^


Implementation Types
""""""""""""""""""""

1. Intra-Process Edges:

   * Direct memory transfer
   * Lightweight queue implementation
   * No serialization needed

2. Inter-Process Edges:

   * Shared memory queues
   * System V IPC or similar
   * Basic serialization required

3. Inter-Host Edges:

   * Network communication (ZeroMQ)
   * Full serialization required
   * Network error handling


6.3 Process Management
^^^^^^^^^^^^^^^^^^^^^^


Process Types
"""""""""""""

* Main System Process: Coordinates overall execution
* Node Processes: Execute node implementations
* Monitor Process: System observation and control


Process Communication
"""""""""""""""""""""

* Control messages via system signals
* Data transfer via edges
* Status reporting via monitoring interface


7. Requirements Traceability
----------------------------


7.1 Functional Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^


Model-Driven Design Requirements
""""""""""""""""""""""""""""""""

* **MDD-1**: System architecture must be explicitly modeled

  * Implemented via configuration data structures
  * Supported by node/edge abstractions

* **MDD-2**: Architecture must be programmatically transformable

  * Configuration can be generated/modified by code
  * Node implementations can be swapped


Product Line Engineering Requirements
"""""""""""""""""""""""""""""""""""""

* **PLE-1**: Support multiple system variants from single design

  * Configuration-driven variant generation
  * Reusable node implementations
  * Flexible edge implementations

* **PLE-2**: Enable systematic testing across variants

  * Deterministic execution model
  * Replay capability
  * Common test infrastructure


Execution Requirements
""""""""""""""""""""""

* **EXEC-1**: Support distributed execution

  * Multi-host deployment
  * Network communication
  * Resource management

* **EXEC-2**: Enable deterministic simulation

  * Kahn Process Network model
  * Reproducible message passing
  * State management


7.2 Non-Functional Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Performance Requirements
""""""""""""""""""""""""

* **PERF-1**: Minimal overhead for local communication

  * Direct memory transfer within processes
  * Shared memory between processes
  * Zero-copy where possible

* **PERF-2**: Scalable distributed execution

  * Efficient network protocols
  * Parallel execution where possible
  * Resource-aware scheduling


Reliability Requirements
""""""""""""""""""""""""

* **REL-1**: Graceful error handling

  * Controlled shutdown capability
  * Error isolation between nodes
  * State recovery mechanisms

* **REL-2**: Deterministic behavior

  * Reproducible execution
  * Predictable resource usage
  * Consistent error handling


Maintainability Requirements
""""""""""""""""""""""""""""

* **MAINT-1**: Modular architecture

  * Clear component boundaries
  * Well-defined interfaces
  * Separation of concerns

* **MAINT-2**: Extensible design

  * Plugin architecture for node implementations
  * Support for new computational models
  * Configurable communication mechanisms


8. Testing Considerations
------------------------


8.1 Platform Testing
^^^^^^^^^^^^^^^^^^^^

Testing the Stableflow framework itself focuses on ensuring
the platform provides its core capabilities reliably.


Unit Testing
""""""""""""

* Node lifecycle management
* Edge implementation correctness
* Process control mechanisms
* Configuration processing
* Signal handling


Integration Testing
"""""""""""""""""""

* Inter-process communication
* Host coordination
* System lifecycle management
* Computational model implementations


System Testing
""""""""""""""

* End-to-end platform functionality
* Performance overhead measurement
* Resource management
* Error handling and recovery


8.2 SOI Testing Support
^^^^^^^^^^^^^^^^^^^^^^^

Stableflow enables testing of Systems of Interest through
model transformations that augment the original system
design.


Deterministic Execution
"""""""""""""""""""""""

The KPN computational model provides deterministic execution,
allowing transformed system models to:

* Record inputs and outputs of specific nodes
* Replay previously recorded data
* Verify system behavior across runs


Model Transformations for Testing
""""""""""""""""""""""""""""""""

Testing capabilities are implemented by transforming the
original system model to include additional nodes:

* **Recording Nodes**:

  * Inserted between existing nodes
  * Capture messages passing through edges
  * Store data for later replay/verification

* **Replay Nodes**:

  * Replace original data sources
  * Replay recorded data deterministically
  * Enable reproducible testing

* **Verification Nodes**:

  * Monitor specific edges or nodes
  * Compare actual vs expected behavior
  * Report test results

* **Mock Nodes**:

  * Replace complex subsystems
  * Provide controlled test conditions
  * Simulate error conditions


State Inspection
""""""""""""""""

System state inspection is achieved through:

* Adding monitor nodes to edges of interest
* Transforming nodes to expose internal state
* Collecting data from monitoring nodes


Variant Testing
"""""""""""""""

Testing across variants is supported by:

* Automated transformation of base system model
* Generation of variant-specific test configurations
* Common monitoring/verification infrastructure


8.3 Test Infrastructure
^^^^^^^^^^^^^^^^^^^^^^


Platform Test Infrastructure
""""""""""""""""""""""""""""

* Python unittest framework
* CI/CD pipeline integration
* Platform benchmark suite
* Regression test suite


SOI Test Support
""""""""""""""""

* Test data recording/replay
* Simulation environment
* Mock node implementations
* Performance measurement tools













Architecture details
--------------------

System Lifecycle
^^^^^^^^^^^^^^^^

Systems progress through the following stages::


    ┌──────────────────────┐
    │                      │
    │      Configure       │
    │   (load settings)    │
    │                      │
    └───────────┬──────────┘
                │
                │ start (first part)
                │
                ▼
    ┌──────────────────────┐
    │                      │
    │        Reset         │
    │ (allocate resources) │
    │                      │
    └───────────┬──────────┘
                │
                │ start (second part)
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


Node Implementation
^^^^^^^^^^^^^^^^^^^

Nodes can be implemented using two approaches:

1. **Functional Interface**:

   * Pure functions for lifecycle stages
   * Simple to understand and port
   * Explicit state management

.. code-block:: python

    def reset(runtime, cfg, inputs, state, outputs):
        """
        Initialize or reinitialize the node
        
        """
        return iter_signal

    def step(inputs, state, outputs):
        """
        Perform one computational step
        
        """
        return iter_signal

    def finalize(runtime, cfg, inputs, state, outputs):
        """
        Clean up resources
        
        """
        return iter_signal

2. **Coroutine Interface**:

   * Uses generator functions
   * Simpler state management
   * More natural control flow

.. code-block:: python

    def coro(runtime, cfg, inputs, state, outputs):
        """
        Main node logic as a coroutine
        
        """
        while True:
            inputs = yield (outputs, iter_signal)


Configuration
-------------

Systems are configured using structured data that specifies:

* Process and node definitions
* Edge connections
* Data types
* Runtime options

Example configuration:

.. code-block:: python

    cfg = {
        'system': {
            'id_system': 'example_system'
        },
        'host': {
            'localhost': {
                'hostname': '127.0.0.1',
            }
        },
        'process': {
            'process_main': {'host': 'localhost'}
        },
        'node': {
            'node_a': {
                'process': 'process_main',
                'state_type': 'python_dict',
                'functionality': {
                    'py_dill': {
                        'step': dill.dumps(step)
                    }
                }
            }
        },
        'edge': [{
            'owner': 'node_a',
            'data': 'python_dict',
            'src': 'node_a.outputs.output',
            'dst': 'node_b.inputs.input'
        }]
    }

Command Line Interface
----------------------

Stableflow provides a CLI for system control:

.. code-block:: shell

    # Start the system
    stableflow system start --cfg-path /path/to/config

    # Control execution
    stableflow system pause
    stableflow system step
    stableflow system stop



𝑥

# XACT design description document

| System of interest | XACT |
| :---- | :---- |
| Document name | XACT design description document |
| Document identifier | xd0006\_xact\_design\_description\_document |
| Revision indicator | 0 |
| Document status | Draft \- Incomplete |
| Date created | 20190729 |
| Date last modified | 20200508 |
| Security marking | N/A |
| Contract \# | N/A |
| Prepared for | TBD  |
| Prepared by | TBD |
| Distribution statement | Approved for public release; distribution is unlimited |

(This page intentionally blank)

# 0 \- Table of contents {#0---table-of-contents}

[**0 \- Table of contents**](#0---table-of-contents)	**[3](#0---table-of-contents)**

[**1 \- Scope**](#1---scope)	**[4](#1---scope)**

[1.1 \- Identification](#1.1---identification)	[4](#1.1---identification)

[1.2 \- System overview](#1.2---system-overview)	[4](#1.2---system-overview)

[1.2.1 \- Purpose of system](#1.2.1---purpose-of-system)	[4](#1.2.1---purpose-of-system)

[1.2.2 \- General nature of system](#1.2.2---general-nature-of-system)	[4](#1.2.2---general-nature-of-system)

[1.2.3 \- History of system development](#1.2.3---history-of-system-development)	[5](#1.2.3---history-of-system-development)

[1.2.4 \- Operation](#1.2.4---operation)	[5](#1.2.4---operation)

[1.2.5 \- Maintenance](#1.2.5---maintenance)	[6](#1.2.5---maintenance)

[1.2.6 \- Sponsor](#1.2.6---sponsor)	[6](#1.2.6---sponsor)

[1.2.7 \- Developer](#1.2.7---developer)	[6](#1.2.7---developer)

[1.2.8 \- Acquirer](#1.2.8---acquirer)	[6](#1.2.8---acquirer)

[1.2.9 \- End user](#1.2.9---end-user)	[6](#1.2.9---end-user)

[1.2.8 \- Support](#1.2.8---support)	[6](#1.2.8---support)

[1.2.9 \- Other relevant documents.](#1.2.9---other-relevant-documents.)	[6](#1.2.9---other-relevant-documents.)

[1.3 \- Document overview](#1.3---document-overview)	[6](#1.3---document-overview)

[**2 \- Referenced documents**](#2---referenced-documents)	**[7](#2---referenced-documents)**

[2.1 \- Engineering design documents](#2.1---engineering-design-documents)	[7](#2.1---engineering-design-documents)

[2.2 \- Academic references](#2.2---academic-references)	[7](#2.2---academic-references)

[2.3 \- Relevant technical standards and processes](#2.3---relevant-technical-standards-and-processes)	[7](#2.3---relevant-technical-standards-and-processes)

[**3 \- System wide design decisions**](#3---system-wide-design-decisions)	**[8](#3---system-wide-design-decisions)**

[3.1 \- Inputs](#heading=h.fq8cqjd4kpvj)	[8](#heading=h.fq8cqjd4kpvj)

[3.1.1 \- Structure of the configuration data](#3.21---structure-of-the-configuration-data)	[8](#3.21---structure-of-the-configuration-data)

[3.1.2 \- Representation of the configuration data on disk](#3.2.2---representation-of-the-configuration-data-on-disk)	[8](#3.2.2---representation-of-the-configuration-data-on-disk)

[3.1.3 \- Python modules.](#3.2.3---python-modules.)	[9](#3.2.3---python-modules.)

[3.1.4 \- Unix philosophy command line applications.](#3.2.4---unix-philosophy-command-line-applications.)	[9](#3.2.4---unix-philosophy-command-line-applications.)

[3.1.5 \- Shared libraries.](#3.2.5---shared-libraries.)	[9](#3.2.5---shared-libraries.)

[3.1.6 \- Command line interface](#3.2.6---command-line-interface)	[9](#3.2.6---command-line-interface)

[3.1.7 \- Graphical user interface](#3.2.7---graphical-user-interface)	[9](#3.2.7---graphical-user-interface)

[3.2 \- Outputs](#3.3---outputs)	[9](#3.3---outputs)

[3.3 \- Files and file formats](#3.4---files-and-file-formats)	[9](#3.4---files-and-file-formats)

[3.4 \- Response times](#3.5---response-times)	[9](#3.5---response-times)

[3.5 \- Safety requirements](#3.6---safety-requirements)	[9](#3.6---safety-requirements)

[3.6 \- Security requirements](#3.7---security-requirements)	[9](#3.7---security-requirements)

[3.7 \- Privacy requirements](#3.8---privacy-requirements)	[10](#3.8---privacy-requirements)

[3.8 \- Approach to provide flexibility](#3.9---approach-to-provide-flexibility)	[10](#3.9---approach-to-provide-flexibility)

[3.9 \- Approach to provide availability](#3.10---approach-to-provide-availability)	[10](#3.10---approach-to-provide-availability)

[3.10 \- Approach to provide maintainability](#3.11---approach-to-provide-maintainability)	[10](#3.11---approach-to-provide-maintainability)

[3.11 \- Design conventions needed to understand the design.](#3.12---design-conventions-needed-to-understand-the-design.)	[10](#3.12---design-conventions-needed-to-understand-the-design.)

[**4 \- System architectural design**](#4---system-architectural-design)	**[11](#4---system-architectural-design)**

[4.1 \- System components](#4.1---system-components)	[11](#4.1---system-components)

[4.1.1 \- System components identification and diagrams.](#4.1.1---system-components-identification-and-diagrams.)	[11](#4.1.1---system-components-identification-and-diagrams.)

[4.1.2 \- Command line interface](#4.1.2---command-line-interface)	[12](#4.1.2---command-line-interface)

[4.1.3 \- System controller](#4.1.3---system-controller)	[12](#4.1.3---system-controller)

[4.1.4 \- Process host controller](#4.1.4---process-host-controller)	[12](#4.1.4---process-host-controller)

[4.1.5 \- Process controller](#4.1.5---process-controller)	[12](#4.1.5---process-controller)

[4.1.6 \- Node controller](#4.1.6---node-controller)	[12](#4.1.6---node-controller)

[4.1.7 \- Configuration logic](#4.1.7---configuration-logic)	[12](#4.1.7---configuration-logic)

[4.1.8 \- Interface logic generation](#4.1.8---interface-logic-generation)	[12](#4.1.8---interface-logic-generation)

[4.1.9 \- Queue handling](#4.1.9---queue-handling)	[12](#4.1.9---queue-handling)

[4.2 \- Concept of execution](#4.2---concept-of-execution)	[12](#4.2---concept-of-execution)

[4.3 \- Interface design](#4.3---interface-design)	[13](#4.3---interface-design)

[4.3.1 \- Interface identification and diagrams](#4.3.1---interface-identification-and-diagrams)	[13](#4.3.1---interface-identification-and-diagrams)

[4.3.2 \- Configuration Interface](#4.3.2---configuration-interface)	[13](#4.3.2---configuration-interface)

[4.3.3 \- Command line interface](#4.3.3---command-line-interface)	[13](#4.3.3---command-line-interface)

[4.3.4 \- Runtime interface to launch remote processes.](#4.3.4---runtime-interface-to-launch-remote-processes.)	[13](#4.3.4---runtime-interface-to-launch-remote-processes.)

[**5 \- Requirements traceability**](#5---requirements-traceability)	**[13](#5---requirements-traceability)**

[**6 \- Notes**](#6---notes)	**[13](#6---notes)**

[6.1 \- Background information](#6.1---background-information)	[13](#6.1---background-information)

[6.2 \- Rationale](#6.2---rationale)	[13](#6.2---rationale)

[6.3 \- Glossary of terms](#6.3---glossary-of-terms)	[13](#6.3---glossary-of-terms)

[**Appendix A \- TBD**](#appendix-a---tbd)	**[13](#appendix-a---tbd)**




# 1 \- Scope {#1---scope}

## 1.1 \- Identification {#1.1---identification}

This document describes the design of the xact systems engineering framework. At the time of writing, xact is at a relatively early stage of development, so many of the features described are only partially implemented. This document is more correctly thought of as a description of design intent than as documentation of the as-implemented design, although some effort has been made to distinguish between the two in the body of the text. It is intended that this document be continually updated as the xact framework is developed. The design documents for the xact framework are currently hosted on github at the following URL: [https://github.com/xplain-systems/xact/](https://github.com/xplain-systems/xact/)

## 1.2 \- System overview {#1.2---system-overview}

### 1.2.1 \- Purpose of system {#1.2.1---purpose-of-system}

The xact framework is intended to support the development of software intensive systems using model based systems engineering techniques. It is oriented toward distributed, dataflow-oriented, compute-bound soft-real-time systems.

At early stages of development, it is intended to enable technology demonstrators to be assembled rapidly from prototype components and environment simulations and then to support the independent development of each component towards design maturity. In this way, the xact framework is intended to enable engineering organizations to narrow the structural and technical gaps that so often exist between research and product development teams.

The xact systems engineering framework is also intended to support automation of various aspects of the engineering process, supporting techniques such as design optimization or determining the acceptability of arguments for the safety, security or privacy case.

The ultimate vision is for xact to provide a foundation for the development of explainable systems, able to make arguments about the safety of their own actions, and the safety of their design, given the environment in which they find themselves operating.

### 1.2.2 \- General nature of system {#1.2.2---general-nature-of-system}

Functionally, the xact framework is an implementation of a Kahn process network. A Kahn process network consists of a number of ‘processes’ connected by ‘channels’ along which 'tokens’ may be passed. If the ‘processes’ and the ‘channels’ both obey certain restrictions, then guarantees of monotonicity and determinism may be obtained. To prevent confusion with the similar but distinct notion of operating system processes, this xact system refers to a Kahn 'process’ as a ‘node’.

Xact allows one or more nodes in the Kahn process network graph to be mapped to each of the available operating system processes (or an equivalent), across one or more process hosts. Each process host normally corresponds to a distinct server or embedded computer, although it is intended that a large system-on-chip may contain multiple process hosts, one for each microprocessor in the SOC. In this way, xact supports both multiprocessing and distributed computing.

Conceptually, each node in the Kahn process network graph corresponds either to the implementation of a computational component in the system itself, or to a simulation of some other thing inside or outside the system boundary; perhaps a sensor or part of the physical environment within which the system operates. It is in this way that xact is intended to support model based systems engineering techniques.

The xact framework is intended to support nodes that are implemented in a number of different languages, although at the time of writing only Python is supported with C being the next language planned. It is intended that eventually it should be possible to deploy collections of compute nodes to FPGAs or ASICs as well as more conventional compute hardware.

For the guarantees of monotonicity and determinism to be upheld, each node must meet certain restrictions, although in certain cases (such as at the edge of the process network graph) those restrictions may be lifted to permit interfacing with external systems.

Similarly, the xact framework is intended to support a range of different implementations for the channels that connect the nodes in the Kahn process network graph. At the time of writing, nodes communicating within a single process use synchronized access to shared memory areas, nodes communicating across process boundaries on the same process host use a shared memory interprocess queue implementation, and nodes communicating between process hosts use zeromq sockets. It is intended that future development work enable the support of other transports such as SPI, DDS, ROS or Kafka.

The topology of the Kahn process network graph is treated as configuration data, and is provided as a data structure that is read from a set of configuration files. It is intended that this data structure could be generated automatically, either by a design optimization algorithm, or by an IDE to permit graphical drag-and-drop style rapid prototyping.

At its most basic functional level,, the xact system can be seen as a configuration tool for message based middleware.

### 1.2.3 \- History of system development {#1.2.3---history-of-system-development}

The xact systems engineering framework is a relatively straightforward implementation of ideas which emerged starting in the early 1960s with Bell Labs’ BLODI (Block diagram compiler), and expanded upon in the mid 1970s with Gilles Kahn and David Macqueen’s work on Kahn process networks, Jack Dennis’ work on Data Flow networks, and Tony Hoare’s work on Communicating sequential processes.

These ideas have been enormously influential over the last 60 years or so, and today it is commonplace to come across systems and software based on concepts that trace their intellectual foundations back to this time. Unix pipes, coroutines, message based middleware and actor models all share this academic heritage.

Macqueen and Kahn’s work stands out, not only because of the denotational semantics that Kahn developed, but also because of the monotonicity and determinism guarantees provided by his formalism; guarantees which are clearly of critical importance to any model based engineering methodology.

There are a very large number of commercial systems that are conceptually similar to xact \- Simulink, LabView and LUSTRE are perhaps the most well-known of these. The open source ROS framework and the automotive AUTOSAR standard both have message passing models as a subset of their functionality. The number of message passing systems in the enterprise software space are too numerous to enumerate fully, as are those which are specialized for data science or for machine learning.

The intent of xact is not to compete with or replace these frameworks, but rather to provide a uniform interface for the automatic configuration and deployment of such systems, enabling a higher level of automation than is currently practicable. To this end, the structure of the process network graph in xact is not defined programmatically, but rather is specified as a data structure which can either be read from configuration or generated dynamically.

Development started in late 2016 with a simple sequential model. After a hiatus, development picked up again in the summer of 2019, adding more capable data definitions, multiprocessing and then distributed computing capability.

### 1.2.4 \- Operation {#1.2.4---operation}

At present, the end user is required to write a set of configuration files that describe both the topology of the compute graph as well as how the nodes are to be distributed across available computing resources. The logic that is instantiated by each node is also specified in configuration. Where new logic is required, this can be done by creating a python module that conforms to a specific interface; providing a ‘step’ function and an (optional) reset function.

Once the configuration files have been defined and the implementation for all nodes is available, the xact system can be launched from the command line. 

When the xact system is launched, it first reads in the specified configuration files, assembling the configuration data structure and enriching it with information that is represented only implicitly in the on-disk configuration.

If some nodes are to be run on remote process hosts, then xact uses ssh to launch processes on those computers. With xact processes running on all process hosts, a brief synchronization routine is run to ensure that all remote queues are ready and connected.

At this point, the reset() function is called on all nodes, and then normal operation commences.

Data flows between nodes, and for each node, when all inputs have data items and are ready to be read, the step() function for that node is called.

In future, it is intended that it should be possible to edit the configuration files via a graphical editor, and that the network should be able to change dynamically, without the system halting. 

It is also intended to support recording and replay of data passing through nodes, enabling a step-forwards and step-backwards functionality when running as a simulation.

### 1.2.5 \- Maintenance {#1.2.5---maintenance}

When xact changes, how will those changes be communicated to the end user?

I.e. when features are obsoleted and removed, how do we coordinate with the customers who are using those features? Do we mark APIs as obsoleted and then removed? Or do we encourage customer projects to fix versions?

How will the framework be versioned? What will the release cycle look like? How will that integrate with how our customers get support?

How do we document what features we have implemented?

When we introduce new features, how do we coordinate with training and documentation?

### 1.2.6 \- Sponsor {#1.2.6---sponsor}

N/A

### 1.2.7 \- Developer {#1.2.7---developer}

Initial development was undertaken by Mr. W. Payne (2016-2019). The intent is to contract Mr A Kumar to implement specific features.

### 1.2.8 \- Acquirer {#1.2.8---acquirer}

N/A

### 1.2.9 \- End user {#1.2.9---end-user}

This software is targeted at systems engineers and software engineers who want to be able to quickly produce prototypes, and then smoothly and easily take those prototypes into production.

The vision is to enable rapid prototyping of systems with ML algorithm components in Python, then easily transforming the system piece-by-piece into C and deploy onto embedded hardware (or into VHDL and deploy on an FPGA).

### 1.2.8 \- Support {#1.2.8---support}

TBD. Strategic decision required. See also maintenance. 

### 1.2.9 \- Other relevant documents. {#1.2.9---other-relevant-documents.}

* xd0007\_xact\_requirements\_specificatio \- XACT Requirements Specification.  
* xd0008\_xact\_user\_manual \- XACT User Manual.  
* DI-IPSC-81432A \- Data Item Description for System / Subsystem Design Description documents.  
* SMC-S-012 \- Air Force Space Command \- Space and Missile Systems Center Standard \- Software Development

## 1.3 \- Document overview {#1.3---document-overview}

This is a working document and is expected to develop and mature along with the system itself.

# 2 \- Referenced documents {#2---referenced-documents}

## 2.1 \- Engineering design documents {#2.1---engineering-design-documents}

* xd0007\_xact\_requirements\_specificatio \- XACT Requirements Specification.  
* xd0008\_xact\_user\_manual \- XACT User Manual.

## 2.2 \- Academic references {#2.2---academic-references}

* 1974 \- “The Semantics of a Simple Language for Parallel Programming” \- Gilles Kahn  
* 1976 \-“Communicating Sequential Processes” \- Tony Hoare  
* CyberPhysical systems book.

## 2.3 \- Relevant technical standards and processes {#2.3---relevant-technical-standards-and-processes}

* DI-IPSC-81432A \- Data Item Description for System / Subsystem Design Description documents.  
* SMC-S-012 \- Air Force Space Command \- Space and Missile Systems Center Standard \- Software Development  
* INCOSE Systems engineering handbook, 2nd edition..

# 

# 3 \- System wide design decisions {#3---system-wide-design-decisions}

This section shall be divided into paragraphs as needed to present system wide design decisions, that is, decisions about the systems behavioral design (from the users point of view) in meeting its requirements, and other decisions affecting the selection and design of system components.

Or simply refer to the requirements document.

## 3.1 \- Computational model

## 3.2 \- Inputs

### 3.21 \- Structure of the configuration data {#3.21---structure-of-the-configuration-data}

xact systems can be configured either by authoring configuration files or by generating and/or modifying configuration data programmatically. In both cases the structure of the configuration data is the same.

When being handled by a Python program, the xact configuration data is a hierarchical dict that specifies the structure of the system to be run. It is divided into six sections, each corresponding to a major architectural division of the xact framework:

**`‘system’`**`:         <SYSTEM-CONFIGURATION>`  
**`‘host’`**`:`  
    `<HOST-ID>:    <PROCESS-HOST-CONFIGURATION>`  
**`‘process’`**`:`  
    `<PROCESS-ID>: <PROCESS-CONFIGURATION>`  
**`‘node’`**`:`  
    `<NODE-ID>:    <NODE-CONFIGURATION>`  
**`‘edge’`**`:`  
    `- <EDGE-CONFIGURATION>`  
**`‘data’`**`:`  
    `<TYPE-ID>:    <TYPE-SPEC>`

The **`‘system’`**, **`‘host’`**, **`‘process’`** and **`‘node’`** sections each correspond to a level in the physical decomposition hierarchy of an xact system.

The **`‘system’`** section contains configuration structure which applies to the system as a whole. 

The **`‘host’`**, **`‘process’`** and **`‘node’`** sections each contain a dict which maps from the component identifier to the configuration structure for that component. Thus **`cfg[‘host’]`** is a dict that maps from host id strings to host configuration, **`cfg[‘process’]`** is a dict that maps from process id strings to process configuration, and **`cfg[‘node’]`** is a dict that maps from node id strings to node configuration.

The **`’edge’`** section is a little different, as edges in an xact system are anonymous. This means that Instead of mapping from an identifier to configuration data, we instead have a list (or set) of edge configuration structures.

The **`‘data’`** section is laid out in a similar manner to the host, process and node sections, as a dict that maps from a type id string to the configuration structure that defines the properties of the data type.

A key driving requirement for this approach is to minimize the risk of merge conflicts between different versions of the configuration files. This is achieved by structuring the configuration such that most changes are both minimal and compact.

It is for this reason that the containment structure of the system (which nodes are contained within which processes, and which processes are contained within which process-hosts) is specified within the configuration of the subordinate component. For example, the configuration for each process records the host within which it resides, and changing to a new host will involve a change only to the relevant process configuration and nowhere else.

Similarly, a change to the connectivity structure of the system (the Kahn process network graph) requires a change only to the relevant edge configuration and nowhere else.

The intent of these design decisions is to produce minimal, readable diffs, and a minimum of merge conflicts in a branch-and-merge engineering process.

### 3.2.2 \- Representation of the configuration data on disk {#3.2.2---representation-of-the-configuration-data-on-disk}

To start an xact system from the command line, call **`xact-cli -p <PATH>`**. 

The path parameter specifies the location where the configuration of the system to be run may be found. It can either be a file path giving the location of a single configuration file, or a directory path, giving the location of a collection of configuration files held together in a single directory.

When read (and combined together, in the case of a directory path being given), the resulting configuration is expected to have the structure described in the previous section.

Xact can read configuration files formatted as YAML, JSON or XML. If YAML format is used, the filename should take the form `<NAME>.cfg.yaml`. Similarly, if JSON or XML is used, the filename should take the form `<NAME>.cfg.json` or `<NAME>.cfg.xml` respectively.

If the path parameter is given as a directory path, then the leading part of the filename (the part preceding the `.cfg.*` suffix) is used to determine where in the configuration structure the file content should be placed, with any dots in the filename being used as a path delimiter This means that the content of file `host.cfg.yaml` will be placed in `cfg[‘host’]`, and the content of file `host.my_host_id.cfg.yaml` goes to `cfg[‘host’][‘my_host_id’]`. 

Configuration files are read in order of filename length, shortest to longest, so a file targeting a specific subset of the configuration structure is not wiped out by one targeting a broader superset of the structure.

If a file named `root.cfg.*` is present in the directory, it is treated as a special case, and is always read first, it’s content placed in the root of the configuration structure.

Another special case concerns XML files. If t

### 3.2.3 \- Python modules. {#3.2.3---python-modules.}

TBD \- Refer to some sort of interface definition (TBD) in source document repository.  
Requirement is for a mandatory step() function and an optional reset() function.

### 3.2.4 \- Unix philosophy command line applications. {#3.2.4---unix-philosophy-command-line-applications.}

Describe planned wrapper for UNIX pipes

### 3.2.5 \- Shared libraries. {#3.2.5---shared-libraries.}

TBD \- Define an interface for .so files.

### 3.2.6 \- Command line interface {#3.2.6---command-line-interface}

TBD

### 3.2.7 \- Graphical user interface {#3.2.7---graphical-user-interface}

TBD

## 3.3 \- Outputs {#3.3---outputs}

TBD

## 3.4 \- Files and file formats {#3.4---files-and-file-formats}

TBD

## 3.5 \- Response times {#3.5---response-times}

TBD

## 3.6 \- Safety requirements {#3.6---safety-requirements}

TBD

## 3.7 \- Security requirements {#3.7---security-requirements}

TBD

## 3.8 \- Privacy requirements {#3.8---privacy-requirements}

TBD

## 3.9 \- Approach to provide flexibility {#3.9---approach-to-provide-flexibility}

TBD

## 3.10 \- Approach to provide availability {#3.10---approach-to-provide-availability}

TBD

## 3.11 \- Approach to provide maintainability {#3.11---approach-to-provide-maintainability}

TBD

## 3.12 \- Design conventions needed to understand the design. {#3.12---design-conventions-needed-to-understand-the-design.}

TBD

# 

# 4 \- System architectural design {#4---system-architectural-design}

An xact system is composed of one or more process hosts, each of which is composed of one or more processes, each of which is in turn composed of one or more nodes in the compute graph. In this way each process (normally implemented as a linux process) may contain several nodes which operate synchronously, but we can also distribute the computational load across multiple processes and even multiple computers if required. Each node in the xact graph corresponds to the concept of a ‘process’ in a Kahn process network.

This hierarchy is intended to map loosely onto the systems engineering hierarchy defined in version 2 of the INCOSE systems engineering handbook, although the exact system breakdown structure and the exact mapping used will of course vary from problem to problem.

Each xact graph node can be thought of as a software component, and a system implemented using xact as a component-oriented architecture. During development, xact nodes can also be used to implement simulations of sensors, actuators, or other extra-

Because xact nodes can be used for either 

 it should be possible to map the xact process and process host concepts onto whatever hardware components they reside within.   
The xact system can be used to model or implement anything from an entire cyber-physical system, down to the control system for an individual subassembly.  
This computational model suits certain types of cyber-physical systems, namely those compute-bound soft-real time systems that map naturally onto a ‘processing pipeline’ consisting of a small number of long-lived processes.

### 4.1 \- System components {#4.1---system-components}

### 4.1.1 \- System components identification and diagrams. {#4.1.1---system-components-identification-and-diagrams.}

The product breakdown structure for xact decomposes the framework into 8 top level system components.

These 8 components work together to read in configuration data and to distribute computational work across hardware resources accordingly, managing communications between hardware resources as configured and as required, and enabling the system to be controlled by the user.

1. The **cli** component provides elementary command line control over xact systems, enabling the system to be started, stopped and paused from the command line.  
2. The **sys** component is responsible for executing commands on the level of the entire xact system, deploying logic to remote hosts; configuring and connecting inter host channels, as well starting, stopping and pausing the process hosts.  
3. The **host** component is responsible for executing commands on the level of process hosts, configuring and connecting inter process communications channels as well as starting and stopping the processes at the next level down.  
4. The **proc** component is responsible for executing commands on the level of individual operating system processes. This component contains the ‘main loop’ for independently running processes, or the callback for those processes that are running under the control of an integrated application. The proc component is responsible for scheduling and stepping individual graph nodes, handling interrupts and restarting when recoverable errors occur.  
5. The **node** component provides a thin wrapper around the logic that is configured for each node. It handles reading and writing to the queue interface, stores data between calls to step(), and provides functionality for recording and replaying channel data.  
6. The **cfg** component provides functions for reading, writing, serializing, deserializing, and ‘enriching’ configuration data.  
7. The **gen** component responsible for generating logic for the serialization, deserialization and validation of data items based on specifications from the configuration data.  
8. The **queue** component provides adapter classes for different queue implementations, ensuring that each node is able to use a common interface to send and receive data irrespective of the underlying implementation.

### 4.1.2 \- Command line interface {#4.1.2---command-line-interface}

The xact command line interface component is stored in an executable python script named ‘xact’. The click (command line interface construction kit) library is used for command line parsing, via a thin wrapper with minor customization in ‘cli.py’. The command line interface reads configuration data with the ‘config’ package, and either invokes xact at a system level with the system.py module, or invokes xact at a host level with the host.py module.

### 4.1.3 \- System controller {#4.1.3---system-controller}

If configuration data has been generated programmatically, the xact system is started by calling **`xact.sys.start(cfg)`**. 

### 4.1.4 \- Process host controller {#4.1.4---process-host-controller}

TBD

### 4.1.5 \- Process controller {#4.1.5---process-controller}

TBD

### 4.1.6 \- Node controller {#4.1.6---node-controller}

TBD

### 4.1.7 \- Configuration logic {#4.1.7---configuration-logic}

TBD

### 4.1.8 \- Interface logic generation {#4.1.8---interface-logic-generation}

TBD

### 4.1.9 \- Queue handling {#4.1.9---queue-handling}

TBD

## 4.2 \- Concept of execution {#4.2---concept-of-execution}

This paragraph shall describe the concept of execution among the system components. It shall include diagrams and descriptions showing the dynamic relationship of the components. That is, how they will interact during system assembly, storage, deployment and operation, including, as applicable, flow of execution control, data flow, dynamically controlled sequencing, state transition diagrams, priorities among components, handling of interrupts, timing/sequencing relationships, exception handling, concurrent execution, dynamic allocation/deallocation, dynamic creation/deletion of objects, processes, tasks, assembly, storage, deployment and other aspects of dynamic behavior.

## 4.3 \- Interface design {#4.3---interface-design}

This section describes both interfaces among the components of the system and their interfaces with external entities such as other systems, configuration items and users, referencing interface design description documents as needed.  
TBD

### 4.3.1 \- Interface identification and diagrams {#4.3.1---interface-identification-and-diagrams}

This section describes the project-unique identifier assigned to each interface and identifies the interfacing entities by name, number, version and documentation references as applicable. The identification shall state which entities have fixed interface characteristics and which are being developed or modified. One or more interface diagrams shall be provided.

### 4.3.2 \- Configuration Interface  {#4.3.2---configuration-interface}

Configuration file format and configuration structure

### 4.3.3 \- Command line interface {#4.3.3---command-line-interface}

CLI overview

### 4.3.4 \- Runtime interface to launch remote processes. {#4.3.4---runtime-interface-to-launch-remote-processes.}

CLI overview

# 5 \- Requirements traceability {#5---requirements-traceability}

Traceability from each component to requirements allocated to it.

# 6 \- Notes {#6---notes}

## 6.1 \- Background information {#6.1---background-information}

## 6.2 \- Rationale {#6.2---rationale}

## 6.3 \- Glossary of terms {#6.3---glossary-of-terms}

# Appendix A \- TBD {#appendix-a---tbd}

