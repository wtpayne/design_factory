==================
The design factory
==================


Overview
========

The design factory is where the design process
happens.

At the core of the design process are design
documents. Design documents control the
manufacture and configuration of all the products
and services which we offer to our colleagues,
customers and partners.

Design documents are almost always written using
formal notations that enable them to control
various automated processes.

These formal notations include both programming
language notations and data serialization language
notations.

Despite the fact that much of the design process
involves the production of documents written
using programming languages and other similar
formal notations, these documents are written
primarily by and MUST be written primarily for
human beings.

We aspire to be designers, not hackers or coders.

A design document which is coded, obfuscated or
difficult to comprehend is a symptom of slovenly
design, and an expression of contempt for your
colleagues. We strive to be better than this.

Systematic, rigorous, clean and elegant. Designed
for humans, not machines.


Structure
=========

On your local filesystem, the design factory
takes the form of a hierarchical structure of
files and directories, the outermost of which
is normally named using the abbreviation 'df'.

The top level 'df' design factory directory
contains one or more workspaces, each named
using a different workspace identifier.


Workspace directories
---------------------

The main, primary workspace is normally given
the identifier 'ws00_pri'

Other secondary workspaces are normally
given similar identifiers with a 'ws' prefix,
sequentially ascending two digit serial number,
and human-readable, english-language, lowercase,
underscore-delimited suffix.

Each workspace contains a set of design documents
and is normally treated as a separate, self
contained and internally consistent set of
designs. Colleagues with a software engineering
background will recognize each workspace as a
local working copy (or "clone") of a unitary
("monolithic") source document repository.

The ability to have multiple workspaces present
at the same time within the design factory is
primarily intended as a convenience when working
concurrently on mutually inconsistent design
configurations.

Each workspace directory contains within it five
inner "process area" directories. Each of these
process area directories are associated with a
particular part of the design process

* df
  * ws00_pri
    * a0_env - The technical environment
    * a1_cfg - Personal configuration
    * a2_dat - Dataset management system
    * a3_src - Source design document repository
    * a4_tmp - Temporary working file storage
    * a5_cms - Configuration management system


a0_env - The technical environment
----------------------------------

The first process area directory holds a set of
managed external dependencies which are available
for use within our designs.

These external dependencies include third party
tools, virtual machine disk images, vendored
third party source files, built third party
binary dependencies, and any associated technical
documentation.

Together, these artifacts consistute the technical
environment within which our designs are situated.


a1_cfg - Personal configuration
-------------------------------

The second process area directory holds a
set of configuration files for individual
users and specific devices.

This area is intended to help support the
ability to reproduce the working environment
of individual team members - either to recover
from a catastrophic failure or to reproduce
and diagnose problems.

This area was created because Eclipse
configuration can affect the behaviour of the
build but is at the same time both user and
machine specific, making it unsuitable to store
in the main part of the repository.


a2_dat - Dataset management system
----------------------------------

The third process area directory is used as
part of a system for storing and accessing
large sets of data files for system validation
and machine learning model training.

This mainly consists of a systematic structure
of symlinks to externally located datasets,
rather than files checked-in to the document
repository itself.


a3_src - Source design document repository
------------------------------------------

The fourth process area directory is used
as the main repository for design documents.

This acts as the source of truth for system
design configurations and the input to
any manufacturing, production or commissioning
process.


a4_tmp - Temporary working file storage
---------------------------------------

Automated processes build to here.

A structured area for temporary files that
may be generated as part of the build.


a5_cms - Configuration management system
----------------------------------------

A structured area for storing build outputs
and different product configurations.
