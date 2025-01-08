H.4 Software Measurement Plan (SMP) Template
This appendix is a MANDATORY part of the (SDSMCS). It provides the content requirements for
the SMP.
1. If the section numbering used below is not used, the developer shall provide an appendix in the
SMP with a traceability matrix mapping from the section numbers and titles below to the
section numbers and titles used in the developer SMP.
2. If there is such a traceability mapping appendix, it shall be referenced in Section 1.3.
Note 1: The information shown below is consistent with the Software Development Standard
for Mission Critical Systems, especially Sections 5.1 and 5.20.
Note 2: The definitions and terms used in this template are consistent with those in (ISO/IEC
15939).
Note 3: The definitions and terms used in this template are consistent with those in the Software
Measurement Standard (SMS).
Note 4: Additional guidance is provided in the Software Measurement Standard (SMS).
Purpose: The Software Measurement Plan (SMP) is an integrated plan covering the software
development measurement activities for all software team members throughout the system
development. The SMP provides the planned metrics and their aggregation levels, explanations of
computation, expected or projected values, thresholds, and any planned corrective actions to be taken
in case thresholds are breached.
References
(ISO/IEC 15939) International Organization for Standards/International Electrotechnical
Commission (ISO/ IEC), Systems and Software Engineering – Measurement Process,
ISO/IEC 15939:2007, 1 August 2007.
(SMS) Abelson, L. A., S. Eslinger, M. C. Gechman, C. H. Ledoux, M. V. Lieu, K. Korzac,
Software Measurement Standard for Mission Critical Systems, Aerospace Report No.
TOR-2009(8506)-6, 5 May 2011, The Aerospace Corporation.
(SDSMCS) Adams, R. J., S. Eslinger, K. L. Owens, J. M. Tagami, and M. A. Zambrana,
Software Development Standard for Mission Critical Systems (SDSMCS), Aerospace
Report No. TR-RS-2015-00012, March 17, 2014, The Aerospace Corporation. This is
the same as SMC Standard SMC-S-012, Software Development Standard.
Content Requirements
This template contains the required content of the Software Measurement Plan (SMP). See Section 3
of the Software Development Standard for Mission Critical Systems (SDSMCS) for definitions of all
italicized words or phrases.
1. Scope. This section shall be divided into the following paragraphs.
1.1 Identification. This paragraph shall contain a full identification of the system and the software
to which this document applies, including, as applicable, identification number(s), title(s),
abbreviation(s), version number(s), and release number(s).
1.2 System overview. This paragraph shall briefly state the purpose of the system and the software
to which this document applies. It shall: a) describe the general nature of the system and software; b)
summarize the history of system development, operation, and maintenance; c) identify the project
H.4-1
Downloaded from http://www.everyspec.com
sponsor, acquirer, user, developer, and support organizations; and d) identify current and planned
operating and user sites.
1.3 Document overview. This paragraph shall summarize the purpose and contents of this
document. This paragraph shall summarize the role of the SMP in the project’s measurement process.
This paragraph shall describe any security or privacy considerations associated with its use.
1.4 Relationship to other plans and documents. This paragraph shall describe the relationship, if
any, of the SMP to the SDP and other project plans and documents.
2. Referenced documents. This section shall list the number, title, revision, and date of all
documents referenced in this plan. This section shall also identify the source for all documents
not available through normal Government stocking activities.
3. Project measurement description. This section shall be divided into the following paragraphs.
3.1 Project measurement characteristics. This paragraph shall:
a. Identify the project team responsible for implementing the measurement plan, including the
prime contractor and other software team members;
b. Depict and describe the organizational structure to be used for measurement, including all
organizations, their relationships to one another, the authority and responsibility of each for
carrying out required activities, and points of contact for each. This paragraph shall reference
relevant documents with citations; and
c. Identify current and planned operations, maintenance, and user sites.
3.2 Measurement management characteristics. This paragraph shall briefly state:
a. The management review hierarchy for the measurement data;
b. The management reporting systems, i.e., tools and reports, that contain measurement data;
and
c. The approval sequencing for all measurement data.
3.3 Project measurement approach. This paragraph shall be divided into paragraphs as needed to
establish the context for the planning described in later sections. It shall include, as applicable, an
overview of:
a. How measurement is integrated into the technical and management processes;
b. How system, software, and hardware measurements are related;
c. How data will be collected and used;
d. Measurement points of contact, i.e., prime contractor and other software team members;
e. Measurement roles, responsibilities, and resources;
f. Communication interfaces between project metrics personnel and organizational metrics
personnel;
g. Implementation of the measurement approach, address builds and their associated lifecycle
activities, if applicable;
h. Tools and databases to be used for the measurement process;
i. Configuration management of the measurement process and data, including addressing how
measures are added, modified, or deleted for future reports; and
j. Evaluation criteria for the measurement process, measures, and indicators.
3.4 Software identification items. This paragraph shall provide the software identification items
specified in the Software Identification Items paragraph of (SMS).
H.4-2
Downloaded from http://www.everyspec.com
4. Measurement description. This section shall be divided into the following paragraphs. Provisions
corresponding to nonrequired activities may be satisfied by the words “Not applicable.” If
different builds, different software items, different part of the software items, or different types or
categories of software on the project require different planning, then these differences shall be
noted in the paragraphs. In addition to the content specified below, each paragraph shall identify
applicable risks and uncertainties and the plans for dealing with them.
4.1 Software measurement process. This paragraph shall describe the process to be used for
measurement data collection and reporting throughout the system development lifecycle. This
paragraph shall describe the software development lifecycle model(s) to be used, including: a)
planned builds, if applicable, b) their build objectives, and c) the software measurements to be
collected in each build.
4.2 General requirements. This paragraph shall be divided into the following paragraphs.
4.2.1 Measurement goals. This paragraph shall be divided into the following subparagraphs.
4.2.1.1 Organizational goals. This paragraph shall describe or reference the organizational
goals that impact the project’s measurement system. This paragraph shall discuss any
organizational goals for specific process improvement initiatives either currently planned or
projected.
4.2.1.2 Project goals. This paragraph shall describe or reference the project goals,
quantitative or otherwise, that impact the project’s measurement system. This paragraph shall
include any project-specific process improvement initiatives either currently planned or
projected.
4.2.1.3 Prioritized goals. This paragraph shall itemize the organizational and project goals
into a single priority-ordered list.
4.2.2 Recording rationale. This paragraph shall describe the approach to be followed for recording
rationale for key decisions about software measurements made on the project. This paragraph shall
interpret the term “key decisions” for the project. The rationale shall include tradeoffs considered,
analysis methods, and criteria used to make decisions. This paragraph shall state where the rationale
is to be recorded.
4.2.3 Access for acquirer review. This paragraph shall describe the approach to be followed for
providing the acquirer and its authorized representatives access to developer and software team
member quantitative data about the products and activities.
4.2.4 Meeting contractual requirements. This paragraph shall describe how the planned software
measurement process covers all contractual requirements concerning software measurement
collection, reporting, acquirer team access, management, and related topics.
Note: The exact contractual requirements for deliverables are in the contract. Those contractual
requirements state where the software measurement planning information is to be recorded. If the
software measurement plan is not a deliverable, then the software measurement planning information
can be included in Section 5.20 of the SDP or in a separate software measurement plan.
4.2.5 Measurement information specification. This paragraph shall contain the measurement
information need description for each measure that is identified for use on the project. See
H.4-3
Downloaded from http://www.everyspec.com
Measurement Information Specification Information Need table of the (SMS) for more information.
This paragraph shall be divided into the following subparagraphs. The subsequent subparagraphs
(4.2.5.x below) specify high level information about each measure. For each measure identified for
use on the project, this paragraph shall provide:
4.2.5.x Measure name. This paragraph shall be divided into the following subparagraphs to describe
the identified measure. Provisions corresponding to nonrequired activities may be satisfied by the
words “Not applicable.”
a. Information need. What the measurement user (e.g., manager or project team member)
needs to know in order to make informed decisions.
b. Information category. A logical grouping of information needs provided as structure of
the measurements. The information category shall be one of the following: schedule and
progress, resources and costs, product size and stability, product quality, and
development performance.
c. Measurable concept. An idea for satisfying the information need by defining the data to
be measured.
d. Relevant entities. The object that is to be measured. Entities include process or product
elements of a project such as project tasks, plans, estimates, resources, and deliverables.
e. Base measure(s). The property or characteristic of the data that is quantified.
f. Derived measure(s). A measure that is calculated as a function of two or more base
measures or other derived measures, to obtain a derived measure.
g. Prioritized goals. The list of prioritized goals, i.e., specified in Paragraph 4.2.1.3 above,
to which this measure responds.
Note: Section 5 below requires detailed specifications for each indicator, base measure, and
derived measure that support the measures in Paragraph 4.2.5.
5. Software measures. This section shall describe the measures to be used for software measurement
throughout the system development lifecycle. This section shall also include the specific software
measures to be used, i.e., collected, interpreted, analyzed, applied, reported, and used for
decisionmaking, corrective actions, and reporting to the acquirer. This section shall specify
which measures will be reported by lifecycle activity (e.g., requirements, design, code,
integration, test). This section shall be divided into the following paragraphs. Provisions
corresponding to nonrequired activities may be satisfied by the words “Not applicable.” For each
measure, i.e., specified in Paragraph 4.2.5 above, selected for use on the project, this section shall
provide:
5.1 Indicator specifications. This paragraph shall be divided into the following subparagraphs. For
each measurement information specification identified in Paragraph 4.2.5 above, include at least one
of the following:
5.1.x Indicator name. This paragraph shall be divided into the following subparagraphs to describe
the identified indicator. The measurement information specification, i.e., specified in Paragraph 4.2.5
above, to which this indicator responds shall be identified.
a. Indicator description. A text discussion of how one or more measures are used to support
the creation of information necessary for analysis and decision making. An indicator is
often displayed as a graph or chart.
b. Example indicator diagram. A sketch of the indicator diagram incorporating sample data.
This subparagraph shall provide a description of how the example indicator diagram is to
be interpreted.
H.4-4
Downloaded from http://www.everyspec.com
c. Analysis model. A defined process that applies decision criteria to characterize the
positive or negative behavior of the indicator. If decision criteria are specified, then this
field describes their use.
d. Decision criteria. A project performance threshold that delineates positive indicator
behavior from negative indicator behavior. A defined set of actions that will be taken in
response to specific values of the indicator. This paragraph shall define the responses of
the measurement user to the indicator.
e. Frequency of data analysis. Identify how often the indicator is reported. This may be less
frequently than it is collected.
f. Responsible organization. Identify the organization assigned to analyze the indicator and
report the results.
g. Phase of analysis. Identify the phases or activities when the indicator is analyzed.
h. Source of data for analysis. Identify sources of data used in the indicator analysis.
i. Tools used in analysis. Identify any tools used for indicator analysis (e.g., statistical
tools).
j. User(s) of analysis. Identify the users of the indicator results.
k. Additional analysis guidance. Any additional guidance on variations of this measure.
l. Implementation considerations. Any process or implementation requirements that are
necessary for successful implementation.
5.2 Base measure specification. This paragraph shall be divided into the following subparagraphs.
For each base measure identified in Paragraph 4.2.5 above include:
5.2.x Base measure name. This paragraph shall be divided into the following subparagraphs to
describe the identified base measure.
a. Measurement method. The logical sequence of operations that define the counting rules
to collect the base measure.
b. Type of method. The type of method used to quantify the base measure, either (1)
subjective, involving human judgment, or (2) objective, using only established rules to
determine numerical values.
c. Scale. The ordered set of values or categories used to define the base measure.
d. Type of scale. The type of the relationship between values on the scale, either: Nominal,
Ordinal, Interval, or Range.
Note: See Measurement Information Specification Base Measure Specification table in
(SMS) for more information.
e. Unit of measure. The standardized quantitative amount that is counted to assign value to
the base measure. If tailoring is performed, the developer shall document the conversion
factors between the expected standard value and the developer’s tailored value. See the
Measurement Tailoring paragraph of (SMS).
Note: The developer may tailor the base measure collection and the derived measure
calculations specified in the (SMS) standard, where this tailoring is limited to the use of
different units of measure (UOMs) for base or derived measures.
f. Frequency of collection. Identify how often the data described by the base measure is
collected.
g. Responsible organization. Identify the organization assigned to collect the base measure.
h. Phase of collection. Identify the phases or activities when the base measure is collected.
i. Tools used in collection. Identify any tools used to collect the base measure (e.g., source
code analyzer).
j. Verification and validation. Identify any verification and validation activities (e.g., tests)
that will be executed to verify that the base measure is complete and accurate.
H.4-5
Downloaded from http://www.everyspec.com
5.3 Derived measure specification. This paragraph shall be divided into the following
subparagraphs. For each derived measure identified in paragraph 4.2.5 above, include:
5.3.x Derived measure name. This paragraph shall be divided into the following subparagraphs to
describe the identified derived measure.
a. Measurement function. The formula used to calculate the derived measure.
b. Scale. The ordered set of values or categories for each base measure used in the derived
measure function. Valid mathematical functions are limited by base measure scale.
c. Type of scale. The type of the relationship between values on the scale for the resulting
derived measure, either: Nominal, Ordinal, Interval, or Range.
d. Unit of measure. The standardized quantitative amount of the resulting derived measure.
If tailoring is performed, the developer shall document the conversion factors between
the expected standard value and the developer’s tailored value. See the Measurement
Tailoring paragraph of (SMS).
Note: The developer may tailor the base measure collection and the derived measure
calculations specified in the (SMS) standard, where this tailoring is limited to the use of
different units of measure (UOMs) for base or derived measures.
e. Frequency of calculation. Identify how often the derived measure function is calculated.
f. Responsible organization. Identify the organization assigned to perform the derived
measure function calculation.
g. Phase of collection. Identify the phases or activities in which the derived measure
function calculation occurs.
h. Tools used in calculation. Identify any tools used for the derived measure function
calculation.
i. Verification and validation. Identify any verification and validation activities (e.g., tests)
that will be executed to verify that the derived measure function calculation is complete
and accurate.
6. Measurement indicator reporting and aggregation structures. This section shall be divided into
the following paragraphs. Provisions corresponding to nonrequired activities may be satisfied by
the words “Not applicable.”
6.1 Report aggregation. Measures reported may be aggregated to higher levels of aggregation using
specific mathematical functions. Aggregation may occur up through product integration, e.g., to builds,
software items, or any other applicable aggregation scheme. This paragraph shall identify the
indicators, base measures, and derived measures from paragraph 5 above for which aggregation will be
performed and reported. This paragraph shall specify which measures will be aggregated for each
build and software item. See the Software Measurement Aggregation Considerations paragraph in
(SMS) for more information on aggregation. For each indicator, base measure, and derived measure
for which aggregation is to be performed, this paragraph shall provide:
6.1.1 Aggregated measures. This paragraph shall be divided into the following subparagraph to
describe each identified aggregated measure.
6.1.1.x Aggregated measure name. This paragraph shall be divided into the following
subparagraphs to describe the identified aggregated measure.
a. Measurement function. The formula used to calculate the aggregated measure.
b. Scale. The ordered set of values or categories for each base or derived measure used in
the aggregated measure function. Valid mathematical functions are limited by base and
derived measure scales.
H.4-6
Downloaded from http://www.everyspec.com
c. Type of scale. The type of the relationship between values on the scale for the resulting
derived measure, either: Nominal, Ordinal, Interval, or Range.
d. Unit of measure. The standardized quantitative amount of the resulting aggregated
measure.
e. Frequency of calculation. Identify how often the aggregated measure function is
calculated.
f. Responsible organization. Identify the organization assigned to perform the aggregated
measure function calculation.
g. Phase of collection. Identify the phases or activities when the aggregated measure
function calculation occurs.
h. Tools used in calculation. Identify any tools used in the aggregated measure function
calculation.
i. Verification and validation. Identify any verification and validation activities (e.g., tests)
that will be executed to verify that the aggregated measure function calculation is
complete and accurate.
6.2 Build aggregated measures. This paragraph shall specify the aggregated measure names, i.e.,
specified in Paragraph 6.1.1 above, which will be aggregated for each build. If there are any
differences in the aggregated measures between builds, then this paragraph shall specify the
differences.
6.3 Software item aggregated measures. This paragraph shall specify the aggregated measure
names, i.e., specified in Paragraph 6.1.1 above, which will be aggregated for each software item. If
there are any differences in the aggregated measures between software items, then this paragraph
shall specify the differences.
6.4 Reporting. This paragraph shall specify: a) the planned contents of measurement reports, b)
frequency of measurement reports, c) planned delivery mechanism(s), i.e., electronic and human-
readable), and d) planned recipients of the reports. This paragraph shall specify for each software
item (SI) and build how the following four items will be reported electronically. See the Measurement
Data Electronic Reporting paragraph of (SMS). This paragraph shall also specify for each software
item (SI) and build how the measurement diagrams and analyses of the measurement data will be
reported in human-readable form. See the Measurement Data Human-Readable Reporting paragraph
of (SMS). This paragraph shall also specify the aggregated measurements to be reported: a)
electronically, and b) in human-readable form. The aggregated measurements to be reported shall
include:
a. Project characteristic data. All project characteristics, as specified in the Project
Characteristics paragraph of (SMS).
b. Base measures. All base measures, as specified in the Base Measure Specifications
appendix of (SMS), with tailored UOMs provided.
c. Derived measures. All derived measures, as specified in the Derived Measure
Specifications appendix of (SMS), with tailored UOMs provided.
d. Identification items. All identification items, as specified in the Software Identification
Items paragraph of (SMS).
7. Notes. This section shall contain any general information that aids in understanding this
document (e.g., background information, glossary, rationale). This section shall be divided into
the following paragraphs.
7.1 Abbreviations and acronyms. This paragraph shall include an alphabetical listing of all
acronyms, abbreviations, and their meanings as used in this document.
H.4-7
Downloaded from http://www.everyspec.com
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
END of SMP Template