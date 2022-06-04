! ifort -O3 -Qmkl:sequential for Windows
! ifort -O3 -qmkl=sequential for Linux
!

program MatMulTest

implicit none

interface
  subroutine do_dgemm()
  end subroutine do_dgemm
end interface

!DIR$ NOINLINE
call do_dgemm() ! do not inline this subroutine

end program MatMulTest


subroutine do_dgemm()

integer, parameter :: N = 3000 ! =>This determines the size of NxN matrix
integer :: i, j
integer*8 :: cr, t0, t1
real*8 :: A(N,N), B(N,N), C(N,N) 
real*8 :: rate, tot_time

call random_seed()
call random_number(A)
call random_number(B)

! First initialize the system_clock
CALL system_clock(count_rate=cr)
WRITE(*,fmt="(a19,i0)") "system_clock rate: ", cr

call system_clock(count=t0)
do i = 1, 100, 1
    call dgemm('N','N',N,N,N,1.d0,A,N,B,N,0.d0,C,N)            
end do

call system_clock(count=t1)
rate = real(cr)
tot_time = real(t1-t0)/rate

write(unit=*, fmt="(a10,f10.5,a2)") "Time taken : ", tot_time, " s"
write(unit=*, fmt="(a24,f10.3)") "First element of C: ", C(1,1)

end subroutine do_dgemm


