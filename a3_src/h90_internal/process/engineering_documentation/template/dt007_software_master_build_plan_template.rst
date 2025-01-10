===================================
Software master build plan template
===================================

This appendix is a MANDATORY part of the (SDSMCS).
It provides the content requirements for the SMBP.

1. If the section numbering used below is not used,
   the developer shall provide an appendix in the
   SMBP with a traceability matrix mapping from the
   section numbers and titles below to the section
   numbers and titles used in the developer SMBP.
2. If there is such a traceability mapping appendix,
   it shall be referenced in section 1.3.


Purpose
^^^^^^^

The Software Master Build Plan (SMBP) includes
plans for integrating and verifying the software
consistent with the software development lifecycle
model(s). (The SMBP is sometimes known as the
Master Software Integration and Verification
Plan.)


References
^^^^^^^^^^

SDSMCS
  Adams, R. J., S. Eslinger, K. L. Owens, 
  J. M. Tagami, and M. A. Zambrana, Software
  Development Standard for Mission Critical
  Systems (SDSMCS), Aerospace Report No.
  TR-RS-2015-00012, March 17, 2014, The Aerospace
  Corporation. This is the same as SMC Standard
  SMC-S-012, Software Development Standard.


Content requirements
^^^^^^^^^^^^^^^^^^^^

This template contains the required content of
the SMBP. The content and level of detail of the
SMBP is expected to evolve as more information
is available and captured. See Section 3 of the
Software Development Standard for Mission-Critical
Systems (SDSMCS) for definitions of all italicized
words or phrases.


1. Scope
--------

This section SHALL be divided into the following
paragraphs.


1.1 Identification
^^^^^^^^^^^^^^^^^^

* This paragraph SHALL contain a full
  identification of the system and the software
  to which this document applies, including, as
  applicable, identification number(s), title(s),
  abbreviation(s), version number(s), and release
  number(s).

1.2 System overview
^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL briefly state the purpose
  of the system and the software to which this
  document applies.
* This paragraph SHALL: 

  #. Describe the general nature of the system and
     software.
  #. Summarize the history of system development,
     operation, and maintenance.
  #. Identify the project sponsor, acquirer, user,
     developer, and support organizations.
  #. Identify current and planned operating and
     user sites.


1.3 Document overview
^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL summarize the purpose and
  contents of this document.
* This paragraph SHALL describe any security or
  privacy considerations associated with its use.


1.4 Relationship to other documents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL describe the relationship,
  if any, of the SMBP to the SDP and other project
  management plans and project documents.


2. Referenced documents
-----------------------

* This section SHALL list the number, title,
  revision, and date of all documents referenced
  in this plan.
* This section SHALL also identify the source for
  all documents not available through normal
  Government stocking activities.


3. Software master build plan
-----------------------------

* This section SHALL provide the philosophy and
  rationale for the decisions about the contents
  and progression of the builds.
* This section SHALL provide multiple perspectives
  of the builds, including descriptions of which
  requirements are in which builds, which software
  units and software items are integrated in which
  builds, and the integration levels and
  qualification testing levels of the various
  builds.
* Build content descriptions SHALL include newly
  developed software, reusable software, and the
  software used for verification.
* This paragraph SHALL be divided into the 
  following subparagraphs. The paragraphs
  containing “.x” in their numbers and
  “x” in their names shall be repeated for each
  build “x.”


3.1 Planned builds
^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the philosophy and
  rationale for determining the builds, based
  upon, e.g., required capability need dates by
  the acquirer, a regular integration schedule
  (e.g., quarterly or monthly), an achievable
  build development size determined by number of
  requirements, number of lines of source code,
  size of executable software, or some other
  factor.
* This paragraph SHALL provide the names of the
  planned builds. 
* This paragraph SHALL provide the names of the
  planned builds in relationship to internal
  milestone reviews, e.g., build reviews and major
  reviews, e.g., SAR, PDR, CDR, Test Readiness
  Reviews (TRRs).
* This paragraph SHALL provide the driving
  objectives of each build.


3.2 Build requirements contents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the philosophy and
  rationale for determining which requirements go
  into which builds.
* This paragraph SHALL summarize the set of
  software requirements that will be included in
  each build.
* The SMBP MAY include requirements at higher
  levels than software, e.g., element, segment,
  subsystem, and system requirements.


3.2.x Build x <Insert Name> requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the list of
  software requirements that will be included
  in build “x.”
* For each requirement, the requirement identifier,
  a short requirement description, the requirements
  text, and the verification event, as a minimum,
  SHALL be included.
* For each requirement, this paragraph SHALL
  indicate if the requirement will only be
  partially implemented in build “x.”

Note 1: A table can provide this information.
Note 2: This information may be placed in an
        appendix referenced from this section.
Note 3: If a software item is developed in multiple
        builds, its requirements might not be fully
        implemented and verified until the final
        build. The planning identifies the subset
        of each software item’s requirements to be
        implemented in each build.


3.3 Build integration levels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the philosophy and
  rationale for determining which builds are
  promoted to a higher level of integration.
* This paragraph SHALL provide the hierarchy of
  integration and integration testing.
* This paragraph SHALL specify responsibilities
  for each integration level in the integration
  hierarchy.
* This paragraph SHALL summarize which levels of
  integration will occur for each build.
* This paragraph SHALL summarize which levels
  of integration testing will occur for each
  build.
* This paragraph MAY make use of a table to provide
  this information.
* This paragraph SHOULD list the hardware on which
  the software executes, whether it is COTS
  hardware or special hardware being developed.


3.3.x Build x <Insert Name> integration levels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the list of
  integration level(s) that will be performed
  for build “x.” For example, the build will
  integrate software units or software items:

  #. Into part of a software item
  #. Into a whole software item
  #. Into multiple software items
  #. With the hardware items on which they execute
  #. Into the subsystem level
  #. Into the system level
  #. Any combination of the integration levels

* This paragraph MAY make use of a table to provide
  this information.


3.4 Build contents and integration order
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the philosophy 
  and rationale for determining which units are
  integrated in which order.
* This paragraph SHALL specify the location of
  each integration activity.
* This paragraph SHALL summarize the software
  items and software units, including reusable
  software, that are allocated to each build.


3.4.x. Build x <Insert Name> contents and integration order
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For build “x,” this paragraph shall provide the
subparagraphs below.


3.4.x.1 Build x <Insert Name> contents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the set of software
  items and software units that will be included
  in build “x.”
* This paragraph MAY make use of a table to provide
  this information.
* This information MAY be placed in an appendix
  that is referenced from this paragraph.


3.4.x.2 Build x <Insert Name> integration order
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the intended order
  of integrating the units for build “x.”
* This paragraph MAY make use of a table to 
  provide this information.
* This information MAY be placed in an appendix
  that is referenced from this paragraph.


3.5 Build qualification testing levels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the philosophy
  and rationale for determining which builds 
  will undergo which levels of qualification
  testing.
* This paragraph SHALL specify responsibilities
  for each qualification test level.
* This paragraph SHALL specify the location
  of each qualification test event.
* This paragraph SHALL summarize the qualification
  testing level(s) for each build.


3.5.x Build x <Insert Name> qualification testing levels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the list of
  qualification testing levels that will be
  performed for build “x”. For example, the
  build will be qualification tested at the
  following level(s), if any:

  * Software item 
  * Software level (e.g. some or all s/w items)
  * Element level
  * Segment level
  * Subsystem level
  * System level

  Note: A table can provide this information.

* This paragraph SHALL provide the allocation of
  requirements to specific qualification testing
  events.
* This paragraph SHALL specify responsibilities
  for each qualification testing event.
* This paragraph SHALL specify the location of
  each qualification testing event for build “x.”


3.6 Build deliveries
^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL provide the philosophy and
  rationale for determining:

  #. Which builds will be delivered to a higher
     level for internal integration and testing.
  #. Which builds will be delivered to a higher
     level for internal qualification testing.
  #. Which builds will be delivered to the
     acquirer for integrated operational test
     and evaluation. 
  #. Which builds will be delivered to the
     acquirer for operations.

* This paragraph SHALL summarize which builds will
  be delivered for internal integration and test.
* This paragraph SHALL summarize which builds will
  be delivered for higher levels of internal
  integration, integration testing, and qualification
  testing.
* This paragraph SHALL summarize which builds will
  be delivered to the acquirer for integrated
  operational test and evaluation.
* This paragraph SHALL summarize which builds will
  be delivered to the acquirer for operations.


3.7 Build schedule
^^^^^^^^^^^^^^^^^^

* This paragraph SHALL summarize when each build
  will be started and completed.
* This paragraph SHALL summarize when each build
  will be delivered for each level of integration.
* This paragraph SHALL summarize when each build
  will be delivered for each level of qualification
  testing.
* This paragraph SHALL summarize when each build
  will be delivered to the acquirer for integrated
  operational test and operations.
* This paragraph SHALL summarize when each build
  will be delivered to the acquirer for operations.


4. Notes
--------

* This section SHALL contain any general information
  that aids in understanding this document (e.g., 
  background information, glossary, rationale).
* This section SHALL be divided into the following
  paragraphs.


4.1 Abbreviations and acronyms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL include an alphabetical
  listing of all acronyms, abbreviations, and
  their meanings as used in this document.


4.2 Glossary
^^^^^^^^^^^^

* This paragraph SHALL include a list of any terms
  and their definitions needed to understand this
  document.
* Terms often used differently between organizations
  (e.g., acquisition phase names, build, block,
  development phase names, effectivity, evolution,
  increment, and iteration) SHALL be defined to
  avoid confusion.
* If the terms used are exactly as defined in the
  Software Development Standard (SDSMCS), they 
  MAY be omitted and need not be redefined here.


4.3 General information
^^^^^^^^^^^^^^^^^^^^^^^

* This paragraph SHALL contain any other general
  information that aids in understanding this
  document (e.g., background information,
  rationale).


A. Appendices
-------------

* Appendices MAY be used to provide information 
  published separately for convenience in document
  maintenance (e.g., charts, classified data).
* As applicable, each appendix SHALL be referenced
  in the main body of the document where the data
  would normally have been provided.
* Appendices MAY be bound as separate documents
  for ease in handling.
* Appendices SHALL be lettered alphabetically
  (Appendix A, B, etc.).
