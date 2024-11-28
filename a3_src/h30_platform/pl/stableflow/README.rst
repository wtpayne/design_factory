Stableflow Architectural Overview
=================================

Stableflow is a framework designed for engineering 
distributed data-flow oriented systems.

It is intended to enable and encourage:
- **Model driven engineering.**
- **Product line engineering.**
- **Engineering workflow automation.**

To achieve this, it is designed to support:
- Deterministic simulation and re-simulation.
- Automatic transformation of system architecture specifications.
- Automatic optimisation of system design parameters.

Stableflow is also intended to integrate well into
the modern ecosystem of ML/AI tools, allowing for
e.g. the integration of LLMs into various engineering
workflows.

Core Concepts
-------------

Stableflow's architecture is built around several 
core concepts:

- **System**:  The highest level entity representing the system of interest as a whole.
- **Host**:    A physical or virtual processor, capable of hosting one or more contexts of execution. This normally corresponds to a single machine or device.
- **Process**: A single context of execution, capable of executing one or more nodes sequentially. This normally corresponds to a single thread or operating system process.
- **Node**:    The fundamental computation unit that performs a specific task.

These components interact to form a distributed 
system capable of instantiating and running complex
workflows across a distributed collection of devices.

Components and Their Interactions
---------------------------------

### System

The **System** orchestrates the entire Stableflow SOI 
(System Of Interest). It manages the lifecycle of hosts 
and processes, ensuring that all components work together
cohesively. The system is responsible for starting, 
stopping, pausing, and stepping through the execution
of the SOI, both in simulation and also in live operation.

Key functions:

- **Start**: Initiates the system, starting all hosts and processes.
- **Stop**: Stops the system gracefully.
- **Pause/Step**: Allows for controlled execution by pausing and stepping through the processes.

### Host

A **Host** represents a physical or virtual processor, 
capable of hosting one or more contexts of execution.
Each host normally corresponds a single machine or device
that participates in the system of interest. Each host is
responsible for managing the resources needed by the
processes they run.

Host responsibilities:

- Starting and stopping local processes.
- Managing inter-process communication for processes on the same host.
- Handling control signals from the system (e.g., pause, resume).

### Process

A **Process** is a single context of execution, capable of
sequentially executing the logic controlled by each of the
nodes that it contains. Each process corresponds conceptually
with either a single operating system process or thread. (At
the time of writing, OS processes are used exclusively).
Each process executes the nodes that it contains in a 
specified order and manages inter-node communication within
the same process.

Process functions:

- **Configuration**: Processes are configured based on the system's configuration, determining which nodes they contain and how they interact.
- **Execution**: Managing the execution loop that steps through nodes.
- **Signal Handling**: Processes handle control signals to manage execution flow (e.g., pause, reset).

### Node

A **Node** is the basic unit of functionality in Stableflow.
Each node meets a specific functional specification and can
be composed either manually or automatically with other
nodes to implement more complex compound functions.

Node characteristics:

- **Functionality**: Defined by a reset function and a step function, or as a coroutine. Nodes encapsulate the design implementation needed to perform their function.
- **State**: Nodes maintain state across executions, which can be reset as needed.
- **Inputs and Outputs**: Nodes receive inputs and produce outputs, enabling data flow between nodes.

#### Node Lifecycle

1. **Initialization**: Configure the node with necessary parameters and initialize state.
2. **Reset**: Prepare the node for execution, resetting state if necessary.
3. **Step**: Execute the node's main functionality, processing inputs and producing outputs.
4. **Finalize**: Clean up resources when the node is no longer needed.

Data Flow and Communication
---------------------------

Stableflow uses a message-passing mechanism for communication
between nodes, processes, and hosts.

### Edges

- **Edges** represent the connections between nodes, defining the data flow.
- Edges can be:

  - **Intra-Process**: Communication between nodes within the same process.
  - **Inter-Process**: Communication between nodes in different processes on the same host.
  - **Inter-Host**: Communication between nodes on different hosts.

### Queues

- **Queues** are used for inter-node communication, handling message passing along edges.
- Depending on the edge type, different queue implementations are used (e.g., in-memory queues for intra-process communication, network-based queues for inter-host communication).

Control Signals
---------------

Stableflow provides a set of control signals for managing 
execution flow and coordinating between components.

### Signal Types

- **Continue**: Indicates that execution should proceed normally.
- **Exit**:     Signals that a process or node should shut down.

  - **Immediate Exit**:  For non-recoverable errors requiring immediate termination.
  - **Controlled Exit**: For graceful shutdowns.

- **Reset**:      Instructs nodes or processes to reset their state.
- **Pause/Step**: Used to pause execution or step through execution one node at a time.

### Signal Handling

- Processes and nodes can emit and handle signals to control the flow of execution.
- The system and hosts listen for signals to manage the overall execution state.

Execution Flow
--------------

1. **System Start**: The system initializes hosts and processes based on the configuration.
2. **Process Initialization**: Each process sets up its nodes and communication channels.
3. **Node Execution**: Nodes execute their reset functions, then enter their execution loop.
4. **Data Processing**: Nodes process incoming data, produce outputs, and pass data to connected nodes via edges.
5. **Control Signals**: Signals can alter the execution flow, triggering pauses, resets, or shutdowns.
6. **System Shutdown**: The system coordinates a graceful shutdown of all components when execution is complete or upon receiving an exit signal.

Configuration
-------------

Stableflow applications are configured using structured data (e.g., dictionaries). Configuration specifies:

- **Processes and Nodes**: Definitions of processes and the nodes they contain.
- **Edges**: Connections between nodes, including the type of communication channel.
- **Data Types**: Definitions of data structures passed between nodes.
- **Runtime Options**: Settings for execution behavior (e.g., local vs. distributed execution).

Example (incomplete) configuration snippet:

.. code-block:: python

    cfg = {
        'system': {
            'id_system': 'stableflow_system_example'
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
            },
            'node_b': {
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
        }],
        'data': {
            'python_dict': 'py_dict'
        }
    }

Example Node Implementation
---------------------------

Nodes can be implemented as step functions or coroutines.

### Step Function Node

.. code-block:: python
    import pl.stableflow.signal

    def step(inputs, state, outputs):
        if 'count' not in state:
            state['count'] = 0
        else:
            state['count'] += 1
        outputs['output']['count'] = state['count']
        if state['count'] >= 10:
            return (exit_ok_controlled,)

### Coroutine Node

.. code-block:: python

    def coro(runtime, cfg, inputs, state, outputs):
        count = -1
        signal = (None,)
        while True:
            inputs = yield (outputs, signal)
            count += 1
            outputs['output']['count'] = count
            if count >= 10:
                signal = (exit_ok_controlled,)

Command-Line Interface
----------------------

Stableflow provides a command-line interface (CLI) for interacting with the system.

### Main Commands

- **system**: Control the system as a whole.
  - **start**: Start the entire system.
  - **stop**: Stop the system.
  - **pause**: Pause the system.
  - **step**: Step through execution.
- **host**: Control individual hosts.

Example usage:

.. code-block:: shell

    stableflow system start --cfg-path /path/to/config
    stableflow system stop
    stableflow system step

Conclusion
----------

Stableflow's architecture allows developers to build 
scalable, distributed systems by composing nodes into 
processes and hosts within a system. Its structured 
approach to data flow, control signals, and execution
management simplifies the development of complex 
applications in a model driven engineering and
product line engineering context.
