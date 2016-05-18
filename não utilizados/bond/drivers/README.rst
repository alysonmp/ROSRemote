=========================
``bond`` protocol drivers
=========================
----------------------------------------------
Ambivalent bonds between interpreted languages
----------------------------------------------

.. contents::

The ``bond`` protocol is a *simple*, line-based serial protocol based on JSON
implementing a remote/recursive procedure call interface for command-line
interpreters.

``bond`` allows different languages to call each other, with the only
requirement of an open communication channel to a REPL.

Documentation is still incomplete. Please refer to the current reference host
implementation for further information:

http://www.thregr.org/~wavexx/software/python-bond/


Driver matrix
=============

========== ==== ==== ======== ====== ====== ===== === === ======== =====
Language   Call Eval Ev/Block Except Export N/Ser Out Rec Trans/Ex XCall
========== ==== ==== ======== ====== ====== ===== === === ======== =====
JavaScript ✓    ✓    ✓        ✓      ✓      ✓     ✓   ✓   ✓        ✓
PHP        ✓    ✓    ✓        ✓      ✓            ✓   ✓   ✓        ✓
Perl       ✓    ✓    ✓        ✓      ✓            ✓   ✓   ✓        ✓
Python     ✓    ✓    ✓        ✓      ✓      ✓     ✓   ✓   ✓        ✓
========== ==== ==== ======== ====== ====== ===== === === ======== =====

Call:
  Can "call" a native function by applying the supplied list of arguments to a
  function name, statement or expression.

Eval:
  Can evaluate an arbitrary statement and return it's value.

Ev/Block:
  Can evaluate an arbitrary code block in the top-level.

Except:
  Can forward exceptions back to the caller.

Export:
  Can accept foreign functions to be called natively.

N/Ser:
  Supports the native serialization method of the language in addition to JSON.

Out:
  Remote output (stdout/stderr) is redirected locally.

Rec:
  Evaluation is fully recursive (a foreign method can call back native code).

Trans/Ex:
  Allows exceptions themselves to be serialized.

XCall:
  "call" supports immediate, unevaluated code references.


Host matrix
===========

======== ====== ====== ===== ========= ========
Language Except Export N/Ser Recursive Trans/Ex
======== ====== ====== ===== ========= ========
Python_  ✓      ✓      ✓     ✓         ✓
Julia_   ✓      ✓            ✓          
======== ====== ====== ===== ========= ========

Except:
  Can forward local exceptions to the driver.

Export:
  Can export a local function to the driver.

N/Ser:
  Supports the native serialization method of the language in addition to JSON.

Recursive:
  Evaluation is fully recursive (an exported method can call back the driver).

Trans/Ex:
  Allows exceptions themselves to be serialized.

.. _Python: http://www.thregr.org/~wavexx/software/python-bond/
.. _Julia: http://www.thregr.org/~wavexx/software/julia-bond/


Authors and Copyright
=====================

| "bond-drivers" is distributed under the GNU GPLv2+ license (see COPYING).
| Copyright(c) 2014-2015 by wave++ "Yuri D'Elia" <wavexx@thregr.org>.

bond-drivers's GIT repository is publicly accessible at::

  git://src.thregr.org/bond-drivers

or at https://github.com/wavexx/bond-drivers
