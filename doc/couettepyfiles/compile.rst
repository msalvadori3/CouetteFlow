Compilation Options
===================

|CouetteFlow| has several builtin compilation options, that can be accessed through the command :command:`./setup.py -e` and allied utilities that can be accessed using :command:`./setup.py -u`. These are described here.

Configure
+++++++++

The default method for compiling |CouetteFlow| from scratch is using the command::

  $ ./setup.py -e configure couetteflow
  
This generates a CCMake window with configuration options that can be chosen by the user. Refer to the :ref:`compilation section <compilation>` of the :ref:`|CouetteFlow| Setup page<setup-couetteflow>` for details on using this method.

Compile
+++++++

This option should be used only if |CouetteFlow| has been configured first (using ``-e configure``). This recompiles the code with any changes, while retaining the build directory and related objects. It can be executed using the command::

  $ ./setup.py -e compile couetteflow
  
Setting the path
================

|CouetteFlow| requires the path to the working directory be set every time a run is executed from scratch (i.e. after clearing all the compilations). The |CouetteFlow| executable ``couette.x`` will not run without this path set. To set the path, compile/configure |CouetteFlow| using any of the options, and then run::

  $ ./setup.py -u set_path
  
  
Cleaning commands
=================

After completion of a simulation, or before running a fresh simulation, |CouetteFlow| can be cleared of compiled objects, results and other files. There are three variants to clean |CouetteFlow|. The first is to perform a complete clean, which removes the build directories, the executables and any generated results. This can be accomplished by running::

  $ ./setup.py -u clean heavy
  
On the other hand, the build directories and executables can be retained while deleting only the results by running the command::

  $ ./setup.py -u clean results
  
The last variant is where the build directories alone are cleared, retaining the results and the executables, which is done using the command::

  $ ./setup.py -u clean

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
