H.5 Software Measurement Report (SMR) Template
This appendix is a MANDATORY part of the (SDSMCS). It provides the content requirements for
the SMR.
1. If the section numbering used below is not used, the developer shall provide an appendix in the
SMR with a traceability matrix mapping from the section numbers and titles below to the
section numbers and titles used in the developer SMR.
2. If there is such a traceability mapping appendix, it shall be referenced in Section 1.3.
Note 1: The information shown below is consistent with the Software Development Standard
for Mission Critical Systems (SDSMCS), especially Sections 5.1 and 5.20.
Note 2: The software measurement report (SMR) definitions and terms used below are
consistent with those in the Software Measurement Standard (SMS).
Purpose: Each Software Measurement Report (SMR) is an integrated report covering the software
development activities for all significant software team members throughout the system development.
The SMR provides explanations and interpretations of reported measurement data, including
deviations from expected or projected values and breaches of thresholds as well as any corrective
actions being undertaken. The software measurements collected and reported each month are
expected to vary because the lifecycle activities vary over time.
References
(CMMI) Software Engineering Institute, Capability Maturity Model Integration, Version 1.3,
CMMI for Development, Report No. CMU/SEI-2010-TR-033, November 2010,
Software Engineering Institute, Carnegie Mellon University. Capability Maturity
Model® and CMMI® are registered in the U. S. Patent and Trademark Office by
Carnegie Mellon University.
(SMS) Abelson, L. A., S. Eslinger, M. C. Gechman, C. H. Ledoux, M. V. Lieu, K. Korzac,
Software Measurement Standard for Space Systems, Aerospace Report No. TOR-
2009(8506)-6, 5 May 2011, The Aerospace Corporation.
(SDSMCS) Adams, R. J., S. Eslinger, K. L. Owens, J. M. Tagami, and M. A. Zambrana,
Software Development Standard for Mission Critical Systems (SDSMCS), Aerospace
Report No. TR-RS-2015-00012, March 17, 2014, The Aerospace Corporation. This is
the same as SMC Standard SMC-S-012, Software Development Standard.
Content Requirements
This template contains the required content of the Software Measurement Report (SMR). See
Section 3 of the Software Development Standard for Mission Critical Systems (SDSMCS) for
definitions of all italicized words or phrases.
1. Scope. This section shall be divided into the following paragraphs.
1.1 Identification. This paragraph shall contain a full identification of the system and the software
to which this document applies, including, as applicable, identification number(s), title(s),
abbreviation(s), version number(s), and release number(s). This paragraph shall provide the period of
reporting.
1.2 System overview. This paragraph shall briefly state the purpose of the system and the software
to which this document applies. It shall: a) describe the general nature of the system and software; b)
summarize the history of system development, operation, and maintenance; c) identify the project
H.5-1
Downloaded from http://www.everyspec.com
sponsor, acquirer, user, developer, and support organizations; and d) identify current and planned
operating and user sites.
1.3 Document overview. This paragraph shall summarize the purpose and contents of this
document. This paragraph shall describe any security or privacy considerations associated with its
use.
1.4 Relationship to other documents and plans. This paragraph shall describe the relationship, if
any, of the SMR to the Software Development Plan (SDP), software measurement plan, and other
project management plans.
2. Referenced documents. This section shall list the number, title, revision, and date of all
documents referenced in this plan. This section shall also identify the source for all documents
not available through normal Government stocking activities.
3. Metrics analysis summary. This section shall be divided into the following paragraphs.
3.1 Contract milestones. This paragraph shall identify significant project milestones for the next
six months.
3.2 Measurement performance. This paragraph shall summarize measurement performance
highlights that are detailed in the subsequent report. When a threshold identified in the Software
Measurement Plan (SMP) is breached, then mitigation planning shall be itemized in this section.
4. General requirements. This section shall be divided into the following paragraphs. Provisions
corresponding to nonrequired activities may be satisfied by the words “Not applicable.” If
different builds or different software on the project require different planning, these differences
shall be noted in the paragraphs.
4.1 Project build and software item characteristics. For each build and software item (SI), this
paragraph shall provide the context information specified in the Project Characteristics paragraph of
the Software Measurement Standard (SMS):
a. Computer resource characterization;
(1) Computer hardware identification;
(2) Computer communication identification;
(3) Computer storage hardware identification;
b. Authorizing agreement (e.g., Memorandum of Understanding (MOU), contract,
amendment);
c. Development organization(s);
d. Capability Maturity Model Integration for Development (CMMI®
-DEV) maturity level;
e. Application type;
f. Development process;
g. Software origin;
h. Computer language;
i. Reusable software applications, including COTS and acquirer-furnished software.
4.1.x Build x <Insert Name> characteristics. For each build “x,” this paragraph shall provide the
context information specified in paragraph 4.1 above. If any of these characteristics changes, then this
paragraph shall highlight the change(s).
H.5-2
Downloaded from http://www.everyspec.com
4.1.x.y Software item x.y <Insert Name> characteristics. For each software item (SI) “y” in the
build, this paragraph shall provide the context information specified in paragraph 4.1 above. If any of
these characteristics changes, then this paragraph shall highlight the change(s).
4.2 Identification items. For each build and SI, this paragraph shall provide the identification
information specified in the Software Identification Items paragraph of (SMS):
a. WBS element identifier;
b. Control account;
c. Integrated master schedule (IMS);
d. Specification tree identification number;
e. Component identification;
f. Acquisition phase identification;
g. Development phase identification;
h. System identification (version and release);
i. Subsystem identification (version and release);
j. Element identification (version and release);
k. Software item identification (version and release);
l. Build identification (Release);
m. Computer resource utilization (CPU):
(1) CPU identification(s) (ID(s));
(2) Computer resource utilization input/output ID;
(3) Computer resource utilization memory storage device;
n. Computer resource utilization response time.
4.2.x Build x <Insert Name> identification items. For each build, this paragraph shall provide the
context information specified in paragraph 4.2 above. If any of these characteristics changes, then this
paragraph shall highlight the change(s).
4.2.x.y Software item x.y <Insert Name> identification items. For each SI in the build, this
paragraph shall provide the context information specified in paragraph 4.2 above. If any of these
characteristics changes, then this paragraph shall highlight the change(s).
5. Measurement data human-readable reporting. This section shall report the data by the particular
component, e.g., build, increment, or evolution, to which they apply. In addition, this section
shall report the data by the SI to which they apply. This section shall be divided into the
following paragraphs. Provisions corresponding to nonrequired activities may be satisfied by the
words “Not applicable.” For each measurement diagram whenever a tailored Unit of Measure
(UOM) is used, a footnote or other appropriate notation shall document that fact. For each
measurement diagram, the subsections shall provide the following labeling information specified
in the Measurement Diagram Content and Labeling paragraph of (SMS):
a. Scope of the data;
b. SI or build name;
c. Product integration level;
d. Reporting period;
e. Reported by.
5.x Build identifier. Identify the specific component, e.g., build, increment, or evolution, to which
each of the subsequent measurements apply. This paragraph, including each of its sub-items and its
aggregated data (5.x.y through 5.x.y+1), shall be repeated for each build “x.”
H.5-3
Downloaded from http://www.everyspec.com
5.x.y Software item identifier. Identify the specific software item (SI) to which each of the
subsequent measurements apply. In addition to the content specified below, each paragraph shall
identify applicable risks and uncertainties and the plans for dealing with them. This paragraph,
including each of its sub-items and its aggregated data (5.x.y through 5.x.y.18, where “.x” is the build
and “.y” is the software item) shall be repeated for each software item “y.”
5.x.y.1 Requirement progress management indicator. For the current reporting period, this
paragraph shall provide in tabular and graphic form the following base and derived measures of
requirement progress. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Requirements progress management
paragraph:
a. Requirements defined
b. Requirements TBX closure
c. Requirements verified
d. Qualification methods
5.x.y.2 Development progress management indicator. For the current reporting period, this
paragraph shall provide in tabular and graphic form the following base and derived measures of
development progress. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Development progress management
paragraph:
a. Components defined
b. Units defined
c. Units coded and unit tested
d. Units integrated and tested
5.x.y.3 Test progress management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base and derived measures of test progress. For the
current reporting period, plot and report base and derived measures in accordance with the
instructions provided in the (SMS) Test progress management paragraph:
a. Test cases developed
b. Test cases dry run
c. Test cases performed
d. Test cases passed
5.x.y.4 Schedule adherence management indicator. For the current reporting period, this paragraph
shall provide in tabular and graphic form the following base and derived measures of schedule
adherence. For the current reporting period, plot and report base and derived measures in accordance
with the instructions provided in the (SMS) Schedule adherence management paragraph:
a. Project milestones
b. Scheduled activities
5.x.y.5 Effort profile management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base and derived measures of effort profile
management. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Effort profile management paragraph:
a. Labor hours
b. Rework labor hours
H.5-4
Downloaded from http://www.everyspec.com
5.x.y.6 Staff profile management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base and derived measures of staff profile
management. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Staff profile management paragraph:
a. Staffing level
b. Staff by experience
c. Staff turnover
5.x.y.7 Computer resource management indicator. For the current reporting period, this paragraph
shall provide in tabular and graphic form the following base and derived measures of computer
resource management. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Computer resource management paragraph:
a. CPU utilization
b. Memory utilization
c. Input/output utilization
d. Response time
5.x.y.8 Cost profile management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base and derived measures of cost profile
management. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Cost profile management paragraph:
a. Earned value performance
b. Schedule and cost performance index
c. Schedule and cost variance
5.x.y.9 Size management indicator. For the current reporting period, this paragraph shall provide in
tabular and graphic form the following base and derived measures of size management. For the
current reporting period, plot and report base and derived measures in accordance with the
instructions provided in the (SMS) Size management paragraph:
a. Requirements size
b. Requirements by type
c. Line of code size
d. Line of code by origin
e. Line of code by type
5.x.y.10 Volatility management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base and derived measures of volatility
management. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Volatility management paragraph:
a. Requirement volatility
b. Line of code volatility
5.x.y.11 Build content management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base measures of build content management. For
the current reporting period, plot and report base measures in accordance with the instructions
provided in the (SMS) Build content management paragraph:
a. Requirements per build
5.x.y.12 Defect resolution management indicator. For the current reporting period, this paragraph
shall provide in tabular and graphic form the following base and derived measures of defect
H.5-5
Downloaded from http://www.everyspec.com
resolution management. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Defect resolution management paragraph:
a. Discrepancy report status
b. Discrepancy report aging
c. Discrepancy report by type
d. Discrepancy report by source
5.x.y.13 Complexity management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base measures of complexity management. For the
current reporting period, plot and report the base measure in accordance with the instructions
provided in the (SMS) Complexity management paragraph:
a. Cyclomatic complexity
5.x.y.14 Coverage management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base and derived measures of coverage
management. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Coverage management paragraph:
a. Requirements to design traceability
b. Requirements to test traceability
5.x.y.15 Productivity management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base and derived measures of productivity
management. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Productivity management paragraph:
a. Development productivity
5.x.y.16 Maturity management indicator. For the current reporting period, this paragraph shall
provide in tabular and graphic form the following base and derived measures of maturity
management. For the current reporting period, plot and report base and derived measures in
accordance with the instructions provided in the (SMS) Maturity management paragraph:
a. Development defect density
5.x.y.17 Management status management indicator. For the current reporting period, this paragraph
shall provide in tabular and graphic form the following base and derived measures of management
status. For the current reporting period, plot and report base and derived measures in accordance with
the instructions provided in the (SMS) Management status paragraph:
a. Action item closure
b. Risk mitigation task Completion Status
c. Schedule compression
5.x.y.18 Aggregated measurement report (SI level). For the current reporting period, this paragraph
shall report any aggregated measurements identified for the project as specified in the project
software measurement plan (SMP) for the software item (SI). This information shall be reported for
each paragraph 5.x.y SI after all of the other measurements for that SI.
5.x.y+1 Aggregated measurement report (build level). For the current reporting period, this
paragraph shall report any aggregated measurements identified for the project as specified in the
project software measurement plan (SMP) for the build. This information shall be reported for each
paragraph 5.x build after all of the other measurements of the software items for that build.
H.5-6
Downloaded from http://www.everyspec.com
6. Measurement data electronic reporting. This section shall specify the electronic reporting of
measurement data. This section shall be divided into the following paragraphs.
6.1 Base measures. In accordance with the data definitions provided in (SMS) Appendix A, Base
Measure Specifications, this paragraph shall provide the planned base measure data. For the current
reporting period, this paragraph shall provide actual base measure counts in accordance with the data
definition provided in (SMS) the Base Measure Specifications appendix.
6.2 Derived measures. For the current reporting period, this paragraph shall report the calculated
derived values in accordance with the data definition provided in (SMS) the Derived Measure
Specifications appendix.
6.3 Aggregated measurement report. Report any aggregated measurements identified for the
project as specified in the project software measurement plan (SMP).
7. Notes. This section shall contain any general information that aids in understanding this
document (e.g., background information, glossary, rationale). This section shall be divided into
the following paragraphs.
7.1 Abbreviations and acronyms. This paragraph shall include an alphabetical listing of all
acronyms, abbreviations, and their meanings as used in this document.
7.2 Glossary. This paragraph shall include a list of any terms and their definitions needed to
understand this document. Terms often used differently between organizations (e.g., acquisition phase
names, build, block, development phase names, effectivity, evolution, increment, and iteration) shall
be defined to avoid confusion. If the terms used are exactly as defined in the Software Development
Standard (SDSMCS) and Software Measurement Standard (SMS), they need not be redefined here.
7.3 General information. This paragraph shall contain any other general information that aids in
understanding this document (e.g., background information, rationale).
A. Appendices. Appendices may be used to provide information published separately for
convenience in document maintenance (e.g., charts, classified data). As applicable, each
appendix shall be referenced in the main body of the document where the data would normally
have been provided. Appendices may be bound as separate documents for ease in handling.
Appendices shall be lettered alphabetically (A, B, etc.).
END of SMR Template