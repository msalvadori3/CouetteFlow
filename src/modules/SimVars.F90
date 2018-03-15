!> \file: SimVars.F90
!> \author: Marc Salvadori

MODULE SimVars_m

      USE parameters_m,ONLY :wp
      IMPLICIT NONE
      
      !Obtain data from XML input file
      INTEGER, PARAMETER :: IOunit = 10, fileLength = 64
      CHARACTER(LEN=64) :: prjTitle
      REAL(KIND=wp) :: Utop,L,nu,theta
      INTEGER :: jmax
      INTEGER :: nmax,nout
      REAL(KIND=wp) :: dt
      
      
      !Prime Variables
      REAL(KIND=wp) :: dy,dtp,dyp,t,tp

      ! Flags for timestep evaluation

      INTEGER :: iflag
      
      ! Dimensional and Non-Dimensional variables
      REAL(KIND=wp),ALLOCATABLE,DIMENSION(:) :: yp,y
      REAL(KIND=wp),ALLOCATABLE,DIMENSION(:) :: up,u
      REAL(KIND=wp),ALLOCATABLE,DIMENSION(:) :: up_exact,up_exactSS,u_exact,u_exactSS

      ! RMS Residual variables

      REAL(KIND=wp) :: rms_SS,rms_US
      REAL(KIND=wp) :: maxRMS_US

      ! Time Variables

      INTEGER :: c1,c2,cr
      REAL(KIND=wp) :: elapse_time
      REAL(KIND=wp) :: rate


END MODULE SimVars_m