==========
Stableflow
==========


Introduction
------------

This document provides a brief introduction to the
stableflow system covering it's intended purpose, 
benefits and key concepts needed to understand how
it operates and what benefits it provides.


Executive summary
-----------------

Stableflow is a framework for designing and operating 
distributed systems.

It is most suited to continuously operating systems
composed of data flows or data processing pipelines
such as sensor data processing, continuous workflow
processing, or "digital twin" simulation systems.

It is designed to make it easy to adapt and tailor
such systems for different testing, simulation and 
deployment scenarios, making it especially useful for
medium to large scale projects where effort needs 
to be expended on quality assurance, e.g. evidenced
safety cases.

These benefits come at the expense of imposing a 
data-flow oriented architecture, which means that it
is much less suitable for building event-driven or
reactive applications, such as user-interfaces or
CRUD applications.


When to use Stableflow
----------------------

Stableflow is ideal for:

* Distributed "cyber-physical" systems
* Systems of cooperating "agents"
* Systems requiring rigorous testing and simulation before or during deployment
* Building families of related systems with a shared architecture
* Projects where architectural exploration and optimization are key concerns
* Teams adopting model-driven development practices

Stableflow may not be the best choice for:

* Small scale projects
* Inherently event-driven applications such as user interfaces or web APIs
* Projects with minimal need for simulation or testing
* Projects with minimal need for different system variants or configurations


Example use cases
-----------------

The following examples illustrate the sort of use
cases that Stableflow is intended to support.


Autonomous vehicle development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider a tier 1 automotive supplier developing
a machine vision system for autonomous vehicles:

* Base architecture: 

  #. Image capture
  #. Object detection
  #. Object tracking
  #. Track fusion
  #. Scene understanding
  #. Control output

* Variants:

  * Development: Isolated functional chains running on developer workstations using recorded data with visualization and debugging
  * Model-in-the-loop: Integrated systems running on engineering servers with simulated sensors, communications and vehicle responses
  * Hardware-in-the-loop: Integrated systems running on hardware development boards with recorded or simulated sensor data
  * Test drive: Integrated systems running on development hardware with data recording for resimulation
  * Production: Integrated systems running on production hardware fusing data across one or more vehicles

    * Economy: Essential sensors only, cost-optimized compute
    * Mid-range: Balanced sensor suite, shared compute
    * High-end: Multiple high-res cameras, dedicated compute, vehicle-to-vehicle communication with sensor fusion

It should be clear that the development process requires
many different variants of the system to be able to run
in different configurations and on different hardware.
Stableflow supports this approach to systems development by
providing:

* Single framework supporting all development phases
* Automated generation of variant-specific configurations
* Deterministic replay of recorded data for testing
* Clear traceability from requirements to deployment
* Systematic validation across vehicle configurations


Business process automation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider a software company building business
process automation systems for various clients.

* Base architecture:

  #. Data integration (internal wiki, network shares, etc.)
  #. Data transformation (tagging, classification, indexing, etc.)
  #. Task ingestion (email, messenger etc.)
  #. Plan creation / query generation
  #. Agent assignment (human or LLM)
  #. Task execution monitoring
  #. Report generation
  #. Quality monitoring and feedback elicitation 

* Variants:

  * Invoice processing system for a small business client
  * Bid processing system for a public sector client
  * Superset system for internal integration and regression testing

In this case, rather than different system variants
being produced for different stages of the development
process, we instead produce different system variants
for different clients, reflecting how the base product
has been tailored to their individual needs and 
requirements. In particular, because the different
variants are able to be generated automatically from
the base system, rolling out improvements, bugfixes
and security patches can be done in a much more
controlled and systematic manner.

* Single framework supporting all clients
* Automated generation of client-specific tailored configurations
* Systematic synchronization and testing of changes across variants


Core Concepts
-------------

The following sections describe some core concepts
that will help you understand how Stableflow works
and what benefits it provides.


Data flow
^^^^^^^^^

A Stableflow system is a distributed data flow graph,
composed of nodes and edges, where nodes can reside
on different devices (called "hosts"), and edges
represent data flows either across a network or within
a host. Key concepts to understand are:

* **Hosts**: Physical or virtual devices that run processes
* **Processes**: Execution contexts that contain nodes
* **Nodes**: Basic computational units that process data
* **Edges**: Connections that carry data between nodes
* **Functional Chains**: Connected groups of nodes implementing specific features

The functional behaviour of a system is defined by
the data flow graph which is formed from nodes and
edges. Different parts of the functional behaviour
(functional chains) can be represented by different
paths through the data flow graph. Nodes can be
allocated to different processes, allowing computation
to be run concurrently or in parallel, and those
processes can be allocated to different hosts, allowing
computation to be run in a distributed manner.


Computational models
^^^^^^^^^^^^^^^^^^^^

A computational model is an intellectual tool that
helps us talk about concurrency and parallelism.
They mainly give us the ability to talk about how
communication within a system impacts the behaviour
and guarantees that the system as a whole can provide.

Stableflow supports multiple computational models that 
determine how nodes communicate and process data:

#. **Kahn process network**

   * Nodes use non-blocking writes and blocking reads for communication
   * Nodes run when all inputs are available
   * Deterministic behavior
   * Best when quality assurance requires accurate simulation and testing
   * Computational resources may be uner-utilised

#. **Actor model**

   * Nodes use non-blocking writes and non-blocking reads for communication
   * Nodes run as soon as any one input is ready
   * Nondeterministic behavior
   * Best for efficient use of computational resources
   * Simulation and testing are only approximate and functional behaviour is not guaranteed

Both kahn process networks and actor models are
data flow models, and both are based on the idea
of data driven execution.


Model driven engineering
^^^^^^^^^^^^^^^^^^^^^^^^

Model driven engineering is an approach to software
and systems development where functionality is 
prototyped and validated as a model before being 
deployed to production.

For a lot of software intensive projects, there
is no meaningful difference between the model and
the production system, so in these contexts model
driven engineering can be considered more as a
philosophy and an approach to how test environments
and test mocks are constructed.

In Stableflow, as with many other model driven
engineering approaches, the system architecture
is made programmable so that it can be transformed
automatically into different variants, including
test variants where key inputs are replaced with
test data, or key components are replaced with
mocks.

By making the architecture programmable, we enable:

* Automatic generation of system variants
* Rapid adaptation to different deployment scenarios
* Search-based optimisation of system architecture
* Support for AI-assisted system design

When Kahn process network semantics are used, we
can make strong guarantees about functional behaviour
based on the results of simulation and modeling.


Product line engineering
^^^^^^^^^^^^^^^^^^^^^^^^

The idea of product line engineering is most applicable
to businesses that produce multiple closely related
products, for example in business-to-business products
where functionality is often tailored for each customer.

It is very common for such products to be built using
some common core with some functionality to support
configurability e.g. a plugin architecture around a
common core system.

The programmable architecture that Stableflow provides
enables us to take a systematic approach to product
line engineering, using scripts to generate different
product variants as well as supersets for integration
testing.
