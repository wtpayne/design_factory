==========================================
Software architecture description template
==========================================

This appendix is a MANDATORY part of the (SDSMCS).
It provides the content requirements for the
Software architecture description.

#. If the section numbering used below is not used, 
   the developer shall provide an appendix in the 
   SAD with a traceability matrix mapping from the 
   section numbers and titles below to the section 
   numbers and titles used in the developer's SAD.
#. If there is such a traceability mapping appendix,
   it shall be referenced in Section 1.3.


Purpose
-------

The Software architecture description documents the
software architecture, including the approach,
important design decisions, rationale, and tradeoffs.
It provides diagrams and text to document the various
architectural views from different perspectives and
serves as the basis for the detailed design.


References
----------

* (SDSMCS) Adams, R. J., S. Eslinger, K. L. Owens, 
  J. M. Tagami, and M. A. Zambrana, Software 
  Development Standard for Mission Critical Systems
  (SDSMCS), Aerospace Report No. TR-RS-2015-00012, 
  March 17, 2014, The Aerospace Corporation. This 
  is the same as SMC Standard SMC-S-012, Software
  Development Standard.


Content Requirements
--------------------

This template contains the required content of the
SAD. See Section 3 of the Software Development 
Standard for Mission Critical Systems (SDSMCS) for
definitions of all italicized words or phrases.


1. Scope
--------

This section shall be divided into the following
paragraphs.


1.1 Identification
^^^^^^^^^^^^^^^^^^

This paragraph shall contain a full identification 
of the system and the software to which this
document applies, including, as applicable,
identification number(s), title(s), abbreviation(s),
version  number(s), and release number(s).


1.2 System overview
^^^^^^^^^^^^^^^^^^^

This paragraph shall briefly state the purpose of 
the system and the software to which this document 
applies. It shall: 

#. Describe the general nature of the system and 
   software
#. Summarize the history of system development, 
   operation, and maintenance
#. Identify the project sponsor, acquirer, user, 
   developer, and support organizations
#. Identify current and planned operating and user
   sites


1.3 Document overview
^^^^^^^^^^^^^^^^^^^^^

This paragraph shall summarize the purpose and 
contents of this document. This paragraph shall 
describe any security or privacy considerations 
associated with its use.


1.4 Relationship to other documents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe the relationship, 
if any, of the SAD to other project documents.


2. Referenced documents
-----------------------

This section shall list the number, title, revision, 
and date of all documents referenced in this plan. 
This section shall also identify the source for 
all documents not available through normal
Government stocking activities.


3. Software architecture plans and processes
--------------------------------------------

This section shall be divided into paragraphs as
specified below to describe the plans and processes
for developing the software architecture.


3.1 Software architecture plans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The paragraph shall provide an overview of the 
software architecture plans and activities.

This paragraph shall identify the software team
members responsible for developing and evaluating
the software architecture, including their
responsibilities. 

This paragraph shall also identify other
stakeholders in the software architecture,
including their roles.


3.2 Software architecture processes and tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe how the software
architecture has been developed in accordance
with the detailed methods, techniques and tools
specified in the Software Development Plan (SDP).

This paragraph shall identify the architecture
modeling tools and other tools and techniques
(e.g., Unified Modeling Language) used to develop
and maintain the software architecture, including
representing, documenting, and analyzing the
software architecture; performing consistency
analyses; and mapping requirements to architectural
components.

This paragraph shall describe how the software
architecture evolves from high-level architectural
components and interfaces to lower level components
and interfaces and how the lower-level components
and interfaces will transition to the software
design.

This paragraph shall identify the scope of the
software architecture; that is, what design
decisions are and are not considered part
of the software architecture.


4. Software architecture requirements and approach
--------------------------------------------------

This section shall be divided into paragraphs as
specified below to describe the software architecture
requirements and approach.


4.1 Software architecture critical and driving requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall identify: 

#. All critical requirements specified in the SDP 
   (See (SDSMCS) Section 4.2.5).
#. All other nonfunctional requirements that are
   drivers of software architecture decisions.
#. All functional requirements that are drivers
   of software architecture decisions.

This paragraph shall contain a prioritized list of
these critical and driving requirements according
to their importance in software architecture
decisions.


Note 1
^^^^^^

Nonfunctional requirements are also called “quality
attributes.” See definition of “nonfunctional
requirement” in (SDSMCS), Section 3, Terms.


Note 2
^^^^^^

Providing the critical and driving requirements
identifiers n lieu of the actual requirement
statements is acceptable.


4.2 Software architecture approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall discuss the selected
architectural approach, as well as alternatives
that were considered to address the critical and
driving requirements specified in paragraph 4.1
above. This paragraph shall describe the analyses
and trade studies that were performed to evaluate
the architectural alternatives for their ability
to satisfy the critical and driving requirements.
This paragraph shall describe how the results of
these analyses and trade studies support the
selected software architecture approach.


4.3 Software architecture evaluations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe all evaluations
performed, or to be performed, of the selected
software architecture, either by a developer
team, an acquirer team, or a combined team. For
evaluations that have been performed, this
paragraph shall describe the results of these
evaluations, with references to analysis details,
especially with respect to the ability of the
selected software architecture to meet the
critical and driving requirements specified 
in paragraph 4.1 above. This paragraph shall
describe any changes to software architecture
decisions as a result of these evaluations.


4.4 Software architecture risks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall identify the software risks
for the selected software architecture. This
paragraph shall describe any analyses performed to
evaluate these risks, the results of those analyses,
with references to analysis details, and any
mitigation actions taken or being undertaken for
the risks.


5. Overall software architecture description
--------------------------------------------

This paragraph shall provide the overall software
architecture for all software on the contract, 
including all categories of software covered by
the contract (see Section 1.2.5.6 of the (SDSMCS)).

The overall software architecture description
provided in this section shall be at the level
of granularity that crosses software items. The
following topics shall be addressed to describe
the overall software architecture. The following
topics may be discussed in any order chosen by
the developer.

* A high-level description and diagrams of the 
  software architecture.
* A description of how the software architecture
  integrates into the system and subsystem
  architectures and addresses the system 
  operations concept and the primary threads
  that the system supports.
* A description of the relationship between the
  software architecture and any external systems.
* A description of how the software architecture
  addresses the critical and driving requirements
  (identified in paragraph 4.1 above) and their 
  impact on the architecture.
* A description of the architecture style(s),
  applied design principles, key software
  architectural patterns, and constraints.
* A description, expressed in a set of use cases,
  or equivalent, of how the software will interact
  with the users and with other systems and
  subsystems to meet system and software
  requirements, including use cases, or equivalent,
  for nominal and off-nominal (e.g., alternative,
  error, and fault) scenarios.
* Descriptions of the following software architectural
  views, including both diagrams and detailed textual
  descriptions. All diagrams shall be accompanied by
  descriptions of the functionality and behavior
  provided by the components. This paragraph shall
  describe how the views address the concerns of the
  relevant stakeholders. This paragraph shall provide
  the criteria used to determine consistency among
  the architectural views. If additional views are
  used by the developer to describe the software
  architecture, those views shall be included here.
  The views shall include the following information,
  along with the rationale and the alternatives that
  were explored:

  #. Descriptions, including diagrams and text, of
     logical architecture components, connectors,
     and interfaces, both internal and external.
     This paragraph shall include the functionality
     of each component and connector and the
     interactions and dependency relationships
     among components. This paragraph shall include
     the conceptual and logical data schema for key
     data structures, along with a description of
     the relationship between these data structures
     and the software architecture and algorithms.
  #. Descriptions, including diagrams and text, of
     the architecture component behaviors, 
     interactions, and collaborations required by
     each use case, or equivalent, using techniques
     such as sequence diagrams, activity diagrams,
     and state machine diagrams. This paragraph
     shall also include descriptions of states and
     modes and transitions among them, as applicable.
     Descriptions of important internal component
     behaviors shall also be included.
  #. Descriptions, including diagrams and text, of
     the physical organization of the software.
     This paragraph shall include the target
     processors, both physical and virtual, on
     which components will execute, and their
     interconnections. This paragraph shall
     describe how software components, connectors,
     and other elements will be allocated to the
     target processors. This paragraph shall
     describe how and where system data are stored
     and accessed. This paragraph shall identify
     important software-to-hardware interfaces.
     This paragraph shall identify any special
     purpose hardware and any special target
     processor characteristics that have software
     impacts.
  #. Identification and descriptions of the software
     items and other software in the overall software
     architecture, including all categories of
     software. This paragraph shall also include
     the mapping of the software items and other
     software to the software architectural
     components.

* Identification of commercial off-the-shelf (COTS)
  software products that will be used to implement
  part or all of any software architecture components,
  including:

  #. Relationship of each COTS software product to
     the software architecture component(s) it
     implements, what part(s) of the component(s)
     are implemented by each COTS software product,
     and whether the full capabilities of the COTS
     software products are used.
  #. Discussion of alternative products evaluated,
     the evaluation criteria used, and how each
     product met the evaluation criteria.
  #. Discussion of the data rights, including
     licensing, associated with each COTS software
     product.
  #. Discussion of how any mismatches between the
     COTS software product and the architecture
     will be resolved.

* Identification of reusable software products,
  i.e., noncommercial off-the-shelf, that will be
  used to implement part or all of any software
  architecture component, including:

  #. Relationship of each reusable software product
     to the software architecture component(s) it
     implements, what part(s) of the component(s)
     are implemented by each reusable software
     product, and whether the full capabilities of
     the reusable software products are used.
  #. For each reusable software product, a 
     description of what is being reused (e.g.,
     requirements, design, algorithms, code, test
     cases), and the magnitude of expected
     modifications to the reusable software
     component.
  #. Discussion of alternative products evaluated,
     the evaluation criteria used, and how each
     product met the evaluation criteria.
  #. Discussion of the data rights associated with
     each reusable software product.
  #. Discussion of how any mismatches between the
     reusable software product and the architecture
     will be resolved.

* Description of how and where the architecture 
  supports Modular Open Software Approach (MOSA)
  principles.
* Description of how and where the architecture
  supports net-centricity principles, if applicable.
* Description of how and where the software
  architecture supports information assurance and
  cyber-security requirements, including security
  assurance assessment and certification and
  accreditation activities). Examples of supporting
  descriptions include:

  #. Principles that guide the security design of
     the software within the system (e.g., use of
     defense-in-depth, modularity and isolation of
     security-critical functionality, nonbypassability
     of security function chokepoints).
  #. Identification of system security policies
     (e.g., identification and authentication,
     access control, confidentiality, integrity,
     data provenance, nonrepudiation, accountability),
     and how they will be enforced by the software
     architecture.
  #. Identification of policy decision points and
     policy enforcement points within the software
     architecture, including the technology and
     product choices for each.
  #. Identification of security domains, security
     modes (e.g., system high, dedicated), and
     cross-domain solutions, including the types
     of data that they must handle.
  #. Detailed descriptions for aspects of the
     system security design that require a high
     level of security assurance (e.g., key
     management design supporting National Security
     Agency Type 1 encryption).
  #. Detailed descriptions for aspects of the
     software architectural design that help
     support cyber resilience, that is, the
     ability of a system to operate in the face
     of persistent cyber attacks and still support
     mission success (e.g., redundancy of components,
     request throttling, virtualization or
     partitioning of resources, deployment of
     security application tools).

* Description of how and where the software
  architecture implements the supportability
  of the system, that is, the repair, scheduled
  maintenance, and preventive maintenance required
  to retain the system in, or restore the system
  to, a state in which it can perform its required
  functions, including the ability of personnel to
  install, configure, and monitor computer products,
  identify exceptions or faults, debug or isolate
  faults to root-cause analysis, and provide
  hardware or software maintenance in pursuit of
  solving a problem and restoring the product into
  service.
* Description of how and where the software
  architecture supports system reliability,
  maintainability, availability (RMA), and safety,
  including the architectural decisions made to
  support RMA and safety, the fault management
  architecture, use of other architectural
  features to address RMA and safety (e.g., 
  redundancy, automated failover, fault tolerance),
  and uniform exception handling and recovery
  methods.
* If applicable, a description of how and where
  the software architecture supports the human
  systems interface to account for human
  capabilities and limitations in the operations,
  maintenance, and support of the system. This
  description shall include architecture decisions
  concerning user interface screen design and user
  interaction mechanisms for user input and output.
  This description shall include, if applicable:

  #. How the software architecture isolates the 
     user interface from the application logic.
  #. Principal design decisions made to ensure 
     usability by the human operator.
  #. Principal design decisions made to ensure 
     that the user interface is internally 
     consistent across all software in the overall 
     software architecture.
  #. Principal design decisions made to ensure 
     that the user interface is consistent with 
     widely used application user interfaces.
  #. Principal design decisions made to ensure 
     the quantity and frequency of data presented 
     to the operator, including alarms, warnings, 
     and error messages, are able to be assimilated 
     and responded to by the operator within the 
     needed response time.
  #. Applicable human systems interface standards 
     (e.g., graphical user interface (GUI) 
     standards) and how those standards are used 
     within the architecture.

* Description of how the software architecture
  supports the selected software development
  lifecycle model(s) and the integration of
  software and hardware in each software build
  and system increment.
* Discussion of other principal and architecture-wide
  design decisions that are not covered by the above
  items. Examples include the following:

  #. Applicable standards (e.g., interface standards, 
     open system standards) and how those standards 
     are used within the architecture.
  #. Application programming interfaces (APIs) to 
     be used.
  #. Algorithms to be used.
  #. Communications mechanisms (e.g., publish and 
     subscribe message passing, calling sequences, 
     shared memory, sockets) to be used between 
     software entities and under which circumstances 
     each mechanism is to be used.
  #. Definitions of uniform data storage and access 
     methods.

* Requirements traceability. This paragraph shall
  provide bidirectional traceability:

  #. Between the software architecture components 
     and the software requirements and software 
     interface requirements.
  #. Between the use cases, or equivalent, and 
     the software requirements and software 
     interface requirements.


6. Software item architecture description
-----------------------------------------

This paragraph shall provide the software 
architecture for the individual software items 
on the contract, including all categories of
software covered by the contract (see Section
1.2.5.7 of the (SDSMCS)). This paragraph shall
be divided into subparagraphs to describe the
software architecture of each software item.
The paragraphs containing an “.x” in their
numbers and an “x” in their names shall be
repeated for each software item “x.”


6.x Software architecture description for software item x <Insert Name>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe the software architecture
for software item x. This software item architecture
description for software item x may be included in
this paragraph or in a separate appendix that is
referenced from this paragraph. The software item
architecture description provided in this paragraph
shall be at the level of granularity that includes
all the software units in the software item. The
following topics shall be addressed to describe the 
software item architecture. (The following topics
may be discussed in any order chosen by the developer.)

* A high-level description and diagrams of the 
  software item architecture. This paragraph shall 
  also include a description of how the software 
  item architecture evolves from and is consistent 
  with the overall software architecture described 
  in paragraph 5 above.
* A description of how the software item architecture 
  integrates into the system and subsystem architectures 
  and how the software item architecture addresses 
  the system operations concept and the primary 
  system threads that the software item supports.
* A description of the relationship between the 
  software item architecture and any external 
  systems.
* A description of how the software item architecture 
  addresses the critical and driving requirements, 
  i.e., identified in Paragraph 4.1 above, allocated 
  to software item x and their impact on the software 
  item architecture.
* A description of the architecture style(s), applied 
  design principles, key software architectural 
  patterns, and constraints that apply to the 
  software item architecture.
* A description, expressed in a set of use cases, 
  or equivalent, of how the software item will 
  interact with the users and with other systems 
  and subsystems to meet system and software 
  requirements, including use cases, or equivalent, 
  for nominal and off-nominal (e.g., alternative, 
  error, and fault) scenarios.
* Descriptions of the following software architectural 
  views, including both diagrams and detailed 
  textual descriptions. All diagrams shall be 
  accompanied by descriptions of the functionality 
  and behavior provided by the software item 
  architecture components. This paragraph shall 
  describe how the views address the concerns of 
  the relevant stakeholders. This paragraph shall 
  provide the criteria used to determine consistency 
  among the software item architectural views. If 
  additional views are used by the developer to 
  describe the software item architecture, those 
  views shall be included here. The views shall 
  include the following information for the 
  software item architecture, along with the 
  rationale and the alternatives that were explored:

  #. Descriptions, including diagrams and text, 
     of logical software item architecture 
     components, connectors, and interfaces, 
     both internal and external. This paragraph 
     shall include the functionality of each 
     component and connector and the interactions 
     and dependency relationships among components. 
     This paragraph shall include the conceptual 
     and logical data schema for key data 
     structures, along with a description of the 
     relationship between these data structures 
     and the software item architecture and 
     algorithms.
  #. Descriptions, including diagrams and text, 
     of the software item architecture component 
     behaviors, interactions, and collaborations 
     required by each use case, or equivalent, 
     using techniques such as sequence diagrams, 
     activity diagrams, and state machine diagrams. 
     This paragraph shall also include descriptions 
     of states and modes and transitions among them, 
     as applicable. Descriptions of important 
     internal component behaviors shall also be 
     included.
  #. Descriptions, including diagrams and text, 
     of the physical organization of the software 
     item. This paragraph shall include the physical 
     and virtual target processors on which software 
     item architecture components will execute and 
     their interconnections. This paragraph shall 
     describe how software item architecture 
     components, connectors, and other elements 
     will be allocated to the target processors. 
     This paragraph shall describe how and where 
     system data created or used by the software 
     item are stored and accessed. This paragraph 
     shall identify important software-to-hardware 
     interfaces. This paragraph shall identify any 
     special-purpose hardware and any special 
     target processor characteristics that have 
     impacts on the software item.
  #. Identification and descriptions of the 
     software units in the software item architecture. 
     This paragraph shall also include the mapping 
     between the software units and the software 
     item architectural components.

* Identification of commercial off-the-shelf (COTS) 
  software products that will be used to implement 
  part or all of any software item architecture 
  components, including:

  #. Relationship of each COTS software product to
     the software item architecture component(s) 
     it implements, what part(s) of the component(s) 
     are implemented by each COTS software product, 
     and whether the full capabilities of the COTS 
     software products are used.
  #. Discussion of alternative products evaluated, 
     the evaluation criteria used, and how each 
     product met the evaluation criteria.
  #. Discussion of the data rights, including 
     licensing, associated with each COTS software 
     product.
  #. Discussion of how any mismatches between the 
     COTS software product and the software item 
     architecture will be resolved.

* Identification of reusable software products, 
  i.e., noncommercial off-the-shelf, that will 
  be used to implement part or all of any software 
  item architecture component, including:

  #. Relationship of each reusable software product
     to the software item architecture component(s)
     it implements, what part(s) of the component(s)
     are implemented by each reusable software
     product, and whether the full capabilities
     of the reusable software products are used.
  #. For each reusable software product, a
     description of what is being reused (e.g.,
     requirements, design, algorithms, code,
     test cases), and the magnitude of expected
     modifications to the reusable software
     component.
  #. Discussion of alternative products evaluated,
     the evaluation criteria used, and how each
     product met the evaluation criteria.
  #. Discussion of the data rights associated with
     each reusable software product.
  #. Discussion of how any mismatches between the
     reusable software product and the software
     item architecture will be resolved.

* Description of how and where the software item 
  architecture supports Modular Open Software 
  Approach (MOSA) principles.
* Description of how and where the software item 
  architecture supports net-centricity principles, 
  if applicable.
* Description of how and where the software item 
  architecture supports information assurance and 
  cyber-security requirements, including security 
  assurance assessment and certification and 
  accreditation activities). Examples of supporting 
  descriptions include:

  #. Principles that guide the security design of 
     the software item within the system (e.g., 
     use of defense-in-depth, modularity and 
     isolation of security-critical functionality, 
     nonbypassability of security function
     chokepoints).
  #. Identification of system security policies 
     (e.g., identification and authentication, 
     access control, confidentiality, integrity, 
     data provenance, nonrepudiation, accountability)
     and how they will be enforced by the software
     item architecture.
  #. Identification of policy decision points and
     policy enforcement points within the software 
     item architecture, including the technology 
     and product choices for each.
  #. Identification of security domains, security 
     modes (e.g., system high, dedicated), and 
     cross-domain solutions, including the types 
     of data that they must handle.
  #. Detailed descriptions for aspects of the 
     system security design that require a high 
     level of security assurance (e.g., key 
     management design supporting National 
     Security Agency Type 1 encryption).
  #. Detailed descriptions for aspects of the 
     software item architectural design that 
     help support cyber resilience, that is, 
     the ability of a system to operate in the 
     face of persistent cyber attacks and still 
     support mission success (e.g., redundancy 
     of components, request throttling, 
     virtualization or partitioning of resources, 
     deployment of security application tools).

* Description of how and where the software item 
  architecture implements the supportability of 
  the system, that is, the repair, scheduled 
  maintenance, and preventive maintenance required 
  to retain the system in, or restore the system 
  to, a state in which it can perform its required 
  functions, including the ability of personnel to
  install, configure, and monitor computer products,
  identify exceptions or faults, debug or isolate 
  faults to root-cause analysis, and provide hardware 
  or software maintenance in pursuit of solving a 
  problem and restoring the product into service.
* Description of how and where the software item 
  architecture supports system reliability, 
  maintainability, and availability (RMA), and 
  safety, including the software item architectural 
  decisions made to support RMA and safety, the fault 
  management architecture, use of other architectural 
  features to address RMA and safety (e.g., redundancy, 
  automated failover, fault tolerance), and uniform 
  exception handling and recovery methods.
* If applicable, a description of how and where 
  the software item architecture supports the human 
  systems interface to account for human capabilities 
  and limitations in the operations, maintenance, 
  and support of the system. This description shall 
  include software item architecture decisions 
  concerning user interface screen design and user 
  interaction mechanisms for user input and output. 
  This description shall include, if applicable:

  #. How the software item architecture isolates the
     user interface from the application logic.
  #. Principal software item design decisions made 
     to ensure usability by the human operator.
  #. Principal software item design decisions made 
     to ensure that the user interface of the software 
     item is internally consistent across the software 
     item architecture.
  #. Principal software item design decisions made 
     to ensure that the user interface of the software
     item is consistent with widely used application 
     user interfaces.
  #. Principal software item design decisions made 
     to ensure the quantity and frequency of data 
     presented to the operator, including alarms, 
     warnings, and error messages, is able to be 
     assimilated and responded to by the operator 
     within the needed response time.
  #. Applicable human systems interface standards 
     (e.g., graphical user interface (GUI) standards)
     and how those standards are used within the 
     software item architecture.

* Description of how the software item architecture
  supports the selected software development 
  lifecycle model(s) and the integration of 
  software and hardware in each software build 
  and system increment.
* Discussion of other principal and software item 
  architecture-wide design decisions that are not 
  covered by the above items. Examples include the 
  following:

  #. Applicable standards (e.g., interface 
     standards, open system standards) and how 
     those standards are used within the software 
     item architecture.
  #. Application program interfaces (APIs) to be 
     used within the software item.
  #. Algorithms to be used within the software
     item.
  #. Communications mechanisms (e.g., publish and 
     subscribe message passing, calling sequences, 
     shared memory, sockets) to be used between 
     software entities within the software item 
     and under which circumstances each mechanism 
     is to be used.
  #. Definitions of uniform data storage and access 
     methods within the software item.
  #. Requirements traceability. This paragraph 
     shall provide bidirectional traceability:

     * Between the software item architecture 
       components and the software item requirements
       and software item interface requirements.
     * Between the use cases, or equivalent,
       and the software item requirements and
       software item interface requirements.


7. Notes
--------

This section shall contain any general information
that aids in understanding this document (e.g., 
background information, glossary, rationale). This
section shall be divided into the following
paragraphs.


7.1 Abbreviations and acronyms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall include an alphabetical
listing of all acronyms, abbreviations, and their
meanings as used in this document.


7.2 Glossary
^^^^^^^^^^^^

This paragraph shall include a list of any terms
and their definitions needed to understand this
document. Terms often used differently between
organizations (e.g., acquisition phase names,
build, block, development phase names, effectivity,
evolution, increment, and iteration) shall be
defined to avoid confusion. If the terms used
are exactly as defined in the Software Development
Standard (SDSMCS), they need not be redefined
here.


7.3 General information
^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall contain any other general
information that aids in understanding this
document (e.g., background information, rationale).


A. Appendices
-------------

Appendices may be used to provide information
published separately for convenience in document
maintenance (e.g., charts, classified data). As
applicable, each appendix shall be referenced in
the main body of the document where the data would
normally have been provided. Appendices may be
bound as separate documents for ease in handling.
Appendices shall be lettered alphabetically
(Appendix A, Appendix B, etc.).