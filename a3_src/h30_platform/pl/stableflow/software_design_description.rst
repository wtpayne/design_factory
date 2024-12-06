======================================
Stableflow software design description
======================================

Stableflow is a tool for designing and operating 
distributed systems. 

It is intended to enable and encourage:

* Model driven design.
* Design workflow automation.
* Product line engineering.

To achieve this, it is designed to support:

* Deterministic simulation and re-simulation.
* Automatic transformation of system architecture specifications.
* Automatic optimisation of system design parameters.

It is conceptually similar to tools like Simulink, 
Labview or Ptolemy, but with a greater focus on
interoperability with today's ecosystem of ML/AI
models and tools, which is dominated by languages
like Python, R, Julia and C/C++.


----------------------------
The argument for stableflow
----------------------------

Software development is on the cusp of a transformation.
As AI reshapes how we build software, we need better ways
to express, manipulate, and reason about system architecture
at scale. Traditional approaches that focus on individual
features and products are no longer enough.

Two powerful techniques from industries like aerospace,
defense, and automotive offer a path forward:

Product line engineering transforms how we think about
product strategy - instead of building individual products,
we design entire families of related products. This enables:
* Systematic reuse across product variants
* Strategic planning of feature combinations
* Rapid response to market opportunities
* Clear mapping between market segments and technical capabilities

Model-driven development changes how we build systems by
making the architecture itself programmable. This enables:
* Automatic generation of system variants
* Rapid adaptation to different deployment scenarios
* Architecture-level transformations and optimizations
* Strong foundations for AI-assisted system design

While many developers work effectively within client-server
architectures and user-story driven development ("As a user,
I want to..."), these approaches alone don't unlock the full
potential of automated system design and strategic product
planning.

Stableflow brings these powerful techniques into the modern
software development ecosystem, combining them with the
agility and tooling that developers expect. As AI and LLMs
transform software development, having explicit, transformable
models of system architecture becomes increasingly valuable.


-------------
Core concepts
-------------

Stableflow's architecture is built around several 
foundational concepts:

* **System**: The highest level entity representing the system of interest as a whole.
* **Host**: A physical or virtual processor that can run one or more execution contexts. This typically corresponds to a single machine, device, processor core or virtual machine.
* **Process**: A single sequential execution context running on a host. This typically corresponds to a single thread or operating system process.
* **Node**: The basic building block of system behavior, recieving and sending messages. Runs within the execution context of a process.
* **Node implementation**: The software that gives a node behaviour. Must implement one of a handful of interface standards.
* **Edge**: Represents a flow of messages between nodes, usually implemented using either a queue of a piece of shared memory.
* **Functional chain**: Represents an interconnected sequence of nodes and edges that together implement a specific system function.
* **Computational model**: An abstract model of concurrent computation, specifying when and how nodes are run, and the guarantees that arise as a result.

These concepts work together to form distributed systems
capable of running sophisticated workflows across multiple 
devices.


------------------------------------
Core concepts and their interactions
------------------------------------


System
^^^^^^

The **System** orchestrates the entire Stableflow SOI 
(System Of Interest). It manages the lifecycle of hosts and
processes, ensuring that all components work together 
cohesively. The system is responsible for starting, stopping,
resetting, pausing, and stepping through the execution of 
the SOI, both in simulation (i.e. during development) and
also in live operation.

Key functions:

* **Start**: Initiates the system, starting all hosts and processes.
* **Stop**: Stops the system gracefully.
* **Reset**: Resets the system to some initial state.
* **Pause/Step**: Allows for controlled execution by pausing and single-stepping the system.


System lifecycle
^^^^^^^^^^^^^^^^

The following diagram shows the system lifecycle::

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

1. **Configure**: Configuration data is processed, processes and nodes instantiated, queues created and static schedules computed.
2. **Reset**: All nodes are reset, allocating resources as required.
3. **Run**: Nodes are stepped as per the computational model.
4. **Pause**: If the system is paused, single-stepping is handled.
5. **Stop**: If the system is stopped, nodes are finalized to clear resources.

Note that the system can be reset or stopped at any time, but
these transitions are omitted from the diagram for clarity.


Host
^^^^

A **Host** represents a physical or virtual processor, 
capable of hosting one or more contexts of execution. Each
host normally corresponds to a single machine, device (or
processor core on a SoC) that participates in the system of
interest. Each host is responsible for managing the resources
needed by the processes they run.

Host responsibilities:

* Starting and stopping local processes.
* Managing inter-process communication for processes on the same host.
* Handling control signals from the system (e.g., start, stop, pause, step).


Process
^^^^^^^

A **Process** is a single context of execution, capable of
sequentially executing the logic controlled by each of the
nodes that it contains. Each process corresponds conceptually
with either a single operating system process or thread. (At
the time of writing, OS processes are used exclusively).
Each process executes the nodes that it contains in a 
specified order and manages inter-node communication within
the same process.

Process functions:

* **Configuration**: Processes are configured based on the system's configuration, determining which nodes they contain and how they interact.
* **Execution**: Managing the execution loop that steps through nodes.
* **Signal Handling**: Processes handle control signals to manage execution flow (e.g., pause, reset).


Node
^^^^

A **Node** is the basic building block of system behaviour
in Stableflow. The system as a whole can be seen as a data
flow graph which is composed of nodes and edges, potentially
spanning across multiple hosts and processes. Each edge in
this graph represents messages being passed from node to node, 
and each node represents some computation. The design of that
computation is determined by the **implementation** that is
associated with each node.

Stableflow is intended to be used for model driven engineering,
so it is designed to make it possible to swap out different
node implementations with minimal changes to the system
configuration as a whole. The node itself ends up being a
small wrapper which simply "glues" the implementation into
the larger system.


Node Implementation:
^^^^^^^^^^^^^^^^^^^^

It is intended that node implementations can be provided by
a wide variety of different programming languages, although
currently only Python is supported.

For Python modules, Stableflow also allows a couple of
different interface conventions to be used, each offering
different advantages and disadvantages.

* **Functional** uses pure functions for node lifecycle stages.
* **Coroutine** uses a synchronous coroutine (generator function).

The functional approach is conceptually very simple, allows
logic to be translated very easily to different programming
languages, but imposes some complexity as state information
needs to be explicitly passed between consecutive model steps.

.. code-block:: python

    def reset(runtime, cfg, inputs, state, outputs):
        """
        The reset function initializes or reinitializes
        inputs, state and outputs to initial values. It is 
        always called on system start, and can be called
        again to reset the node back to a known good
        condition. The reset implementation must take care
        of disposing of any allocated resources as needed
        before (re-)allocating them.

        """
        iter_signal = ...
        return iter_signal

    def step(inputs, state, outputs):
        """
        The step function carries out a single computational
        step, reading from inputs and state, and writing to
        state and outputs.

        """
        iter_signal = ...
        return iter_signal

    def finalize(runtime, cfg, inputs, state, outputs):
        """
        The finalize function is called when the node is no
        longer needed. It can be used to clean up any resources
        allocated by the node.

        """
        iter_signal = ...
        return iter_signal

The coroutine approach is conceptually a little bit more
complex, as it requires engineers to understand how to use
synchronous coroutines (generator functions), but it has
the advantage of dramatically simplifying the logic for
handling state.

.. code-block:: python
    def coro(runtime, cfg, inputs, state, outputs):
        """
        The coro function enables us to store state as local
        variables, simplifying state management, and
        enabling conditional logic to be implemented in a
        far simpler manner than would be possible in a
        step function.

        """
        while True:
            iter_signal = ...
            inputs = yield (outputs, iter_signal)

    def finalize(runtime, cfg, inputs, state, outputs):
        """
        The finalize function is called when the node is no
        longer needed. It can be used to clean up any resources
        allocated by the node.

        """
        pass


Edge
^^^^

**Edges** represent the connections between nodes, defining 
the data flow. The implementation of an edge can vary depending 
on the computational model and whether the edge goes from one 
host to another, or from one process to another within the 
same host, or from one node to another within the same process.
When the system is being configured, the Stableflow platform
determines the appropriate edge implementation based on the
configuration.

In general, edges that span between different hosts will be
implemented with some sort of networked queue, such as zeromq,
whereas edges that span between processes on the same host will
be implemented using some form of shared memory queue. Edges
that span between nodes within the same process can use an
even simpler shared memory mechanism, although this depends
on the computational model for that node.


Functional chain:
^^^^^^^^^^^^^^^^^

A **Functional chain** is a connected group of nodes that 
work together to implement a specific feature or capability 
in the system. Think of it like a pipeline or workflow that
accomplishes one particular task that your users care about.

For example, in a video streaming application, you might have
a functional chain for "video playback" that includes nodes
for:

* Fetching video chunks from storage
* Decoding the video
* Applying filters or effects
* Rendering to screen

While individual nodes might contain programming functions, 
a functional chain operates at a higher level - it often
represents an entire user-facing feature described in your
requirements (like "users can watch videos"). The chain
encompasses all the components needed to deliver that
feature end-to-end.

In systems engineering terminology, these user-facing features
are called "system functions" and are typically described as
"functional requirements" in specification documents. For
example, "The system shall allow users to watch videos" would
be a functional requirement that maps to our video playback
chain.

This concept helps you:
* Map user requirements directly to the parts of your system that implement them
* Understand dependencies between features
* Analyze performance and reliability of specific features
* Make changes to features without accidentally affecting other parts of the system
* Identify and talk about (potentially overlapping) subsets of the system data flow graph.


Computational Model:
^^^^^^^^^^^^^^^^^^^^

A computational model defines the rules for how and when nodes
communicate and process data. Think of it as the "traffic rules"
that govern how messages flow between nodes in your system.
These rules determine important characteristics like whether
your system will behave predictably (deterministic) or not.

Stableflow supports several computational models, each with
different tradeoffs:

1. **Kahn Process Networks (Primary Model)**
   * How it works: Nodes only run when ALL their input data is ready
   * Reading: Blocks (waits) until data is available
   * Writing: Never blocks (always succeeds)
   * Key benefit: Guaranteed predictable behavior - given the same inputs, you'll always get the same outputs
   * Best for: Simulation, testing, and situations where predictability is crucial

2. **Actor Model (Planned)**
   * How it works: Nodes can run as soon as ANY input data is ready
   * Reading: Never blocks (returns immediately if no data)
   * Writing: Never blocks
   * Key benefit: Better performance and resource utilization
   * Trade-off: Behavior can vary between runs
   * Best for: High-performance systems where exact reproducibility isn't critical

3. **Concurrent Sequential Processes (Under Consideration)**
   * How it works: Nodes communicate through synchronized message passing
   * Reading: Blocks until data is available
   * Writing: Blocks until receiver is ready
   * Key benefit: Predictable behavior with direct communication between nodes
   * Trade-off: Can be more complex to reason about
   * Best for: Systems requiring tight coordination between nodes

For most applications, we recommend starting with the Kahn
Process Network model as it provides the best balance of
simplicity and predictability. You can switch to the Actor
model if you need better performance and can tolerate
non-deterministic behavior.

Because the computational model is all about how nodes are
triggered by messages, it is good to think about computational
models as applying to connected subsets of the system graph,
in other words, what can be thought of as functional chains.

For example, in a video streaming application, you might have:
* A deterministic functional chain for video processing (using Kahn Process Networks)
* A high-performance functional chain for real-time user interface updates (using Actor Model)
* A synchronized functional chain for managing user sessions (using CSP)

This ability to mix computational models within well-defined boundaries (functional chains) allows you to:
* Use the right model for each part of your system
* Maintain clear guarantees about behavior where needed
* Optimize performance where determinism isn't critical
* Test and verify critical paths independently
* Clearly communicate the behavior expectations for different system features


---------------
Control Signals
---------------

Stableflow provides a set of control signals for managing 
execution flow and coordinating between components.

Signal Types
^^^^^^^^^^^^

* **Continue**: Indicates that execution should proceed normally.
* **Exit**:     Signals that a process or node should shut down.

  * **Immediate Exit**:  For non-recoverable errors requiring immediate termination.
  * **Controlled Exit**: For graceful shutdowns.

* **Reset**:      Instructs nodes or processes to reset their state.
* **Pause/Step**: Used to pause execution or step through execution one node at a time.

Signal Handling
^^^^^^^^^^^^^^^

* Processes and nodes can emit and handle signals to control the flow of execution.
* The system and hosts listen for signals to manage the overall execution state.

--------------
Execution Flow
--------------

1. **System Start**: The system initializes hosts and processes based on the configuration.
2. **Process Initialization**: Each process sets up its nodes and communication channels.
3. **Node Execution**: Nodes execute their reset functions, then enter their execution loop.
4. **Data Processing**: Nodes process incoming data, produce outputs, and pass data to connected nodes via edges.
5. **Control Signals**: Signals can alter the execution flow, triggering pauses, resets, or shutdowns.
6. **System Shutdown**: The system coordinates a graceful shutdown of all components when execution is complete or upon receiving an exit signal.


-------------
Configuration
-------------

Stableflow applications are configured using structured data (e.g., dictionaries). Configuration specifies:

* **Processes and Nodes**: Definitions of processes and the nodes they contain.
* **Edges**: Connections between nodes, including the type of communication channel.
* **Data Types**: Definitions of data structures passed between nodes.
* **Runtime Options**: Settings for execution behavior (e.g., local vs. distributed execution).

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

Note that dill is a library for serializing (pickling)
Python objects, and enables us to serialize the node
implementation functions so that they can be passed
into dynamically generated system configurations.


---------------------------
Example Node Implementation
---------------------------

Nodes can be implemented as step functions or coroutines.

Step Function Node
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import pl.stableflow.signal
    def step(inputs, state, outputs):
        if 'count' not in state:
            state['count'] = 0
        else:
            state['count'] += 1
        outputs['output']['count'] = state['count']
        if state['count'] >= 10:
            return (pl.stableflow.signal.exit_ok_controlled,)

Coroutine Node
^^^^^^^^^^^^^^

.. code-block:: python

    import pl.stableflow.signal
    def coro(runtime, cfg, inputs, state, outputs):
        count = -1
        signal = (None,)
        while True:
            inputs = yield (outputs, signal)
            count += 1
            outputs['output']['count'] = count
            if count >= 10:
                signal = (pl.stableflow.signal.exit_ok_controlled,)

----------------------
Command-Line Interface
----------------------

Stableflow provides a command-line interface (CLI) for interacting with the system.

Main Commands
^^^^^^^^^^^^^

* **system**: Control the system as a whole.
  * **start**: Start the entire system.
  * **stop**: Stop the system.
  * **pause**: Pause the system.
  * **step**: Step through execution.
* **host**: Control individual hosts.

Example usage:

.. code-block:: shell

    stableflow system start --cfg-path /path/to/config
    stableflow system stop
    stableflow system step

----------
Conclusion
----------

Stableflow's architecture allows developers to build 
scalable, distributed systems by composing nodes into 
processes and hosts within a system. Its structured 
approach to data flow, control signals, and execution
management simplifies the development of complex 
applications in a model driven engineering and
product line engineering context.
