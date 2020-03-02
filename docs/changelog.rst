Changelog
=========

0.3.0
-----

- **Backwards compatibility break:** The CDP API avoids shadowing Python
  built-ins. For example, an argument called ``id`` in CDP will be renamed to
  ``id_`` in this library. Other common names include ``type_`` and
  ``format_``.
- The documentation has been improved to be faster to load and navigate.
- Better handling of the "deprecated" and "experimental" flags.
