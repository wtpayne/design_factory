=========================
Documentation style guide
=========================


Document content and writing style
----------------------------------


Tone and language
^^^^^^^^^^^^^^^^^

* Use clear, professional language
* Write in active voice
* Keep sentences concise and direct
* Use present tense
* Prioritize clarity, then accuracy, then persuasiveness


Document structure
^^^^^^^^^^^^^^^^^^

* Follow relevant standards and conventions for the document type



Document formatting
-------------------


Headers and sections
^^^^^^^^^^^^^^^^^^^^

* Use minimal capitalization (sentence case) for all headers
* Keep headers concise and descriptive
* Avoid punctuation in headers
* Place two blank lines before headers
* Place one blank line after headers
* Document title: Use `=` above and below, same length as title
* Section: Use `-` below, same length as header
* Subsection: Use `^` below, same length as header  
* Sub-subsection: Use `"` below, same length as header


Paragraphs
^^^^^^^^^^

* Keep paragraphs focused on single topics
* Use short to medium length paragraphs
* Wrap lines at approximately 65 characters for readability (guidance only)
* Add one blank line between paragraphs


Text formatting
---------------


Emphasis
^^^^^^^^

* Use `**text**` for bold
* Use `*text*` for italics
* Use ````text```` for inline code
* Apply emphasis consistently throughout documents
* Use emphasis to highlight technical terms and improve clarity


Lists and enumerations
----------------------

* Use `*` for unordered lists
* Use `#.` for ordered lists
* Indent sub-lists consistently
* Add blank line before and after lists
* Add blank line before and after sub-lists
* Capitalize first word of each list item
* Avoid ending list items with periods


Formatted examples
------------------

* Use `.. code-block:: language` directive
* Include appropriate language identifier
* Indent formatted blocks consistently
* Add descriptive comments for clarity

Example:
.. code-block:: rst
    .. code-block:: python
        def example():
            """
            Descriptive docstring

            """

            return True


Diagrams
--------

* Use ASCII diagrams when appropriate
* Ensure proper alignment and spacing
* Add explanatory text before diagrams
* Use consistent symbols for similar elements

Example:

    ┌──────────────────────┐
    │                      │
    │        Box 1         │
    │    (description)     │
    │                      │
    └───────────┬──────────┘
                │
                │ edge label
                │
                ▼
    ┌──────────────────────┐
    │                      │
    │        Box 2         │
    │    (description)     │
    │                      │
    └──────────────────────┘


Cross-references
----------------

* Use descriptive labels for references
* Keep reference names lowercase and underscore-separated
* Place references close to relevant content


Document examples
-----------------

The following examples demonstrate proper document formatting 
and structure.

.. code-block:: rst


    ==============
    Document title
    ==============

    Brief introduction paragraph explaining the document's 
    purpose.


    Section header
    --------------

    Content organized into clear paragraphs with a single 
    focus. Lines wrapped at approximately 65 characters.

    Another paragraph providing additional information.


    Sub-section header
    ^^^^^^^^^^^^^^^^^^

    More detailed content organized under relevant
    subsections.


    Sub-sub-section header
    """"""""""""""""""""""

    Even more fine grained orgamization using 
    sub-sub-sections.
