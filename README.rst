==========
pyrewriter
==========

Pyparsig extension that captures grammar parsing result as tokens tree that
can be modified and written back as text. Used to modify config files.

Why?
====

Where is no standard way to read non-ini config file (for example, nginx),
programmaticaly add or change something and add it back. The only way is
regexp, but it fails in non-trivial cases and resulting file formatting
may became a mess.

