=================================
Stableflow architectural overview
=================================

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
* **Functional chain**: Represents a contiguously connected subset of the nodes and edges in the system, and is normally associated with a high level system function.
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


Node Lifecycle:
^^^^^^^^^^^^^^^

1. **Configuration**: Configuration data is processed, nodes instantiated, queues created and static schedules computed.
2. **reset**: All nodes are reset, allocating resources as required. If a reset function fails, the system is finalized and exits early.
3. **pause/step**: If the system is paused, single-stepping is handled.
3. **run**: If the system is not paused, nodes are stepped continuously.
4. **Finalize**: If the system shuts down, finalize is called to clear resources.

TODO: Draw a state machine diagram to illustrate the operation
      of pl/stableflow/proc/mainloop.py


Computational Model:
^^^^^^^^^^^^^^^^^^^^

The following computational models are possible for functional chains in
the system:-

* **Concurrent sequential processes** - Blocking reads and blocking writes. Nodes trigger when at least one message is ready. Determinism is guaraneed.
* **Kahn process network** - Blocking reads and nonblocking writes. Nodes trigger when all inputs are ready. Determinism is guaranteed.
* **Actor model** - Nonblocking reads and writes. Nodes trigger when at least one message is ready. Nondeterministic, but provides higher utilization.

NOTE: Currently only Kahn process models are implemented.

Data Flow and Communication
---------------------------

Stableflow uses a message-passing mechanism for communication
between nodes, processes, and hosts.

Edges
^^^^^

* **Edges** represent the connections between nodes, defining the data flow.
* Edges can be:

  * **Intra-Process**: Communication between nodes within the same process.
  * **Inter-Process**: Communication between nodes in different processes on the same host.
  * **Inter-Host**: Communication between nodes on different hosts.

NOTE FROM PS: Just to be clear; these words encapsulated with ** ** - are these actually script keywords, or just general concepts, or both in some cases? I'm not certain if we are describing how the system works conceptually, or whether these are script keywords?
NOTE FROM WP: These are concepts, not keywords. We should rewrite this to make it clear.
NOTE FROM PS: Suggestion: If these are keywords, 'Intra-Process' and 'Inter-Process' are incredibly similar - this could be a place where the user could introduce bugs into their design with a very trivial typo that would be difficult to spot... suggest 'Process' and 'Intra-Process' instead... 
NOTE FROM WP: Not keywords, but language could be improved for clarity.

Queues
^^^^^^

* **Queues** are used for inter-node communication, handling message passing along edges.
* Depending on the edge type, different queue implementations are used (e.g., in-memory queues for intra-process communication, network-based queues for inter-host communication).

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

NOTE FROM PS: Suggest moving the below paragraph above the list here

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

NOTE FROM PS: Should the "process initialization" item be broken into two phases?  Node Reset and Node Execution?  Also, Node's don't execute their reset functions, right? I thought the Process executes them in an iteration loop...this language may suggest the nodes are responsible for resetting themselves.)
NOTE FROM PS: Why are Data Processing and Control Signals separate steps here?  Aren't these integral parts of the system execution?
NOTE FROM PS: If this section is designed to describe distinct phases of execution, then am I understanding this wrong?
NOTE FROM PS: I'm not clear on how control signals fit in.  How are they passed between things?  How are they handled?  By a function? or as parameters to other functions?
NOTE FROM WP: Signals came in as a means for the application layer nodes to communicate with the runtime. I'm very much open to re-engineering how they work.

-------------
Configuration
-------------

Stableflow applications are configured using structured data (e.g., dictionaries). Configuration specifies:

NOTE FROM PS: Should we be explicit that this is a JSON text file? - or is that optional?
NOTE FROM WP: It can be a text file or it can be an API call. The API call is central to the automation of model transformation.

* **Processes and Nodes**: Definitions of processes and the nodes they contain.
* **Edges**: Connections between nodes, including the type of communication channel.
* **Data Types**: Definitions of data structures passed between nodes.
* **Runtime Options**: Settings for execution behavior (e.g., local vs. distributed execution).

Example (incomplete) configuration snippet:

NOTE FROM PS: Is the below snippet intended to be JSON?
NOTE FROM WP: This example shows Python dictionaries, to intoduce it using a fully programmatic example. But I need to make that intent clear.

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

NOTE FROM PS: Most of this is self-explanatory, but not clear on the 'data' thing - what is it defining?
NOTE FROM PS: What is py_dill?
NOTE FROM WP: I should probably try to make the data section optional and remove it from the example, or explain that it is to define the data types used above.
NOTE FROM WP: py_dill is a pickle of a function - I need to explain that.


---------------------------
Example Node Implementation
---------------------------

NOTE FROM PS: Talk about the various languages that are supported.  The following example is python
NOTE FROM PS: Not sure how 'coroutines' work - I guess this is a python specific concept? How
NOTE FROM WP: Yes, we need to do a better job of explaining that.

Nodes can be implemented as step functions or coroutines.

Step Function Node
^^^^^^^^^^^^^^^^^^

NOTE FROM PS: Is this readme also intended to be a API Spec? We may need to 
provide an explanation of these function parameters - particularly 'state'
and its lifecycle.
NOTE FROM PS: Also, should there not be a 'reset' function here, just to be complete?
NOTE FROM WP: Yes, it should be more complete, and yes, it is an introduction to the API spec.

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

NOTE FROM PS: So when you 'start' the system, it will always run in the background? - as a daemon? - and immediately return control to the shell? - in which case I assume there is a command to see it's current running time-step? or status?
NOTE FROM WP: No, it could be running on the local machine, or it could be running on a remote machine. Whichever machine it DOES run on though, it will be a daemon, or something similar.
NOTE FROM WP: I **Do** need to give some thought about what happens when the remote machine restarts ... does the daemon also restart and attempt to reconnect?

NOTE FROM PS: Just a thought - I could imagine breaking "system start" into "system init" and "system run" and a separate "system reset" because if the initialization phase is long and complex, you might want to do that ahead of time before running the simulation... also I could imagine a "system run <timesteps>" function that would run a certain number of steps before stopping. - you can then keep calling "system run <timesteps>" to advance the simulation by specific chunks of time... "system run 1" would be equivalent to "system step" I guess...
NOTE FROM WP: The phased system start is a good idea. Definitely things to give some careful thought to.

NOTE FROM PS: I could also imagine a "system status <node/nodes/all>" .. or something... to get data associated with the current state.
NOTE FROM WP: Yes, that is something we could add.

NOTE FROM PS: I assume there's a lot more CLI commands?
NOTE FROM WP: Yes, there are, for host and process as well. We should add them to the README.
NOTE FROM WP: I can imagine that the CLI will evolve and grow as well.

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
