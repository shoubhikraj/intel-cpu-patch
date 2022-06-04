! compile with ifort -O3 -QaxCORE-AVX2 for Windows
! or ifort -O3 -axCORE-AVX2 for Linux 
! If you have a newer CPU (like Intel i7) that supports AVX-512 then use QaxCORE-AVX512 or QaxCOMMON-AVX512

program MatMulTest

implicit none


!DIR$ NOINLINE
call matrix_multiply() ! prevent inlining

contains

subroutine matrix_multiply()

integer, parameter :: N = 500 ! => this determines the size of the NxN square matrix
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
    C=MatMul(A,B)                
end do

call system_clock(count=t1)
rate = real(cr)
tot_time = real(t1-t0)/rate

write(unit=*, fmt="(a10,f10.5,a2)") "Time taken : ", tot_time, " s"
write(unit=*, fmt="(a24,f10.3)") "First element of C: ", C(1,1)

end subroutine matrix_multiply

end program MatMulTest
