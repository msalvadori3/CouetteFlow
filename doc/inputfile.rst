.. _inputfile:

Input File
==========

The input file is central location for setting any and all parameters for all the features in |CouetteFlow|. Depending on the type of operation being performed on |CouetteFlow|, the relevant input options are set in the input file.

.. _str-geometry:

Structure of the Geometry Module
--------------------------------

.. parsed-literal::

  <geometry>
      <jmax>51</jmax>
   </geometry>

.. _str-setup:

Structure of Setup Module
-------------------------

.. parsed-literal::

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

.. _str-post:

Structure of Postprocessing Module
----------------------------------

.. _plot-input:

|CouetteFlow| also allows the user to graphically visualize the results through the use of graphs and contours. Inputs to this plotting utility are also provided through the input file. The relevant block for this utility is shown below, and linked to the dedicated plotting utility page.

.. parsed-literal::

    <PostProcessing>
      <plot>
          <iPost>1</iPost>
          <Method>TecPlot</Method>
          <files>rmslog.dat</files>
          <style>k +r</style>
          <label>Grid</label>
          <LegendFontSize>16</LegendFontSize>
          <FigureSize>10 7</FigureSize>
          <AxisLabelSize>21</AxisLabelSize>
          <AxisTitleSize>22</AxisTitleSize>
          <XTickSize>23</XTickSize>
          <YTickSize>24</YTickSize>
      </plot>
    </PostProcessing>


.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
