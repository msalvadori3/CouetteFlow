!> \file: CouetteSetup.F90
!> \author: Marc Salvadori

MODULE CouetteSetup_m

      USE parameters_m,ONLY: wp
      
      IMPLICIT NONE

CONTAINS

      SUBROUTINE Init(inputData)

              USE xml_data_input_file
              USE io_m, ONLY: ReadInput

              IMPLICIT NONE

              TYPE(input_type_t) :: inputData

              CALL ReadInput(inputData)
              CALL InitVars()
              CALL SetBCs()
              CALL Dim2NonDimVars()

      END SUBROUTINE Init

      SUBROUTINE InitVars()

              USE SimVars_m, ONLY: jmax,yp,up,y,u,u_exact,u_exactSS,&
                                    up_exactSS,up_exact,tp,t

              IMPLICIT NONE

              WRITE(*,'(A)') "INITIALIZING ARRAYS FOR SIMULATION"
              ALLOCATE(yp(jmax))
              ALLOCATE(up(jmax))
              ALLOCATE(y(jmax))
              ALLOCATE(u(jmax))
              ALLOCATE(u_exact(jmax))
              ALLOCATE(up_exact(jmax))
              ALLOCATE(u_exactSS(jmax))
              ALLOCATE(up_exactSS(jmax))

              y = 0.0_wp
              u = 0.0_wp
              yp = 0.0_wp
              up = 0.0_wp
              u_exact = 0.0_wp
              up_exact = 0.0_wp
              u_exactSS = 0.0_wp
              up_exactSS = 0.0_wp
              t = 0.0_wp
              tp = 0.0_wp

      END SUBROUTINE InitVars

      SUBROUTINE EndVars()

              USE SimVars_m,ONLY:yp,up,y,u,u_exact,up_exact,&
                                u_exactSS,up_exactSS

              IMPLICIT NONE

              DEALLOCATE(yp)
              DEALLOCATE(up)
              DEALLOCATE(y)
              DEALLOCATE(u)
              DEALLOCATE(u_exact)
              DEALLOCATE(up_exact)
              DEALLOCATE(u_exactSS)
              DEALLOCATE(up_exactSS)

      END SUBROUTINE EndVars

      SUBROUTINE SetBCs()

              USE SimVars_m,ONLY:jmax,y,dy,u,L,Utop
              USE parameters_m,ONLY:PI
              
              IMPLICIT NONE

              INTEGER :: j

              dy = L/(jmax-1)

              DO j=1,jmax

                y(j) = dy*(j-1)

                u(j) = Utop*(y(j)/L + SIN(PI*y(j)/L))

              END DO

              WRITE(*,'(A,G15.6)') "dy = ",dy
              

      END SUBROUTINE SetBCs


      SUBROUTINE Dim2NonDimVars()

              ! Routine to non-dimensionalize the variables

              USE SimVars_m,ONLY:L,nu,t,y,yp,u,up,Utop,&
                                 dy,dt,u_exact,up_exact,u_exactSS,&
                                 up_exactSS,dtp,dyp,tp

              IMPLICIT NONE

              REAL(KIND=wp) :: tau


              tau = (L**2)/nu

              tp = t/tau
              yp = y/L
              up = u/Utop
              dtp = dt/tau
              dyp = dy/L
              up_exact = u_exact/Utop
              up_exactSS = u_exactSS/Utop

       END SUBROUTINE Dim2NonDimVars

       SUBROUTINE NonDim2DimVars()

               !Routine to dimensionalize variables
                
               USE SimVars_m,ONLY:L,nu,t,y,yp,u,up,Utop,&
                                 dy,dt,u_exact,up_exact,u_exactSS,&
                                 up_exactSS,dtp,dyp,tp


               IMPLICIT NONE

               REAL(KIND=wp) :: tau

               tau = (L**2)/nu
               t = tp*tau
               y = yp*L
               u = up*Utop
               dt = dtp*tau
               dy = dyp*L
               u_exact = up_exact*Utop
               u_exactSS = up_exactSS*Utop

       END SUBROUTINE NonDim2DimVars

       SUBROUTINE TimeStep(iflag)

               ! This Subroutine allows to deduce the time step based
               ! on the Von-Neumann stability analysis

               USE SimVars_m,ONLY: dt,dtp,dyp,theta


               IMPLICIT NONE
               
               INTEGER,INTENT(INOUT) :: iflag

               IF (theta >= 0.5_wp) THEN
                       ! This is the case for unconditionally stable

                       WRITE(*,'(A)') "UNCONDITIONALLY STABLE CASE"
                       WRITE(*,'(A)') "Please change the value of dt"
                       WRITE(*,'(A)') " from the inputfile.xml and rerun."

                       iflag = 1

               ELSE
                       ! This is the non-dimensional form of timestep
                       dtp = (dyp**2)/(4.0_wp*(0.5_wp-theta))
                       ! Convert non-dimensional form into dimensional form

                       CALL NonDim2DimVars()

                       WRITE(*,'(A,G15.6)') "THE SCHEME IS STABLE IF DT  <= :",dt
                       WRITE(*,'(A,G15.6)') "NON-DIMENSIONAL DT :",dtp

                       iflag = 0

               ENDIF

       END SUBROUTINE TimeStep


END MODULE CouetteSetup_m
