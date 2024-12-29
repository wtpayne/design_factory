







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
