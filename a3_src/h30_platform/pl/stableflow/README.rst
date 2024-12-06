==========
Stableflow
==========


Executive Summary
-----------------

Stableflow is a framework for designing and operating 
distributed systems, focusing on model-driven design and
product line engineering. It enables teams to build
families of related systems that can be automatically
transformed and optimized based on architectural models.


When to Use Stableflow
----------------------

Stableflow is ideal for:

* Building families of related distributed systems where variants need to share core architecture
* Systems requiring rigorous testing and simulation before deployment
* Projects where architectural exploration and optimization are key concerns
* Teams adopting model-driven development practices

Stableflow may not be the best choice for:

* Simple CRUD applications
* Single-purpose applications with minimal architectural complexity
* Projects requiring rapid prototyping


Key Benefits
------------

* Model-Driven Design: Express system architecture explicitly and transform it automatically
* Design Automation: Generate system variants and optimize parameters systematically
* Simulation Support: Test and validate system behavior deterministically
* Modern Integration: Works with contemporary ML/AI tools and languages


Example Use Cases
-----------------

Machine Vision System
^^^^^^^^^^^^^^^^^^^^^

Consider an autonomous vehicle company developing machine
vision systems:

* Base Architecture: Image Capture → Pre-processing → Object Detection → Scene Understanding → Control Output
* Variants:

  * Development: Using recorded data, with visualization and debugging
  * Simulation: Simulated sensors, simulated vehicle responses.
  * Hardware-in-Loop: Real sensors, simulated vehicle responses
  * Production: Optimized for specific vehicle configurations

    * High-end: Multiple high-res cameras, dedicated compute
    * Mid-range: Balanced sensor suite, shared compute
    * Economy: Essential sensors, resource-constrained

Stableflow enables:

* Single architecture supporting all development phases
* Automated generation of variant-specific implementations
* Deterministic replay of recorded data for testing
* Clear traceability from requirements to deployment
* Systematic validation across vehicle configurations


Data Processing Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^

Consider a team building a real-time data processing
pipeline:

* Base Architecture: Data Collection → Filtering → Analysis → Storage → Visualization
* Variants:

  * Development: Small datasets, debug outputs, hot reloading
  * Testing: 

    * Unit tests with mock data sources
    * Integration tests with recorded data
    * Performance tests with data generators

  * Production:

    * Local: Single machine, minimal latency
    * Distributed: Multiple machines, high throughput
    * Embedded: Resource-constrained environment

Stableflow enables:

* Same architecture across all development stages
* Deterministic testing with recorded data
* Easy switching between variants without code changes
* Performance optimization for different deployments


Core Concepts
-------------

System Overview
^^^^^^^^^^^^^^^

A Stableflow system is composed of:

* **Hosts**: Physical or virtual machines that run processes
* **Processes**: Execution contexts that contain nodes
* **Nodes**: Basic computational units that process data
* **Edges**: Connections that carry data between nodes
* **Functional Chains**: Connected groups of nodes implementing specific features

These components work together to form distributed 
systems capable of running sophisticated workflows
across multiple devices.


Computational Models
^^^^^^^^^^^^^^^^^^^^

Stableflow supports multiple computational models that 
determine how nodes communicate and process data:

#. **Kahn Process Networks (Primary Model)**

   * Nodes run when all inputs are available
   * Deterministic behavior
   * Best for simulation and testing

#. **Actor Model (Planned)**

   * Nodes run as soon as any input is ready
   * Higher runtime performance
   * Best for efficient use of computational resources

#. **Concurrent Sequential Processes (Planned?)**

   * Direct synchronization between nodes
   * Best for tightly coordinated processes


Architecture Details
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
