==================================
Software development plan template
==================================

Template overview
-----------------

This template defines the required structure and 
content for creating a Software Development Plan
(SDP). It is designed to:

1. Guide the systematic documentation of 
   software development plans.
2. Ensure comprehensive coverage of all critical
   aspects.
3. Maintain consistency across different
   projects.
4. Enable automated processing and validation.

Key Template Usage Rules:

1. All referenced information from sections 4, 
   5, 6, and 7 must be included as attachments.
2. If using different section numbers, provide a
   mapping matrix in an appendix.
3. Reference any mapping matrix in section 1.3.
4. Follow the exact structure and numbering
   unless explicitly mapping differences.

Note:
    The section numbering aligns with the
    Software Development Standard for Mission
    Critical Systems (SDSMCS).


Purpose
^^^^^^^

The Software Development Plan (SDP) is a
comprehensive document that:

1. Details the complete software development
   approach.
2. Covers all development activities:

   * New development
   * Modifications
   * Reuse of existing code
   * System reengineering
   * COTS integration
   * Maintenance
   * Any other software-related activities

3. Provides stakeholders with:

   * Clear development process documentation
   * Defined methodologies
   * Activity-specific approaches
   * Project scheduling
   * Resource allocation
   * Organizational structure


References
^^^^^^^^^^

* (CMMI) Software Engineering Institute,
  Capability Maturity Model Integration, Version
  1.3, CMMI for Development, Report No.
  CMU/SEI-2010-TR-033, November 2010, Software
  Engineering Institute, Carnegie Mellon
  University. Capability Maturity Model ® and
  CMMI ® are registered in the U. S. Patent and
  Trademark Office by Carnegie Mellon University.
* (SMS) Abelson, L. A., S. Eslinger, M. C.
  Gechman, C. H. Ledoux, M. V. Lieu, K. Korzac,
  Software Measurement Standard for Mission
  Critical Systems, Aerospace Report No.
  TOR-2009(8506)-6, 5 May, 2011, The Aerospace
  Corporation.
* (SDSMCS) Adams, R. J., S. Eslinger, K. L.
  Owens, J. M. Tagami, and M. A. Zambrana,
  Software Development Standard for Mission
  Critical Systems (SDSMCS), Aerospace Report
  No. TR-RS-2015-00012, March 17, 2014, The
  Aerospace Corporation. This is the same as SMC
  Standard SMC-S-012, Software Development
  Standard.


Content requirements
^^^^^^^^^^^^^^^^^^^^

Each section in this template:

1. Contains specific required information
2. Must be completed in full
3. Should maintain consistent formatting
4. Must use clear, unambiguous language
5. Should enable automated validation


1. Scope
--------

This section shall be divided into the following
paragraphs.


1.1 Identification
^^^^^^^^^^^^^^^^^^

This paragraph shall contain a full 
identification of the system and the software to
which this document applies, including, as
applicable, identification number(s), title(s),
abbreviation(s), version number(s), and release
number(s).


1.2 System overview
^^^^^^^^^^^^^^^^^^^

This paragraph shall briefly state the purpose
of the system and the software to which this
document applies. It shall: 

1. Describe the general nature of the system and
   software.
2. Summarize the history of system development,
   operation, and maintenance.
3. Identify the project sponsor, acquirer, user,
   developer, and support organizations.
4. Identify current and planned operating and
   user sites.


1.3 Document overview
^^^^^^^^^^^^^^^^^^^^^

This paragraph shall summarize the purpose and 
contents of this document. This paragraph shall
describe any security or privacy considerations
associated with its use.


1.4 Relationship to other plans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe the relationship,
if any, of the SDP to other project management
plans.


2. Referenced documents
-----------------------

This section shall list the number, title,
revision,  and date of all documents referenced
in this plan. This section shall also identify
the source for all documents not available
through normal Government stocking activities.


3. Overview of required work
----------------------------

This section shall be divided into paragraphs as 
needed to establish the context for the planning
described in later sections. It shall include,
as applicable, an overview of:

1. Requirements and constraints on the system
   and software to be developed.
2. Requirements and constraints on project 
   documentation.
3. Position of the project in the system
   lifecycle.
4. The selected project and acquisition strategy
5. Any requirements or constraints on the
   selected project and acquisition strategy.
6. Requirements and constraints on project
   schedules and resources.
7. Other requirements and constraints, such as
   on project security, privacy, methods,
   standards, interdependencies on hardware and
   software development.


4. General requirements
-----------------------

This section defines the core requirements and 
processes for software development.

Key Section Guidelines:

1. Mark non-applicable activities with 
   "Not applicable".
2. Document build-specific differences
   explicitly.
2. Document software-item-specific differences
   explicitly.
3. Include risk analysis for each component
4. Follow SDSMCS Section 4 requirements

For each subsection below:

1. Identify specific risks and mitigation plans
2. Document assumptions and constraints
3. Specify success criteria
4. Define validation methods


4.1 Software development process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Define the complete software development
approach including:

1. Development lifecycle:

   * Selected lifecycle model(s)
   * Rationale for selection
   * Key lifecycle phases
   * Phase transitions

2. Build strategy:

   * Build identification
   * Build objectives
   * Build contents
   * Build schedule

3. Development activities:

   * Activities per build
   * Entry/exit criteria
   * Quality gates
   * Review points


4.2 General requirements for software development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section defines the core requirements and
processes for software development, ensuring
that: 

* Systematic and documented methods have been
  used for all software development activities.
* Methods are specified and documented in the
  SDP.


4.2.1 Software development methods
""""""""""""""""""""""""""""""""""

Specify the software development methods to be
used:

1. Overall approach and methodology:

   * Quality strategies
   * Design philosophies
   * Development activity model(s)
   * Development lifecycle model(s)
   * Applicable standards documents
   * Best practices guides

2. Tool selection:

   * Requirements analysis tools
   * Documentation tools
   * Design automation tools
   * Static analysis, linting tools
   * Test automation tools

3. Specific methods, procedures and protocols:

   * Methods documents
   * Procedures documents
   * Checklists
   * Tool configuration and usage protocols

It is acceptable to reference other paragraphs
in this plan if the methods are better described
in context with the activities to which they
will be applied.


4.2.2 Standards for products
""""""""""""""""""""""""""""

List references to standards for all development
artifacts:

1. Documentation standards:

   * Requirements documentation standards
   * Architecture documentation standards
   * Design decision documentation standards
   * Test documentation standards

2. Design (coding) standards:

   * Language style guides
   * Inline documentation standards
   * Peer review criteria
   * Quality metrics

3. Test standards:

   * Test cases
   * Test procedures
   * Test results

4. Change management:

   * Change reports
   * Discrepancy reports
   * Status tracking
   * Resolution process

A copy of the standards documents shall be
placed in appendices, and this paragraph shall
contain a list of references to those
appendices. The standards listed shall cover all
contractual requirements concerning standards
for products.

4.2.2.1 Standards for code
""""""""""""""""""""""""""

Standards for code shall be provided for each
programming language to be used. The coding
standards for each language shall include, as a
minimum:

#. Standards for format (such as indentation, 
   spacing, capitalization, and order of
   information).
#. Standards for header comments, requiring, for 
   example, name and identifier of the code; 
   version identification; modification history;
   purpose; requirements and design decisions
   implemented; notes on the processing (such as
   algorithms used, assumptions, constraints,
   limitations, and side effects); and notes on
   the data (e.g., inputs, outputs, variables,
   data structures).
#. Standards for other comments, such as required
   number and content expectations).
#. Naming conventions (e.g., for constants, types,
   variables, parameters, packages, procedures,
   classes, objects, methods, functions, files).
#. Restrictions, if any, on the use of programming
   language constructs or features.
#. Restrictions, if any, on the complexity of code
   aggregates.


For each programming language, specify:

1. Formatting Requirements:
   - Indentation rules
   - Spacing conventions
   - Capitalization rules
   - Code organization

2. Documentation Requirements:
   - Header format
   - Required fields
   - Content expectations
   - Update procedures

3. Naming Conventions:
   - Variables
   - Functions
   - Classes
   - Files
   - Packages

4. Code Organization:
   - File structure
   - Module organization
   - Import ordering
   - Section ordering

5. Language Usage:
   - Approved features
   - Restricted features
   - Required patterns
   - Forbidden patterns

6. Complexity Limits:
   - Function size
   - Class size
   - Nesting depth
   - Cyclomatic complexity


4.2.2.2 Standards for DCRs
""""""""""""""""""""""""""

Standards for discrepancy and change reports
(DCRs) shall be provided. The DCR standards shall
include, as a minimum:

#. A glossary and definitions of terms that can be 
   used in discrepancy and change reports (DCRs),
   including all specialized terms used in DCR
   titles, descriptions, causes, and resolutions.
#. Alternative and additional definitions, if any,
   for DCR terms specified in Appendix C.2.1 of
   this standard.
#. A DCR acronym list that includes all acronyms
   that are used (or are permitted to be used) in
   DCRs. These acronyms might appear in (e.g., DCR
   titles, free text descriptions of test
   incidents, discrepancies, failures, causes,
   resolutions, and development, integration and
   qualification test activity names); Note: This
   DCR acronym list is in addition to the acronym
   list for the entire SDP.
#. A list of activity names and their definitions
   used for DCRs besides those in Appendix C,
   Table C.2-2, of the standard.
#. The names and sequence of the DCR steps that
   can be used.


Define comprehensive DCR standards including:

1. Terminology:
   - Standard terms
   - Definitions
   - Usage guidelines
   - Context rules

2. Required Content:
   - Title format
   - Description format
   - Cause analysis
   - Resolution steps

3. Supporting Information:
   - Acronym list
   - Activity names
   - Process steps
   - Status codes

4. Process Requirements:
   - Submission process
   - Review process
   - Approval process
   - Implementation process

5. Documentation:
   - Required fields
   - Optional fields
   - Attachments
   - References

4.2.2.3 Standards for test logs
"""""""""""""""""""""""""""""""

Standards for test logs shall be provided. The
test log standards shall include, as a minimum:

#. The test log fields and terms specified in
   Appendix F.2 of (SDSMCS).
#. Alternative and additional definitions, if any,
   for test log terms specified in Appendix F.2.1
   of (SDSMCS).

Specify test log requirements including:

1. Required Fields:
   - Test identification
   - Environment details
   - Execution steps
   - Results recording

2. Content Standards:
   - Field definitions
   - Format requirements
   - Value constraints
   - Relationships

3. Process Requirements:
   - Creation timing
   - Update procedures
   - Review process
   - Storage requirements

4. Additional Elements:
   - Custom fields
   - Extended definitions
   - Special cases
   - Exceptions


4.2.3 Traceability
""""""""""""""""""

This paragraph shall describe the approach to be
followed for establishing and maintaining
bidirectional traceability between levels of
requirements, between requirements and design,
between design and the software that implements
it, between requirements and qualification test 
information, and between computer hardware
resource utilization requirements and measured
computer hardware resource utilization. See
Section 4.2.3 in the body of (SDSMCS) for the
activities, topics, and other items to be
addressed in this paragraph on bidirectional
traceability.


4.2.4 Reusable software products
""""""""""""""""""""""""""""""""

See Section 4.2.4 in the body of (SDSMCS) for the
activities and topics to be addressed in this
paragraph on reusable software products. This
paragraph shall be divided into the following
subparagraphs.


4.2.4.1 Incorporating reusable software products
""""""""""""""""""""""""""""""""""""""""""""""""

This paragraph shall describe the approach to be
followed for identifying, evaluating, and
incorporating reusable software products,
including the scope of the search for such
products and the criteria to be used for their
evaluation. Candidate or selected reusable
software products known at the time this plan
is prepared or updated shall be identified and
described, together with benefits, drawbacks,
alternatives considered, rationale for those
selected, remaining viable alternatives, and
restrictions, as applicable, associated with
their use.


4.2.4.2 Developing reusable software products
"""""""""""""""""""""""""""""""""""""""""""""

This paragraph shall describe the approach to be
followed for identifying, evaluating, and reporting
opportunities for developing reusable software
products.


4.2.5 Assurance of critical requirements
""""""""""""""""""""""""""""""""""""""""

See Section 4.2.5 in the body of (SDSMCS) for the
activities and topics to be addressed in this
paragraph on assurance of critical requirements.
This paragraph shall be divided into the following
subparagraphs to describe the approach to be
followed for handling requirements designated
critical.


4.2.5.1 Safety
""""""""""""""

This paragraph shall describe the assurance 
approach to be followed for handling safety
requirements.


4.2.5.2 Security
""""""""""""""""

This paragraph shall describe the assurance
approach to be followed for handling security
requirements.


4.2.5.3 Privacy protection
""""""""""""""""""""""""""

This paragraph shall describe the assurance
approach to be followed for handling privacy
protection requirements.


4.2.5.4 Reliability, maintainability, and availability
""""""""""""""""""""""""""""""""""""""""""""""""""""""

This paragraph shall describe the assurance
approach to be followed for handling reliability,
maintainability, and availability requirements.


4.2.5.5 Dependability
"""""""""""""""""""""

This paragraph shall describe the assurance
approach to be followed for handling dependability
requirements.


4.2.5.6 Human system integration, including human factors engineering
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This paragraph shall describe the assurance
approach to be followed for handling human
system integration requirements, including
human factors engineering concerns.


4.2.5.7 Assurance of other mission-critical requirements as agreed to by the acquirer and developer
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This paragraph shall describe the assurance
approach to be followed for handling other
mission critical requirements as may be
agreed upon by the acquirer and developer.


4.2.6 Computer hardware resource utilization
""""""""""""""""""""""""""""""""""""""""""""

This paragraph shall describe the approach to be 
followed for allocating computer hardware
resources and monitoring their utilization. See
Section 4.2.6 in the body of (SDSMCS) for the
activities and topics to be addressed in this
paragraph on computer hardware resource
utilization.


4.2.7 Recording rationale
"""""""""""""""""""""""""

This paragraph shall describe the approach to be
followed for recording rationale that will be
useful to the support organization for key
decisions made on the project. It shall interpret 
the term “key decisions” for the project. It shall
state where the rationale are to be recorded. See
Section 4.2.7 in the body of (SDSMCS) for the
activities and topics to be addressed in this
paragraph on recording rationale.


4.2.8 Access for acquirer review
""""""""""""""""""""""""""""""""

This paragraph shall describe the approach to be
followed for providing the acquirer and its
authorized representatives access to developer and
software team member facilities for review of 
products and activities. It shall cover all
contractual requirements concerning acquirer team 
access for review. See Section 4.2.8 in the body 
of (SDSMCS) for the activities and topics to be 
addressed in this paragraph on access for acquirer
review.


4.2.9 Contractual requirements
""""""""""""""""""""""""""""""

This paragraph shall describe the approach to be
followed for meeting all the contractual
requirements regarding software development,
including testing, transition, maintenance, and
operations. Reference may be made to other
paragraphs in this plan if the approach to be
followed for meeting contractual requirements is
better described in context with the activities
to which they will be applied. These contractual
requirements can be found in, e.g., the Statement 
of Work (SOW), Contract Data Requirements List 
(CDRL), compliance documents and their tailoring, 
Integrated Master Plan (IMP), specifications, 
Section H of the Model Contract (Sections A-K of 
the RFP and Contract), and other contractual 
documentation.


5. Plans for performing detailed software development activities
----------------------------------------------------------------

The paragraphs below cover the plans for 
performing detailed software development 
activities. Provisions corresponding to 
nonrequired activities may be satisfied by the 
words “Not applicable.” If different builds or 
different software on the project require
different planning, these differences shall be 
noted in the paragraphs. If different planning is 
required for new development, modification, 
reusable software products, reengineering, and 
maintenance, these differences shall be described 
in the paragraphs. The discussion of each activity 
shall include the approach, i.e., plans, 
processes, methods, procedures, tools, roles, and
responsibilities, to be applied to:

#. The analysis or other technical tasks involved
#. The recording of results
#. The preparation of associated deliverables, if 
   applicable.

For each activity, include:

#. Entrance criteria
#. Inputs 
#. Tasks to be accomplished 
#. Products to be produced 
#. Verifications to be used to ensure tasks are
   performed according to their defined processes
   and products meet their requirements
#. Outputs
#. Exit criteria.

The discussion shall also identify applicable
risks and uncertainties and plans for dealing with
them. Reference may be made to paragraph 4.2.1 if 
applicable methods are described there. This 
section shall be divided into the following
paragraphs.


This section provides detailed plans for software development activities.
Each activity description must follow this structure:

Activity Documentation Framework:
1. Purpose and Scope
2. Entry Criteria
3. Input Requirements
4. Required Tasks
5. Output Products
6. Verification Methods
7. Exit Criteria
8. Risk Assessment

For each activity:
1. Document variations by:
   - Build type
   - Software category
   - Development phase
   - Maintenance needs

2. Include for each task:
   - Analysis methods
   - Result recording
   - Deliverable preparation

3. Address:
   - Technical procedures
   - Documentation needs
   - Quality assurance
   - Risk management

5.1 Project planning and oversight
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.1 and its subparagraphs in the body 
of the Software Development Standard for Mission
Critical Systems (SDSMCS) for the activities and 
topics to be addressed in this paragraph on 
project planning and oversight. This paragraph 
shall be divided into the following subparagraphs 
to describe the approach to be followed for 
project planning and oversight.

Define comprehensive project management approach:

1. Planning Activities:
   - Initial planning
   - Ongoing updates
   - Risk management
   - Resource allocation

2. Oversight Methods:
   - Progress tracking
   - Performance metrics
   - Quality indicators
   - Risk monitoring

3. Control Mechanisms:
   - Change management
   - Issue resolution
   - Decision making
   - Escalation paths

5.1.1 Software development planning
"""""""""""""""""""""""""""""""""""

Detail the development planning process:

1. Plan Components:
   - Schedule development
   - Resource allocation
   - Risk assessment
   - Quality targets

2. Planning Process:
   - Input gathering
   - Stakeholder review
   - Approval workflow
   - Update procedures

3. Integration Points:
   - Cross-team coordination
   - Dependency management
   - Interface planning
   - Resource sharing


5.1.2 Software integration and test planning
""""""""""""""""""""""""""""""""""""""""""""

Define integration and test strategy:

1. Integration Approach:
   - Component identification
   - Integration sequence
   - Interface verification
   - System assembly

2. Test Strategy:
   - Test levels
   - Test types
   - Coverage requirements
   - Success criteria

3. Resource Planning:
   - Environment needs
   - Tool requirements
   - Personnel allocation
   - Schedule constraints


5.1.2.1 Software integration planning
"""""""""""""""""""""""""""""""""""""

Detail the integration planning process:

1. Integration Levels:
   - Unit integration
   - Component integration
   - System integration
   - External interfaces

2. Integration Methods:
   - Bottom-up approach
   - Top-down approach
   - Hybrid strategies
   - Risk mitigation

3. Verification Points:
   - Interface checks
   - Functionality tests
   - Performance validation
   - Security verification


5.1.2.2 Software item qualification test planning
"""""""""""""""""""""""""""""""""""""""""""""""""

Define qualification test approach:

1. Test Scope:
   - Functionality coverage
   - Performance requirements
   - Interface validation
   - Security assessment

2. Test Methods:
   - Test case development
   - Test procedure creation
   - Test data management
   - Results analysis

3. Quality Criteria:
   - Pass/fail criteria
   - Performance thresholds
   - Acceptance standards
   - Documentation requirements


5.1.3 System qualification test planning
""""""""""""""""""""""""""""""""""""""""

Specify system-level test planning:

1. Test Coverage:
   - System requirements
   - Performance goals
   - Integration points
   - User scenarios

2. Test Environment:
   - Hardware needs
   - Software configuration
   - Data requirements
   - Tool support

3. Test Execution:
   - Sequence definition
   - Resource allocation
   - Schedule planning
   - Risk management

5.1.4 Planning for software transition to operations
""""""""""""""""""""""""""""""""""""""""""""""""""""

Define operational transition strategy:

1. Transition Requirements:
   - Operational readiness
   - User preparation
   - System cutover
   - Support handover

2. Documentation Needs:
   - User manuals
   - Operation guides
   - Training materials
   - Support procedures

3. Validation Process:
   - Acceptance criteria
   - Performance validation
   - Security verification
   - Operational testing


5.1.5 Planning for software transition to maintenance
"""""""""""""""""""""""""""""""""""""""""""""""""""""


5.1.6 Following and updating plans
""""""""""""""""""""""""""""""""""


5.2 Establishing a software development environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The developer shall record the results of the
software engineering environment adequacy analysis
in the SDP. The developer shall record the results
of the software integration and qualification test
environment adequacy analysis in the SDP. See
Section 5.2 and its subparagraphs in the body of
(SDSMCS) for the activities and topics to be
addressed in this paragraph on establishing and
maintaining software development environments.
This paragraph shall be divided into the following
subparagraphs to describe the approach to be
followed for establishing, controlling, and
maintaining a software development environment.

Define the complete development environment including:

1. Environment Components:
   - Development tools
   - Testing frameworks
   - Build systems
   - Version control
   - Issue tracking
   - Documentation tools
   - Collaboration platforms

2. Environment Management:
   - Setup procedures
   - Maintenance processes
   - Access control
   - Backup strategies
   - Recovery procedures

3. Environment Analysis:
   - Capability assessment
   - Performance monitoring
   - Security evaluation
   - Compliance verification


5.2.1 Software engineering environment
""""""""""""""""""""""""""""""""""""""

Detail the engineering environment setup:

1. Development Tools:
   - IDEs and editors
   - Compilers/interpreters
   - Debugging tools
   - Code analysis tools
   - Documentation generators

2. Support Systems:
   - Version control
   - Build automation
   - Continuous integration
   - Code review platforms

3. Quality Tools:
   - Static analyzers
   - Test frameworks
   - Coverage tools
   - Performance profilers


5.2.1.1 Software engineering environment description
""""""""""""""""""""""""""""""""""""""""""""""""""""

Provide detailed environment specifications:

1. Hardware Requirements:
   - Processor specifications
   - Memory requirements
   - Storage needs
   - Network capabilities

2. Software Components:
   - Operating systems
   - Development tools
   - Support utilities
   - Third-party tools

3. Configuration Details:
   - Tool versions
   - Integration points
   - Security settings
   - Network topology


5.2.1.2 Software engineering environment adequacy analysis reports
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Document environment analysis results:

1. Capability Assessment:
   - Tool functionality
   - Performance metrics
   - Scalability analysis
   - Integration effectiveness

2. Gap Analysis:
   - Missing capabilities
   - Performance bottlenecks
   - Security vulnerabilities
   - Compliance issues

3. Improvement Plans:
   - Tool upgrades
   - Process enhancements
   - Security hardening
   - Performance optimization


5.2.2 Software integration and qualification test environment
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Define test environment requirements:

1. Test Infrastructure:
   - Hardware platforms
   - Network configuration
   - Storage systems
   - External interfaces

2. Test Tools:
   - Test frameworks
   - Automation tools
   - Monitoring systems
   - Results analysis

3. Environment Control:
   - Configuration management
   - Version control
   - Data management
   - Access control


5.2.2.1 Software integration and qualification test environment description
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Detail test environment specifications:

1. Physical Infrastructure:
   - Hardware components
   - Network architecture
   - Storage systems
   - Security measures

2. Software Components:
   - Test frameworks
   - Automation tools
   - Monitoring systems
   - Support utilities

3. Configuration Management:
   - Version control
   - Change tracking
   - Environment replication
   - Backup procedures

5.2.2.2 Software integration and qualification test environment adequacy analysis reports
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Document test environment analysis:

1. Capability Verification:
   - Feature coverage
   - Performance validation
   - Security assessment
   - Reliability testing

2. Deficiency Analysis:
   - Missing capabilities
   - Performance issues
   - Security gaps
   - Integration problems

3. Enhancement Planning:
   - Capability additions
   - Performance improvements
   - Security updates
   - Process optimization

5.2.3 Software development library
""""""""""""""""""""""""""""""""""

Define library management approach:

1. Library Structure:
   - Component organization
   - Version management
   - Dependency tracking
   - Documentation storage

2. Access Control:
   - User permissions
   - Security policies
   - Audit procedures
   - Change tracking

3. Maintenance Procedures:
   - Update processes
   - Cleanup routines
   - Backup strategies
   - Recovery plans

5.2.4 Software development files
""""""""""""""""""""""""""""""""

Specify file management requirements:

1. File Organization:
   - Directory structure
   - Naming conventions
   - Version control
   - Backup procedures

2. File Types:
   - Source code
   - Documentation
   - Test files
   - Build scripts
   - Configuration files

3. Management Procedures:
   - Access control
   - Change tracking
   - Review processes
   - Archival policies


5.2.5 Nondeliverable software
"""""""""""""""""""""""""""""

Define management of support software:

1. Software Categories:
   - Development tools
   - Test utilities
   - Build scripts
   - Support tools

2. Management Approach:
   - Version control
   - Configuration management
   - License tracking
   - Usage policies

3. Maintenance Strategy:
   - Update procedures
   - Compatibility checks
   - Security updates
   - Support requirements


5.3 System requirements analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.3 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on system requirements
analysis. This paragraph shall be divided into the
following subparagraphs to describe the approach
to be followed for participating in system
requirements analysis.

Define the approach for system requirements analysis:

1. Analysis Framework:
   - Requirements gathering methods
   - Analysis techniques
   - Validation approaches
   - Documentation standards

2. Process Requirements:
   - Entry criteria
   - Input artifacts
   - Required activities
   - Output products
   - Exit criteria

3. Quality Standards:
   - Completeness criteria
   - Consistency checks
   - Traceability rules
   - Validation methods


5.3.1 Analysis of user input
""""""""""""""""""""""""""""

Detail user input analysis approach:

1. Input Sources:
   - User interviews
   - Stakeholder workshops
   - Requirements documents
   - Legacy system analysis

2. Analysis Methods:
   - Input categorization
   - Priority assessment
   - Feasibility analysis
   - Risk evaluation

3. Documentation Requirements:
   - Input recording format
   - Analysis results
   - Validation evidence
   - Traceability links


5.3.2 Operational concept
"""""""""""""""""""""""""

Define operational concept development:

1. Concept Elements:
   - System purpose
   - Operational scenarios
   - User interactions
   - Environmental conditions

2. Documentation Requirements:
   - Scenario descriptions
   - Use case specifications
   - Interface definitions
   - Performance parameters

3. Validation Approach:
   - Stakeholder reviews
   - Prototype demonstrations
   - Simulation results
   - Acceptance criteria


5.3.3 System requirements definition
""""""""""""""""""""""""""""""""""""

Specify requirements definition process:

1. Requirements Categories:
   - Functional requirements
   - Performance requirements
   - Interface requirements
   - Quality attributes
   - Constraints

2. Documentation Standards:
   - Requirement format
   - Unique identifiers
   - Priority levels
   - Verification methods

3. Quality Criteria:
   - Completeness checks
   - Consistency validation
   - Testability assessment
   - Traceability verification


5.4 System architecture and design
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.4 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on requirements for
system architectural design. This paragraph shall
be divided into the following subparagraphs to
describe the approach to be followed for
participating in system architectural design.

Define system architecture development approach:

1. Architecture Framework:
   - Design principles
   - Architecture patterns
   - Quality attributes
   - Design constraints

2. Documentation Requirements:
   - Architecture views
   - Design decisions
   - Trade-off analysis
   - Interface specifications

3. Validation Methods:
   - Architecture reviews
   - Pattern compliance
   - Quality assessment
   - Risk evaluation


5.4.1 System-wide architectural design decisions
""""""""""""""""""""""""""""""""""""""""""""""""

Detail architectural decision process:

1. Decision Framework:
   - Decision criteria
   - Analysis methods
   - Trade-off evaluation
   - Impact assessment

2. Documentation Requirements:
   - Decision rationale
   - Alternatives considered
   - Selection criteria
   - Implementation impact

3. Quality Standards:
   - Consistency checks
   - Pattern compliance
   - Performance impact
   - Maintainability assessment


5.4.2 System architectural design
"""""""""""""""""""""""""""""""""

Specify architectural design approach:

1. Design Elements:
   - Component structure
   - Interface definitions
   - Data architecture
   - Control flow

2. Documentation Standards:
   - Design notation
   - View specifications
   - Interface contracts
   - Quality attributes

3. Validation Methods:
   - Design reviews
   - Pattern compliance
   - Performance analysis
   - Security assessment


5.5 Software requirements analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe the approach to be
followed for software requirements analysis. See
Section 5.5 in the body of (SDSMCS) for the
activities and topics to be addressed in this
paragraph on software requirements analysis.

Define software requirements analysis approach:

1. Analysis Framework:
   - Requirements sources
   - Analysis methods
   - Validation techniques
   - Documentation standards

2. Process Requirements:
   - Entry criteria
   - Input artifacts
   - Required activities
   - Output products
   - Exit criteria

3. Quality Standards:
   - Completeness checks
   - Consistency validation
   - Testability assessment
   - Traceability verification


5.6 Software architecture and design
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.6 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on software
architecture and design. This paragraph shall be
divided into the following subparagraphs to
describe the approach to be followed for software
design.

Detail software architecture development:

1. Architecture Framework:
   - Design principles
   - Architecture patterns
   - Quality attributes
   - Design constraints

2. Documentation Requirements:
   - Architecture views
   - Design decisions
   - Interface specifications
   - Quality scenarios

3. Validation Methods:
   - Architecture reviews
   - Pattern compliance
   - Performance analysis
   - Security assessment


5.6.1 Overall software architecture
"""""""""""""""""""""""""""""""""""

Define overall architecture approach:

1. Architecture Elements:
   - System decomposition
   - Component relationships
   - Quality strategies
   - Evolution approach

2. Documentation Standards:
   - Architecture views
   - Design patterns
   - Quality attributes
   - Constraints

3. Validation Methods:
   - Architecture reviews
   - Pattern compliance
   - Quality assessment
   - Risk evaluation


5.6.2 Software item architecture
""""""""""""""""""""""""""""""""

Specify item architecture approach:

1. Architecture Components:
   - Module structure
   - Interface definitions
   - Data design
   - Control flow

2. Documentation Requirements:
   - Component specifications
   - Interface contracts
   - Quality attributes
   - Design constraints

3. Validation Methods:
   - Design reviews
   - Interface analysis
   - Performance assessment
   - Security validation


5.6.3 Software item detailed design
"""""""""""""""""""""""""""""""""""

Detail design development approach:

1. Design Elements:
   - Module specifications
   - Algorithm design
   - Data structures
   - Interface details

2. Documentation Standards:
   - Design notation
   - Implementation guidelines
   - Quality requirements
   - Constraints

3. Validation Methods:
   - Design reviews
   - Code inspection
   - Performance analysis
   - Security assessment


5.6.3.1 Software unit detailed design
"""""""""""""""""""""""""""""""""""""

Define unit design approach:

1. Design Components:
   - Function specifications
   - Class definitions
   - Data structures
   - Algorithms

2. Documentation Requirements:
   - Design notation
   - Implementation rules
   - Quality attributes
   - Constraints

3. Validation Methods:
   - Code reviews
   - Unit tests
   - Performance checks
   - Security validation


5.6.3.2 Software interface design
"""""""""""""""""""""""""""""""""

Specify interface design approach:

1. Interface Elements:
   - API specifications
   - Protocol definitions
   - Data formats
   - Error handling

2. Documentation Standards:
   - Interface contracts
   - Protocol documentation
   - Error definitions
   - Version control

3. Validation Methods:
   - Interface testing
   - Protocol verification
   - Error handling
   - Performance analysis


5.6.3.3 Database design, as applicable
""""""""""""""""""""""""""""""""""""""

Define database design approach:

1. Design Elements:
   - Data models
   - Schema definitions
   - Relationships
   - Constraints

2. Documentation Requirements:
   - Schema documentation
   - Data dictionary
   - Relationship maps
   - Integrity rules

3. Validation Methods:
   - Schema review
   - Data validation
   - Performance testing
   - Security assessment


5.6.3.4 User interface design, as applicable
""""""""""""""""""""""""""""""""""""""""""""

Detail UI design approach:

1. Design Elements:
   - Layout specifications
   - Interaction patterns
   - Visual design
   - Accessibility features

2. Documentation Standards:
   - Style guides
   - Component library
   - Interaction patterns
   - Accessibility rules

3. Validation Methods:
   - Usability testing
   - Accessibility checks
   - Performance analysis
   - User acceptance


5.6.3.5 Other applicable software design
""""""""""""""""""""""""""""""""""""""""

(e.g., model-based software, as applicable)


5.7 Software implementation and unit testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.7 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on software
implementation and unit testing. This paragraph
shall be divided into the following subparagraphs
to describe the approach to be followed for
software implementation and unit testing.

Define implementation and testing approach:

1. Implementation Framework:
   - Coding standards
   - Development practices
   - Quality metrics
   - Testing requirements

2. Process Requirements:
   - Entry criteria
   - Development workflow
   - Testing procedures
   - Exit criteria

3. Quality Standards:
   - Code reviews
   - Unit tests
   - Performance checks
   - Security validation


5.7.1 Implementing software
"""""""""""""""""""""""""""

Specify implementation approach:

1. Development Standards:
   - Coding guidelines
   - Documentation rules
   - Quality metrics
   - Best practices

2. Process Requirements:
   - Version control
   - Code review
   - Documentation
   - Testing

3. Quality Controls:
   - Static analysis
   - Code coverage
   - Performance metrics
   - Security checks


5.7.2 Preparing for unit testing
""""""""""""""""""""""""""""""""

Detail unit test preparation:

1. Test Framework:
   - Testing tools
   - Test environment
   - Test data
   - Coverage requirements

2. Test Planning:
   - Test cases
   - Test procedures
   - Test data
   - Expected results

3. Quality Standards:
   - Coverage metrics
   - Performance criteria
   - Security requirements
   - Documentation standards


5.7.3 Performing unit testing
"""""""""""""""""""""""""""""

Define unit testing process:

1. Testing Activities:
   - Test execution
   - Result recording
   - Defect tracking
   - Coverage analysis

2. Documentation Requirements:
   - Test results
   - Coverage reports
   - Defect logs
   - Performance data

3. Quality Criteria:
   - Pass/fail criteria
   - Coverage thresholds
   - Performance targets
   - Security standards

5.7.4 Analyzing and recording unit testing results
""""""""""""""""""""""""""""""""""""""""""""""""""

Specify test analysis approach:

1. Analysis Methods:
   - Result verification
   - Coverage assessment
   - Performance analysis
   - Trend analysis

2. Documentation Standards:
   - Result format
   - Analysis reports
   - Metrics collection
   - Trend reporting

3. Quality Requirements:
   - Completeness checks
   - Accuracy validation
   - Trend analysis
   - Action planning


5.7.5 Unit regression testing
"""""""""""""""""""""""""""""

Define regression testing approach:

1. Testing Strategy:
   - Test selection
   - Automation approach
   - Execution frequency
   - Result analysis

2. Process Requirements:
   - Test maintenance
   - Execution triggers
   - Result verification
   - Issue resolution

3. Quality Standards:
   - Coverage requirements
   - Performance criteria
   - Reliability metrics
   - Documentation standards


5.7.6 Revising and retesting units
""""""""""""""""""""""""""""""""""

Detail revision and retest process:

1. Revision Approach:
   - Change assessment
   - Impact analysis
   - Implementation rules
   - Quality checks

2. Retest Requirements:
   - Test selection
   - Execution process
   - Result verification
   - Documentation

3. Quality Criteria:
   - Change validation
   - Test coverage
   - Performance checks
   - Security validation


5.8 Unit integration and testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.8 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on software unit
integration and testing. This paragraph shall be
divided into the following subparagraphs to
describe the approach to be followed for unit
integration and testing.

Define integration testing approach:

1. Integration Framework:
   - Integration strategy
   - Testing methods
   - Quality criteria
   - Documentation standards

2. Process Requirements:
   - Entry criteria
   - Integration steps
   - Testing procedures
   - Exit criteria

3. Quality Standards:
   - Integration checks
   - Interface testing
   - Performance analysis
   - Security validation


5.8.1 Testing on the target computer system
"""""""""""""""""""""""""""""""""""""""""""


5.8.2 Preparing for unit integration and testing
""""""""""""""""""""""""""""""""""""""""""""""""


5.8.3 Performing unit integration and testing
"""""""""""""""""""""""""""""""""""""""""""""


5.8.4 Analyzing and recording unit integration and test results
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.8.5 Unit integration regression testing
"""""""""""""""""""""""""""""""""""""""""


5.8.6 Revising and retesting unit integration
"""""""""""""""""""""""""""""""""""""""""""""


5.9 Software item qualification testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.9 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on software item
qualification testing. This paragraph shall be
divided into the following subparagraphs to
describe the approach to be followed for software
item qualification testing.


5.9.1 Independence in software item qualification testing
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.9.2 Testing on the target computer system
"""""""""""""""""""""""""""""""""""""""""""


5.9.3 Preparing for software item qualification testing
"""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.9.4 Dry run of software item qualification testing
""""""""""""""""""""""""""""""""""""""""""""""""""""


5.9.5 Performing software item qualification testing
""""""""""""""""""""""""""""""""""""""""""""""""""""


5.9.6 Analyzing and recording software item qualification test results
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.9.7 Software item qualification regression testing
""""""""""""""""""""""""""""""""""""""""""""""""""""


5.9.8 Revising and retesting software items
"""""""""""""""""""""""""""""""""""""""""""


5.10 Software-hardware item integration and testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.10 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on software- hardware
item integration and testing. This paragraph shall
be divided into the following subparagraphs to
describe the approach to be followed for
participating in software-hardware item
integration and testing.


5.10.1 Testing on the target computer system
""""""""""""""""""""""""""""""""""""""""""""


5.10.2 Preparing for software-hardware item integration and testing
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.10.3 Performing software-hardware item integration and testing
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.10.4 Analyzing and recording software-hardware item integration and test results
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.10.5 Software-hardware item integration regression testing
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.10.6 Revising and retesting software-hardware item integration
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.11 System qualification testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.11 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on system
qualification testing. This paragraph shall be
divided into the following subparagraphs to 
describe the approach to be followed for
participating in system qualification testing.


5.11.1 Independence in system qualification testing
"""""""""""""""""""""""""""""""""""""""""""""""""""


5.11.2 Testing on the target computer system(s)
"""""""""""""""""""""""""""""""""""""""""""""""


5.11.3 Preparing for system qualification testing
"""""""""""""""""""""""""""""""""""""""""""""""""


5.11.4 Dry run of system qualification testing
""""""""""""""""""""""""""""""""""""""""""""""


5.11.5 Performing system qualification testing
""""""""""""""""""""""""""""""""""""""""""""""


5.11.6 Analyzing and recording system qualification test results
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.11.7 System qualification regression testing
""""""""""""""""""""""""""""""""""""""""""""""


5.11.8 Revising and retesting the system
""""""""""""""""""""""""""""""""""""""""


5.12 Preparing for software transition to operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.12 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on preparing for
software transition to operations. This paragraph
shall be divided into the following subparagraphs
to describe the approach to be followed for
preparing for software transition to operations.


5.12.1 Preparing the executable software
""""""""""""""""""""""""""""""""""""""""


5.12.2 Preparing version descriptions for user sites
""""""""""""""""""""""""""""""""""""""""""""""""""""


5.12.3 Preparing user manuals
"""""""""""""""""""""""""""""


5.12.3.1 Software user manuals
""""""""""""""""""""""""""""""


5.12.3.2 Computer operations manuals
""""""""""""""""""""""""""""""""""""


5.12.4 Installation at user sites
"""""""""""""""""""""""""""""""""


5.13 Preparing for software transition to maintenance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.13 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on preparing for
software transition to maintenance. This paragraph
shall be divided into the following subparagraphs
to describe the approach to be followed for
preparing for software transition to maintenance.


5.13.1 Preparing the executable software
""""""""""""""""""""""""""""""""""""""""


5.13.2 Preparing source files
"""""""""""""""""""""""""""""


5.13.3 Preparing version descriptions for the maintenance site(s)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.13.4 Preparing the “as built” software architecture, design, and related information
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.13.5 Updating the system/subsystem design description
"""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.13.6 Updating the software requirements
"""""""""""""""""""""""""""""""""""""""""


5.13.7 Updating the system requirements
"""""""""""""""""""""""""""""""""""""""


5.13.8 Preparing maintenance manuals
""""""""""""""""""""""""""""""""""""


5.13.8.1 Computer programming manuals
"""""""""""""""""""""""""""""""""""""


5.13.8.2 Firmware support manuals
"""""""""""""""""""""""""""""""""


5.13.9 Transition to the designated maintenance site
""""""""""""""""""""""""""""""""""""""""""""""""""""


5.14 Software configuration management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.14 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on software
configuration management. This paragraph shall be 
divided into the following subparagraphs to
describe the approach to be followed for software
configuration management.


5.14.1 Configuration identification
"""""""""""""""""""""""""""""""""""


5.14.2 Configuration control
""""""""""""""""""""""""""""


5.14.3 Configuration status accounting
""""""""""""""""""""""""""""""""""""""


5.14.4 Configuration audits
"""""""""""""""""""""""""""


5.14.5 Packaging, storage, handling, and delivery
"""""""""""""""""""""""""""""""""""""""""""""""""


5.14.6 Baselines
""""""""""""""""


5.15 Software peer reviews and product evaluations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.15 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on software peer
reviews and product evaluations. This paragraph
shall be divided into the following subparagraphs
to describe the approach to be followed for
software peer reviews and product evaluations.


5.15.1 Software peer reviews
""""""""""""""""""""""""""""


5.15.1.1 Plan for software peer reviews
"""""""""""""""""""""""""""""""""""""""


5.15.1.2 Prepare for an individual peer review
""""""""""""""""""""""""""""""""""""""""""""""


5.15.1.3 Conduct peer reviews
"""""""""""""""""""""""""""""


5.15.1.4 Analyze and report peer review data
""""""""""""""""""""""""""""""""""""""""""""


5.15.2 Product evaluations
""""""""""""""""""""""""""


5.15.2.1 In-process and final product evaluations
"""""""""""""""""""""""""""""""""""""""""""""""""


5.15.2.2 Product evaluation records
"""""""""""""""""""""""""""""""""""


5.15.2.3 Independence in product evaluations
""""""""""""""""""""""""""""""""""""""""""""


5.16 Software quality assurance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.16 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on software quality
assurance. This paragraph shall be divided into 
the following subparagraphs to describe the 
approach to be followed for software quality 
assurance.


5.16.1 Software quality assurance evaluations
"""""""""""""""""""""""""""""""""""""""""""""


5.16.2 Software quality assurance records
"""""""""""""""""""""""""""""""""""""""""


5.16.3 Independence in software quality assurance
"""""""""""""""""""""""""""""""""""""""""""""""""


5.16.4 Software quality assurance noncompliance issues
""""""""""""""""""""""""""""""""""""""""""""""""""""""


5.17 Corrective action
^^^^^^^^^^^^^^^^^^^^^^

See Section 5.17 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on corrective action.
This paragraph shall be divided into the following
subparagraphs to describe the approach to be
followed for corrective action.


5.17.1 Discrepancy and change reports (DCRs)
""""""""""""""""""""""""""""""""""""""""""""

These DCRs shall include the items to be recorded
specified in Appendix C, Table C.2-5 of (SDSMCS).


5.17.2 Corrective action system
"""""""""""""""""""""""""""""""


5.18 Joint technical and management reviews
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See Section 5.18 and its subparagraphs in the body
of (SDSMCS) for the activities and topics to be
addressed in this paragraph on joint technical and
management reviews. See Appendix E, Joint
Technical and Management Reviews for additional
requirements for joint technical and management
reviews. This paragraph shall be divided into the
following subparagraphs to describe the approach
to be followed for joint technical and management
reviews.


5.18.1 Joint technical reviews
""""""""""""""""""""""""""""""


5.18.2 Joint management reviews
"""""""""""""""""""""""""""""""


5.19 Software risk management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe the approach for
performing risk management. See Section 5.19 in
the body of (SDSMCS) for the activities and topics
to be addressed in this paragraph on software risk
management.


5.20 Software measurement
^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall briefly summarize the
approach to be used for software measurement
throughout the system development lifecycle. This
paragraph shall also itemize the specific software 
measurements to be collected, analyzed,
interpreted, applied, and reported. In addition,
this paragraph shall summarize the importance of
each specific measurement used for decision
making, corrective actions, and reporting to the
acquirer. See Section 5.20 and its subparagraphs
in the body of (SDSMCS) for the activities and
topics to be addressed in this paragraph on
software measurement. When a separate software
measurement plan (SMP) is not required on
contract, this paragraph shall include the content
described in the SMP template provided in Appendix
H.4. When a separate SMP is required on contract,
this paragraph shall include a reference to the
SMP.


5.20.1 Software measurement planning
""""""""""""""""""""""""""""""""""""


5.20.2 Software measurement reporting
"""""""""""""""""""""""""""""""""""""


5.20.3 Software measurement working group (SMWG)
""""""""""""""""""""""""""""""""""""""""""""""""


5.21 Security and privacy
^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe the approach for
meeting the security and privacy requirements.
See Section 5.21 in the body of (SDSMCS) for the
activities and topics to be addressed in this
paragraph on security and privacy.


5.22 Software team member management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall list all software developers
at any level (e.g., prime contractor, software
team members). This paragraph shall identify all
software, including custom, COTS, modified, and
reused, developed by foreign contractors at any
level (e.g., prime contractor, software team
members) that will be delivered to the acquirer.
This paragraph shall identify the foreign
contractor’s company name and foreign location(s).
A “foreign contractor” means any foreign
corporation, business association, partnership,
trust, society or any other entity or group that
is not incorporated or organized to do business in
the United States, as well as international
organizations, foreign Governments, and any agency
or subdivision of foreign Governments (e.g.,
diplomatic missions). This paragraph shall
describe the approach for performing software team
member management. This paragraph shall specify
the mechanisms to be used to ensure that all
contractual requirements, and all changes to
contractual requirements, are flowed down to all
levels of software team members. See Section 5.22
in the body of (SDSMCS) for the activities and
topics to be addressed in this paragraph on
software team member management.


5.23 Interface with software independent verification and validation (IV&V) agents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe the approach for
interfacing with the software IV&V agents. See
Section 5.23 in the body of (SDSMCS) for the
activities and topics to be addressed in this
paragraph on interfacing with software independent
verification and validation agents.


5.24 Coordination with associate developers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe the approach for
performing the coordination with associate
developers, working groups, and interface groups.
See Section 5.24 in the body of (SDSMCS) for the
activities and topics to be addressed in this
paragraph on coordination with associate
developers.


5.25 Improvement of project processes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall describe the approach for
performing the improvement of project processes.
See Section 5.25 in the body of (SDSMCS) for the
activities and topics to be addressed in this
paragraph on improvement of project processes.


6. Schedules and activity network
---------------------------------

This section shall be divided into the following
paragraphs:


6.1 Schedule
^^^^^^^^^^^^

This paragraph shall present schedule(s)
identifying the activities and showing initiation
of each activity, availability of draft and final
deliverables, other milestones, and completion of
each activity. This paragraph shall provide the
detailed schedule activities for each software
item, and other software, for each build, and for
the entire software development lifecycle. See
paragraph 7.2.1.4 below for inclusion of the
rationale for the software cost and schedule
estimation, including software cost and schedule
estimation techniques, the input to those
techniques (e.g., software size and software cost
driver parameters and scale factors), and any
assumptions made.


6.2 Activity network
^^^^^^^^^^^^^^^^^^^^

An activity network depicting sequential
relationships and dependencies among activities
and identifying those activities that impose the
greatest time restrictions on the project.


7. Project organization and resources
-------------------------------------

This section shall be divided into the following
paragraphs to describe the project organization
and resources.


7.1 Project organization
^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall be divided into the following
subparagraphs to describe the organizational
structure to be used on the project, including
the organizations involved, their relationships
to one another, and the authority and
responsibility of each organization for carrying
out required activities. Note: COTS software
suppliers are not included in this paragraph
and its subparagraphs.


7.1.1 Software team members
"""""""""""""""""""""""""""

This paragraph shall identify each geographic site
of each software team member organization that is
performing the project-related effort for any
software-related activities. (See Section 3.1 of
the body of (SDSMCS) for the definition of
software team member.) For each software team
member organization site this paragraph shall
include all of the following information:

#. Organization site name (e.g., XYZ Co. Div ABA,
   City, State).
#. Parent organization name (e.g., company).
#. Internal organization name, i.e., name of
   division or other level (e.g., ground software
   development).
#. Organization site location, i.e., city, state,
   and country.
#. Software-related activities that the software
   team member is expected to be performing at
   this site.
#. The internal structure of each software team
   member, showing all software-related entities
   (e.g., software development groups, test
   groups, software process organizations,
   software quality assurance, software
   configuration management) and how they relate
   to other project and organizational entities
   (e.g., program management, systems engineering,
   system integration and test, hardware
   engineering, quality assurance, configuration
   management). Note: References to supplied 
   organization charts could provide this
   information for item 6.


7.1.2 Full set of project software
""""""""""""""""""""""""""""""""""

This paragraph shall identify the full set of
software items and other software for all
categories of software for this project. This
paragraph shall include for each software item
and other software:

#. Name of the software item or other software.
#. System, subsystem, and any other components
   to which the software belongs.
#. Category of software.
#. For each software team member responsible for 
   all or part of the software item or other 
   software, identify the:

   #. Responsible software team member
   #. Organization site name, i.e., same as in
      7.1.1.a.
   #. Part(s) of the software item or other
      software for which the software team
      member is responsible.
   #. Source of software, i.e., new, reused as is,
      modified reuse, COTS.
   #. If the software is of mixed source, then
      list the percentages of each type of source.


7.1.3 Software team receiver-giver relationships
""""""""""""""""""""""""""""""""""""""""""""""""

This paragraph shall show the contractual and
intracorporation receiver-giver relationships
among the software team members, including the
prime contractor. An internal software team member
receiver is the software team member requiring and
receiving a software item, or other software, from
one of the other software team members. An
internal software team member giver is the
software team member supplying or giving the
required software item or other software to the
software team member that required the product.
This paragraph shall be organized by internal
software team member receiver with the prime
contractor relationships first. If a single
software team member has multiple sites performing
software-related efforts on this project, then
each organization site shall be treated
separately. For each internal receiver-giver pair,
this paragraph shall identify each software item,
and other software, produced by the internal giver
for the internal receiver. This paragraph shall
include for each receiver-giver software team
member relationship:

#. Internal software team member receive
   organization site name.
#. Internal software team member giver
   organization site name.
#. List of name(s) of each software item and other
   software to be produced by the giver for the
   receiver.


7.2 Project resources
^^^^^^^^^^^^^^^^^^^^^

This paragraph shall be divided into the following
subparagraphs to describe the resources to be
applied to the project.


7.2.1 Personnel resources
"""""""""""""""""""""""""

This paragraph shall provide the following items
for the entire software development lifecycle and
for each software item, and other software:


7.2.1.1 Staff hours by software item
""""""""""""""""""""""""""""""""""""

The estimated staff-loading for the project i.e., 
number of total personnel hours by month
throughout the system development lifecycle,
broken out as follows:

#. For each software team member:

   #. For each software item and other software
   #. For each other piece of software
   #. For each build
   #. For the entire software development
      lifecycle

#. For all software team members for the entire
   software development effort.


7.2.1.2 Staff hours by responsibility
"""""""""""""""""""""""""""""""""""""

The breakdown of the staff-loading for the
project, i.e., number of total personnel hours
by month throughout the system development life
cycle, broken out by responsibility (for example,
management, software engineering, software
testing, software configuration management,
product evaluation, software quality assurance):

#. For each software team member:

   #. For each software item
   #. For each other piece of software
   #. For each build
   #. For the entire software development
      lifecycle.

#. For all software team members for the entire
   software development effort.


7.2.1.3 Number of personnel by skill level
""""""""""""""""""""""""""""""""""""""""""

For each software team member, a breakdown of
the number of personnel by skill level of those
personnel performing each responsibility used in
paragraph 7.2.1.2:

#. For each software team member:

   #. For each software item
   #. For each other piece of software
   #. For each build
   #. For the entire software development
      lifecycle.

#. For all software team members for the entire
   software development effort.


7.2.1.4 Rationale
"""""""""""""""""

The rationale for the schedule estimates in
paragraph 6.1 and the effort and head count
estimates in section 7.2, including software 
cost and schedule estimation techniques, the
input to those techniques (e.g., software size
and software cost driver parameters and scale
factors), and any assumptions made.


7.2.1.5 Training
""""""""""""""""

Description of the training required for each
software team member organization site. Also a
description of the training required for each
new staff member.


7.2.2 Overview of developer facilities
""""""""""""""""""""""""""""""""""""""

For each organization site, this paragraph shall
list the development and test facilities, secure
areas, and other site features to be used, as
applicable to the software development, including
which work will be performed at each facility,
area, or other site feature. This paragraph shall
include a schedule detailing when these items will
be needed, developed or acquired, and validated.


7.2.3 Acquirer-furnished equipment and information
""""""""""""""""""""""""""""""""""""""""""""""""""

This paragraph shall list acquirer-furnished
equipment, software, services, documentation,
data, and facilities, as applicable, required
for the software development effort. A schedule
detailing when these items will be needed shall
also be included.


7.2.4 Other required resources
""""""""""""""""""""""""""""""

This paragraph shall list other required
resources, including a plan for obtaining the
resources, dates needed, and availability of each
resource item.


8. Notes
--------

This section shall contain any general information
that aids in understanding this document (e.g.,
background information, glossary, rationale). This
section shall be divided into the following
paragraphs.


8.1 Abbreviations and acronyms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall include an alphabetical
listing of all acronyms, abbreviations, and their
meanings as used in this document.


8.2 Glossary
^^^^^^^^^^^^

This paragraph shall include a list of any terms
and their definitions needed to understand this
document. Terms often used differently between
organizations (e.g., acquisition phase names,
build, block, development phase names,
effectivity, evolution, increment, and iteration)
shall be defined to avoid confusion. If the terms
used are exactly as defined in the Software
Development Standard (SDSMCS), they need not be
redefined here.


8.3 General information
^^^^^^^^^^^^^^^^^^^^^^^

This paragraph shall contain any other general 
information that aids in understanding this 
document (e.g., background information,
rationale).


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
(Appendix A, B, etc.).