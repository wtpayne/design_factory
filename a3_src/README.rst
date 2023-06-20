=================================
Source design document repository
=================================


Overview
========

This directory is used as the main repository
for design documents.

This acts as the source of truth for system
design configurations and the input to
any manufacturing, production or commissioning
process.


Structure
=========

h00_thirdparty
--------------

The h00_thirdparty tier is intended for design
elements which are brought in from third parties
and modified or customised by us in some way.

Most third party dependencies will reside outside
of the hierarchy and be incorporated into one or
more managed environments, but in some cases we
need to tailor or adapt those dependencies in
some way, which means co-versioning them and
managing them alongside our internally developed
design elements.

In principle, third party design elements should
not depend on nor know about any internally
developed design element.


h10_resource
------------

The h10_resource tier is intended for the
management of static resources used across all
products and product lines.

This includes things like brand logo and pallette,
document templates, organisation level registers
and mini-databases, and anything else with a
similar organisation wide pattern of use.


h20_functionality
-----------------

The h20_functionality tier is intended for the
management of design elements which are intended
for generic reuse.

This includes things like software libraries,
APIs and other similar design elements.

Most of the detailed design work should sit at
this level of the hierarchy.


h30_platform
------------

The h30_platform tier is intended for the
management of design elements which are intended
for use as an enabling platform of some sort.

This includes things like software frameworks
and middleware.

It is expected that design elements at the
platform level will make use of detailed design
elements managed at the h20_functionality level
of the hierarchy.


h40_component
-------------

The h40_component tier is intended for the
management of design elements which are intended
for reuse within the context of a component
framework.

It is expected that design elements at the
component level will make use of detailed design
elements managed at the h20_functionality level
of the hierarchy as well as frameworks managed
at the h30_platform level.


h50_subsystem
-------------

The h50_subsystem tier is intended for the
management of networks of components arranged
in functional chains or similar agglomerations
which provide some manageable subset of system
functionality. The primary purpose of this level
is to allow customisation of systems at a high
level of abstraction.

It is expected that design elements at the
subsystem level will consist of configurations
of components with associated scripts to enable
them to be customised and integrated into
larger systems.


h60_system
----------

The h60_system tier is intended for the
management of systems of components and
subsystems which are functionally complete
but not tailored to the requirements of
a specific customer.

It is expected that design elements at the
system level will consist of configurations
of subsystems, components, and associated
scripts which assemble all the pieces
together into a functional whole.


h70_bespoke
-----------

The h70_bespoke tier is intended for the
management of designs of bespoke products.

The designs in the h70_bespoke tier are
normally composed of tailorings applied
on top of off the shelf product designs
drawn from the h60_system tier.


h80_research
------------

The h80_research tier is intended for the
management of design elements that arise
from research activities.

The design elements managed in the h80_research
tier are normally composed of tailorings and
improvements that modify or replace design
elements drawn from tiers at lower levels of
the hierarchy.


h90_internal
------------

The h90_internal tier is intended for the
management of design elements, programs,
scripts, tools and utilities that are
used to automate the design process itself,
along with internal documentation, processes,
and launchers for demonstrations of work in
progress.