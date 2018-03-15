Documentaion for Solving CouetteFlow with different Numerical Schemes
=====================================================================

Author: Marc Salvadori

Email: msalvadori3@gatech.edu

Numerical solution schemes are often referred to as being explicit or implicit. When a direct computation of the dependent variables can be made in terms of known quantities, the computation is said to be explicit. When the dependent variables are defined by coupled sets of equations, and either a matrix or iterative technique is needed to obtain the solution, the numerical method is said to be implicit. In computational fluid dynamics, the governing equations are nonlinear, and the number of unknown variables is typically very large. Under these conditions implicitly formulated equations are almost always solved using iterative techniques.

Iterations are used to advance a solution through a sequence of steps from a starting state to a final, converged state. This is true whether the solution sought is either one step in a transient problem or a final steady-state result. In either case, the iteration steps resemble a time-like process. Of course, the iteration steps usually do not correspond to a realistic time-dependent behavior. In fact, it is this aspect of an implicit method that makes it attractive for steady-state computations, because the number of iterations required for a solution is often much smaller than the number of time steps needed for an accurate transient that asymptotically approaches steady conditions.

On the other hand, it is also this “distorted transient” feature that leads to the question, “What are the consequences of using an implicit versus an explicit solution method for a time-dependent problem?” The answer to this question has two parts. The first part has to do with numerical stability and the second part with numerical accuracy.

The purpose of this project is investigate the use of numerical schemes to try to answer the above questions.

Contents
========

.. toctree::
   :maxdepth: 2

   background
   setup
   inputfile
   devel
   couettepy
   results


.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
