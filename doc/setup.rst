.. _setup-couetteflow:

Setup
=====

.. _setup:

Setting up Couette Solver
-------------------------

.. _structure:

Code Structure
--------------

The |CouetteFlow| code is divided into three major parts:

#. |  **Input**: User input is entered into a file called ``input_file.xml``. 

#. |  **Main Program**: The main program for solving the elliptical grid is ``main.F90`` in the ``<parent directory>/src/main`` folder. 

#. |  **Output**: Once the code is run, the results are stored in the ``<parent directory>/output/`` folder.

.. _input:

Input File
----------

The inputs for CouetteFlow solver are specified in the ``input_file.xml``. The input file is accessed as follows:

#. Go to the parent directory::

     $ cd <path to |CoetteFlow|>
    
   Make sure that you are in the directory that contains the files :command:`setup.py`, :command:`input_file.xml`, and the folder :command:`src`.

#. Open the input file::

     $ vi input_file.xml  


#. The main parts of the input file are shown below

The input file is divided into different parts. The geometry is set in the ``<geometry>`` module, which is shown below:

.. code-block:: xml

    <geometry>
      <jmax>51</jmax>
    </geometry>

For setup of the solver, most of the inputs are set in the ``<setup>`` module. A  snippet of this module is shown below:

.. code-block:: xml
   
    <setup>
      <Project>2D_CouetteFlow</Project>
      <Utop>1.0</Utop>
      <nu>1.0</nu>
      <nmax>1000000000</nmax>
      <nout>1</nout>
      <L>1.0</L>
      <dt>10000.0</dt>
      <theta>1.0</theta>
      <RMSres>1.0e-7</RMSres>
    </setup>

.. _compilation:

Compilation
-----------

The following sequence of commands is used to compile a single simulation.

#. Go to the parent directory::

    $ cd <path to |CouetteFlow|>
    
   Make sure that you are in the directory that contains the files :command:`setup.py`, :command:`input_file.xml`, and the folder :command:`src`.

#. Clean existing results::

    $ ./setup.py -u clean heavy
    
   This command removes the existing files in the output folder ``|CouetteFlow|/output/`` and deletes the object files from previous compilations. **Backup any required results before using this command.**
    
#. Set working directory path::
    
    $ ./setup.py -u set_path
    
   This command sets the working directory path 
    
#. Compile the build::

    $ ./setup.py -e configure
    
   An empty CMake window opens. Press :class:`[c]` on the keyboard to configure the program.
    
    This brings up the CMake window. There are two options for the :command:`CMAKE_BUILD_TYPE` :
      * :class:`Release`: This compiles the program in regular mode; debugging flags are disabled.
      * :class:`Debug`:   This compiles the program in debug mode; errors and warnings are displayed on the terminal.
      
    Press :class:`[Enter]` on the keyboard to edit the option (to change from :class:`Release` to :class:`Debug` or vice versa)
    
    The file :command:`|CouetteFlow|.x` will now be generated in the parent directory
    
#. Execute the program::

     $ ./couette.x
     
   This command runs the program. If Debug mode is enabled in :command:`COUETTE_COMPILE_DEFS`, appropriate output is printed on the Terminal screen. 

.. _results:   

Results
-------

The results are stored in the ``output/`` folder inside the parent directory. The output directory contains several files **.dat** and **.tec** where the calculations are written. In addition, there is also a ``output/plot`` folder, where figures from the calculated data are plotted. To plot the results. open the inputfile and enter the name of the **.dat** file that was generated in the ``files`` entry (as shown below).

.. code-block:: xml

      <PostProcessing> 
          <plot>
             <files>RESULTDATFILE</files>
             ...
          </plot>
      </PostProcessing>
         
Then, from the parent directory execute the following command to plot the results using |CouetteFlow|'s built-in plotting utility::

    $ ./setup.py -p multi_plot
    
This will generate the compined solution plots from the results, which will be stored in the ``output/plot`` folder.


.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
