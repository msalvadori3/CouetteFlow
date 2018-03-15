Code development
================

The present project is aimed to develop a computer program for solving 1-D unsteady 'Couette Flow' problem. Hereafter, the program developed in this project is called 'CouetteFlow'.

CouetteFlow Code summary
------------------------

The source code contains the following directories:

* io - input/output related routines
* main - main program driver
* math - thomas algorithm 
* modules - main couette flow solver routines
* utils - list of useful FORTRAN utilities used within the program
* couettepy - python wrapper for gridgen main program

 Also a 'CMakeLists.txt' file is also included for cmake compiling.

::

   $ cd CouetteFlow/src/
   $ ls
   $ CMakeLists.txt  io  main math modules utils couettepy

The **io** folder has **io.F90** file which contains **ReadInput(inputData)** subroutine. It also includes **input_file_xml** which describes the structure of the user run-time input file located in the main 'src' directory, and **output.F90** for storing data in bothb Tecplot and Python format.

The **main** folder is only used for containing the code driver file. The main routines is run by **couette.F90** which calls important subroutines from the rest of folders.

Details of CouetteFlow development
----------------------------------

The source code shown below is **couette.F90** and it calls skeletal subroutines for generating grid structure. The main features of the main code is to (1) read input file, (2) make initialized variable arrays, (3) se the BCs and ICs, (4) set the time step for the solver, (5) Non-dimensionalize the variables , (6) use the thomas algorithm to calculate and update the velocity, and (7) finally write output files along with the RMS::

        PROGRAM main
             
              USE xml_data_input_file 
              USE CouetteSetup_m,ONLY:Init,EndVars,TimeStep,NonDim2DimVars,&
                                      Dim2NonDimVars
              USE parameters_m,ONLY:wp
              USE SimVars_m,ONLY:fileLength,c1,c2,cr,elapse_time,rate,iflag,&
                                  dt,t,nmax,rms_SS,rms_US,maxRMS_US
              USE CouetteSolver_m,ONLY:TriDiag,SteadySoln,UnsteadySoln,SteadyRMS,UnsteadyRMS
              USE output_m,ONLY:WritePlotFile,WriteRMS

              IMPLICIT NONE

              TYPE(input_type_t) :: inputData
              CHARACTER(LEN=fileLength) ::output= 'data'
              CHARACTER(LEN=fileLength) :: rmsout = 'rms'
              INTEGER :: n
         
              ! Start the time measurements
              elapse_time = 0.0_wp

              CALL system_clock(count_rate=cr)
              rate = REAL(cr)
              CALL system_clock(c1)

              ! Call the initialization of variables
              CALL Init(inputData)
              ! Setup the time step based

              IF (dt == 0.0_wp) THEN
                      iflag = 0
                      WRITE(*,*)'---------------------------------------------------------'
                      CALL TimeStep(iflag)
                      WRITE(*,*)'---------------------------------------------------------'
                      IF (iflag == 1) STOP

              END IF 

              CALL SteadySoln()
              CALL NonDim2DimVars()
              CALL UnsteadySoln()
              CALL NonDim2DimVars()

              ! Output Initial Solutions
              WRITE(*,*) 'Printing Initial Solution.......................................'
              CALL WritePlotFile(output,'"y","u","uExact","yp","up","upExact"',inputData,t)
              WRITE(*,*)'-----------------------------------------------------------------'

              ! Time loop
              DO n = 1,nmax

                t = t+dt

                CALL Dim2NonDimVars()
                CALL TriDiag()
                CALL UnsteadySoln()
                CALL NonDim2DimVars()
                CALL UnsteadyRMS()
                CALL SteadyRMS()
                MaxRMS_US = MAX(MaxRMS_US,rms_US)
                CALL WriteRMS(n,rms_SS,rms_US,rmsout,inputData)

                IF (MOD(n,inputData%setup%nout) == 0) THEN
                    CALL WritePlotFile(output,'"y","u","uExact","yp","up","upExact"',inputData,t)
                END IF

                IF (rms_SS < inputData%setup%RMSres) THEN
                        iflag = 1
                        WRITE(*,*) '---------------------------------------------------------------------'
                        WRITE(*,*) 'Convergence Successful=======> Printing Solution.....................'
                        CALL WritePlotFile(output,'"y","u","uExact","yp","up","upExact"',inputData,t)
                        WRITE(*,*) '---------------------------------------------------------------------'
                        EXIT
                ENDIF

               END DO

               ! Last check for non-convergence

               IF (iflag /= 1) THEN
                       WRITE(*,'(A,X,I6.6,X,A)') 'CONVERGENCE FAILURE WITH',nmax,'ITERATIONS'
               END IF

              CALL system_clock(c2)

              elapse_time = REAL(c2-c1,KIND=wp)/rate

              WRITE(*,*) ""
              WRITE(*,'(A,F10.6,A)') "| Total elapse time: ",elapse_time, " [s]|"

        END PROGRAM main

