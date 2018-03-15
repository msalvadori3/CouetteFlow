!> \file:couette.F90
!> \author: Marc Salvadori

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

      ! Setup the time step

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

      ! Deallocate arrays
      CALL EndVars()
      CALL system_clock(c2)

      elapse_time = REAL(c2-c1,KIND=wp)/rate

      WRITE(*,*) ""
      WRITE(*,'(A,F10.6,A)') "| Total elapse time: ",elapse_time, " [s]|"

END PROGRAM main