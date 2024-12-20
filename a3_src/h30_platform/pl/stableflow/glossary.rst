========
Glossary
========

This document provides definitions for key terms 
used in the Stableflow documentation.


Core concepts
-------------

.. glossary::

  Actor model
    A computational model where components communicate 
    through non-blocking message passing, allowing
    for concurrent execution but with nondeterministic
    behavior.

  Computational model
    A formal model that proves how desirable
    computational properties such as determinism
    can arise from design decisions such as how
    components in a computational system communicate
    with one another.
  
  Data flow
    A type of computational system where data moves through a system of 
    connected components, with each component processing 
    and transforming the data before passing it along.

  Edge
    A connection between nodes in a Stableflow system 
    that carries data either across a network or within 
    a host.

  Functional Chain
    A connected sequence of nodes that together implement 
    a specific feature or capability of the system.

  Host
    A physical or virtual device that runs one or more 
    processes in a Stableflow system.

  Kahn Process Network
    A computational model where components communicate 
    through blocking reads and non-blocking writes, 
    ensuring deterministic behavior regardless of timing.


Engineering concepts
--------------------

.. glossary::

  Model Driven Engineering
    An approach to system development where functionality 
    is first prototyped and validated as a model before 
    being deployed to production.

  Product Line Engineering
    An approach to developing a family of related products 
    using a common core architecture with systematic 
    variations.


System components
-----------------

.. glossary::

  Node
    A basic computational unit in Stableflow that processes 
    data. Nodes are connected by edges to form the system's 
    data flow graph.

  Process
    An execution context that contains one or more nodes, 
    allowing for concurrent computation.

  System Variant
    A specific configuration of a Stableflow system, 
    tailored for a particular use case, deployment 
    scenario, or client requirement. 