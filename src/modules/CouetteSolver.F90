!> \file CouetteSolver.F90
!> \author Marc Salvadori

MODULE CouetteSolver_m
      USE parameters_m,ONLY:wp
      IMPLICIT NONE


CONTAINS

      SUBROUTINE TriDiag()

              USE SimVars_m, ONLY: jmax,dtp,dyp,theta,up
              USE thomas_m,ONLY:SY


              IMPLICIT NONE

              !Local Variables
              INTEGER :: j

              ! We define r = delt_prime/dely_prime**2
              REAL(KIND=wp) :: r
              REAL(KIND=wp),DIMENSION(jmax) :: a,b,c,d


              r = dtp/(dyp**2)

              DO j =1,jmax

                IF( j == 1 .OR. j == jmax) THEN

                        a(j) = 0.0_wp
                        b(j) = 1.0_wp
                        c(j) = 0.0_wp
                        d(j) = up(j)

                ELSE
                        a(j) = -r*theta
                        b(j) = 1.0_wp + 2.0_wp*r*theta
                        c(j) = -r*theta
                        d(j) = up(j) + r*(1.0_wp-theta)*&
                                (up(j-1) - 2.0_wp*up(j) +&
                                up(j+1))
                ENDIF
              ENDDO

              ! Calling the thomas algorithm

              CALL SY(1,jmax,a,b,c,d)

              DO j=1,jmax

                up(j) = d(j)

              ENDDO

        END SUBROUTINE TriDiag

        SUBROUTINE SteadyRMS()

                !This routine calculates the RMS error realtive to the SS exact solution

                USE SimVars_m,ONLY:jmax,up,up_exactSS,rms_SS

                IMPLICIT NONE

                !Local Variables
                INTEGER :: j
                REAL(KIND=wp) :: summ

                summ = 0.0_wp

                DO j =2,jmax-1
                  
                    summ = summ + (up_exactSS(j) - up(j))**2

                ENDDO

                rms_SS = (summ/(jmax-2))**(0.5_wp)

        END SUBROUTINE SteadyRMS

        SUBROUTINE UnsteadyRMS()

                !This routine calculates the RMS error realtive to the SS exact solution

                USE SimVars_m,ONLY:jmax,up,up_exact,rms_US

                IMPLICIT NONE

                !Local Variables
                INTEGER :: j
                REAL(KIND=wp) :: summ

                summ = 0.0_wp

                DO j =2,jmax-1
                  
                    summ = summ + (up_exact(j) - up(j))**2

                ENDDO

                rms_US = (summ/(jmax-2))**(0.5_wp)

        END SUBROUTINE UnsteadyRMS

        SUBROUTINE SteadySoln()

                ! This routine evaluates the steady state solution
                ! at only one time which is before the time loop

                USE SimVars_m,ONLY: up_exactSS,yp,jmax

                IMPLICIT NONE

                ! Non-dimensional form

                up_exactSS = yp

        END SUBROUTINE SteadySoln

        SUBROUTINE UnsteadySoln()

                ! This routine evaluates the unsteady exact solution for 
                ! non-dimensional variables at every time step

                USE parameters_m,ONLY:PI
                USE SimVars_m,ONLY: up,up_exact,tp,yp,jmax

                IMPLICIT NONE

                up_exact = yp + SIN(PI*yp)*EXP(-PI**2*tp)

        END SUBROUTINE UnsteadySoln



END MODULE 