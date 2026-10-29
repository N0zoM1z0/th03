; Expand two packed pixels into four plane BYTEs. Plane b receives the low
; pixel's bit b in bit0 and the high pixel's bit b in bit1. The original table
; is stored in CS and indexed by input BYTE *4. No instruction bytes or filler.
public RotTbl
RotTbl label dword

rotation_input = 0
REPT 256
	rotation_entry = 0
	rotation_plane = 0
	REPT 4
		rotation_pair = ((rotation_input SHR rotation_plane) AND 1) OR (((rotation_input SHR (rotation_plane+4)) AND 1) SHL 1)
		rotation_entry = rotation_entry OR (rotation_pair SHL (rotation_plane*8))
		rotation_plane = rotation_plane + 1
	ENDM
	DD rotation_entry
	rotation_input = rotation_input + 1
ENDM
