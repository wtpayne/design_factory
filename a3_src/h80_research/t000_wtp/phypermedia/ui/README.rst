===================================
Hyperview UI Component Architecture
===================================

--------
Overview
--------

The Hyperview UI component generation system is designed to create and manage dynamic, 
server-side UI components within the Stableflow framework. It implements a pub-sub 
pattern for component communication and uses HTMX for dynamic client-side updates.

-------------
Core Concepts
-------------

Component Context (UiContext)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The UiContext serves as both a pub-sub message broker and component factory. It:

* Manages component lifecycles
* Routes messages between components using regex-based filtering
* Provides context management for safe component cleanup
* Maintains weak references to components to prevent memory leaks

Components (Com)
^^^^^^^^^^^^^^
Components are the fundamental UI building blocks that:

* Inherit from Pydantic BaseModel for data validation
* Support HTML and SVG rendering
* Can be static or dynamic (SSE-based)
* Maintain their own state and hierarchy
* Support HTMX attributes for client-side interactions

Component Data Model
^^^^^^^^^^^^^^^^^^^
Each component maintains metadata through ComData:

* ``id_com``: Unique component identifier
* ``list_id_parent``: Component containment hierarchy
* ``list_id_page``: SSE topic subscriptions
* ``is_valid``: Component lifecycle state
* ``is_dyn_sse``: Server-Sent Events capability flag
* ``media_type``: Content type (default: text/html)

Message Flow
-----------

Component Communication
^^^^^^^^^^^^^^^^^^^^^^
Components communicate through a pub-sub pattern where:

1. Components subscribe to message patterns using regex filters
2. Messages are routed through the UiContext broker
3. Components process received messages in their step function
4. Weak references ensure proper cleanup of deleted components

Dynamic Updates
^^^^^^^^^^^^^
The system supports dynamic updates through:

* Server-Sent Events (SSE) for real-time updates
* HTMX attributes for client-side DOM manipulation
* Component invalidation and regeneration

Example Configuration
-------------------

Component Definition
^^^^^^^^^^^^^^^^^^
.. code-block:: python

    with ctx.com(
        filt           = 'com_1',
        id_com         = 'com_1',
        list_id_parent = ['app'],
        is_dyn_sse     = True
    ) as com_1:
        html.div('Content',
                 data_hx_trigger = 'click',
                 data_hx_target  = '#com_1',
                 data_hx_get     = '/endpoint')

Integration with Stableflow
-------------------------
The component operates as a Stableflow node that:

* Processes input messages through the coro function
* Maintains component state across iterations
* Generates UI components on initialization
* Routes messages to appropriate components

Best Practices
-------------

1. Component Lifecycle
   * Use context managers (with statements) for component creation
   * Properly handle component cleanup through invalidation
   * Maintain clear parent-child relationships

2. Message Handling
   * Use specific regex patterns for message filtering
   * Implement proper message validation
   * Handle component deletion gracefully

3. Dynamic Updates
   * Use SSE for real-time updates when needed
   * Implement proper HTMX attributes for client interactions
   * Consider performance implications of dynamic components

Limitations and Considerations
---------------------------

1. Memory Management
   * Components must be properly invalidated to prevent memory leaks
   * Weak references are used to allow garbage collection

2. Message Routing
   * Complex regex patterns may impact performance
   * Message loops should be avoided

3. Scalability
   * Consider the number of SSE connections for dynamic components
   * Monitor message broker performance with many components

Future Enhancements
-----------------

1. Component Templates
   * Support for reusable component templates
   * Better component composition patterns

2. Performance Optimizations
   * Message routing optimizations
   * Component rendering caching

3. Developer Tools
   * Component debugging utilities
   * Message flow visualization