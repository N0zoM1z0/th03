# Original IBM PIT delay with calibrated CRT INITDATA — after478

Japanese Borland CL.LIB member cibmdely (index **524**) is
fully recovered as original [8086 source](../src/mainl/crt/cibmdely.asm).
It contains the true private PIT wait helper at CODE+0,
private near counter reader at CODE+5, complete FAR CRT
calibration initializer at CODE+35, and public FAR
___ibm_delay at CODE+91.

The calibration routine gates on the authentic conio_type
global, samples the PIT by writing port 43h and reading
port 40h with interrupts temporarily disabled, uses the
native low-bit retry and 100-attempt limit, and sets the
original calibrated 4-byte timing scale. The public delay
routine uses the actual N_LXMUL@ near 32-bit multiplier,
handles PIT counter rollover and waits for the original
32-bit threshold. The natural code preserves all unchecked
hardware/overflow behavior and the original stack/flags ABI.

The entire **188 CODE + 4 initialized DATA + 6 INITDATA
bytes** match. DATA+0 is the original 0952h seed and
DATA+2 is the original upper word. The true CRT
INITDATA contains priority 1001h plus a symbolic FAR
address of the initializer at CODE+35. All **seven
literal ordered original OMF FIXUPPs** match, including
the INITDATA segment-4 offset-2 four-byte reference
targeting CODE+35, the original DATA references and the
N_LXMUL@ CODE-frame near import at CODE+122. The
four original SEGDEFs, original 0aff03ff02 GROUP, true
FAR public and ordered imports also match. No target
machine-code arrays, dummy executable padding or
post-assembly object rewriting were used.

After478 validates the unchanged after477 native source
carrier and produces two new TASM/TLIB/TLINK rounds,
retaining raw OBJ/LIB/EXE/MAP outputs, writer logs and
complete source/driver/parent receipt hashes. Both Japanese
decoded MAINL EXE/MAP are byte-for-byte target-equal,
preserving all 67,372 EXE bytes and 677 original MZ
relocations. Working CRT reaches **686/893** original
source-linked members, **183,034 CODE bytes** and 207
contextual vendor members. No full cold replay or new
formal Factory accepted-source credit is implied.

Focused reviewer: scripts/review_th03_mainl_after478_work.py
(mode ibm-pit-delay-initdata-boss);
tests: tests.test_mainl_after478_work.
