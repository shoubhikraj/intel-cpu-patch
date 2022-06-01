import re
import mmap
import itertools
import sys
import argparse

parser = argparse.ArgumentParser(description="Detect and optionally patch a binary compiled with Intel compiler or MKL for usage on AMD or other non-Intel systems.")
parser.add_argument('--force',action ='store_true', help="Use this switch to actually modify file, otherwise it only checks for cpu dispatch code")
parser.add_argument('filename',help="A binary file (*.exe, *.dll)")
if len(sys.argv)==1:
    print("No arguments given!")
    parser.print_usage()
    sys.exit(1)
args = parser.parse_args()


target_file = args.filename
edit_file = args.force


# this part checks the file extension
file_ext = target_file[-4:]
if (file_ext != ".exe") and (file_ext != ".dll"):
    print("Error! You should only modify binary files with this.")
    print("Your input file does not seem like a binary file i.e. *.exe or *.dll.")
    print("Exiting...")
    sys.exit(1)
# file extension check ends

intel_cpuid_strs = [b'Genu',b'ineI',b'ntel']

# The regex pattern would be a long string, so it is broken up in three substrings
pattern0 = b'[\x3A\x3B\x3C\x3D\x80\x81\x81\x83\x38\x39].{0,8}' 
pattern1 = b'.{0,3}[\x3A\x3B\x3C\x3D\x80\x81\x81\x83\x38\x39].{0,8}' 
pattern2 = b'.{0,3}[\x3A\x3B\x3C\x3D\x80\x81\x81\x83\x38\x39].{0,8}' 
# [\x3A\x3B\x3C\x3D\x80\x81\x81\x83\x38\x39] => cmp instruction x86
# It looks for this pattern :
# cmp (upto eight bytes gap) Genu 
# (upto three bytes for jump instruction)
# cmp (upto eight bytes gap) ineI
# (upto three bytes for jump instruction)
# cmp (upto eight bytes gap) ntel

cpudispatch_found = False

with open(target_file,'r+b') as fh:
    filestream = mmap.mmap(fh.fileno(),0)
    for combs in itertools.permutations(intel_cpuid_strs):
        intel_pattern = pattern0 + combs[0] + pattern1 + combs[1] + pattern2 + combs[2]
        for match in re.finditer(intel_pattern,filestream):
            print("Match for Intel CPUID check found at line number:", match.start())
            start_zone = int(match.span()[0])
            end_zone = int(match.span()[1])
            cpudispatch_found = True
            if edit_file:
                modify_zone = filestream[start_zone:end_zone+1]
                patched_zone = modify_zone.replace(b'Genu',b'Auth')
                patched_zone = patched_zone.replace(b'ineI',b'enti')
                patched_zone = patched_zone.replace(b'ntel',b'cAMD')
                filestream[start_zone:end_zone+1] = patched_zone
                print("Patched this CPUID check!")
    filestream.flush()
    if (not edit_file) and cpudispatch_found:
        print("The program has been run without the --force argument, so binary has not been modified.")
        print("If you wish to actually modify the binary (dangerous!), then add --force.")
    if not cpudispatch_found:
        print("Hurray! No Intel CPU dispatcher found in "+target_file)
        
