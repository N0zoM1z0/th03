; MAINL heap manager: one bounded include, not a translation unit.
; Derived from the master.lib implementations by Akihiko Koizuka in the pinned
; ReC98 revision recorded in provenance.json; localized for the reviewed TH03 GAME=3 body.
; Requires the enclosing .386, USE16, MODEL LARGE _TEXT and DS=DGROUP context.
; Existing root word providers: mem_TopSeg, mem_MyOwn, mem_AllocID, mem_Reserve,
; mem_OutSeg, mem_TopHeap, mem_FirstHole, mem_EndMark. No storage is allocated here.
; MEMHEAD models three words in a 16-byte header paragraph, not a six-byte allocation.
; Far Pascal arguments are measured after one saved word; no external func macros.
MAINL_HEAP_ARG0 EQU 6
MAINL_HEAP_ARG1 EQU 8


; Round the unsigned 32-bit byte count modulo 2^32. Overflow beyond paragraphs returns without clearing AllocID.
PUBLIC HMEM_LALLOCATE
EVEN
HMEM_LALLOCATE PROC FAR
push	BX
mov	BX,SP
byteh = MAINL_HEAP_ARG1
bytel = MAINL_HEAP_ARG0
mov	AX,SS:[BX+byteh]
mov	BX,SS:[BX+bytel]
add	BX,15
adc	AX,0
shr	AX,1
rcr	BX,1
shr	AX,1
rcr	BX,1
shr	AX,1
rcr	BX,1
shr	AX,1
jnz	short @@NOMEM
rcr	BX,1
push	BX
call	HMEM_ALLOC
pop	BX
retf	4
@@NOMEM:
mov	AX,0
stc
pop	BX
retf	4
EVEN
HMEM_LALLOCATE ENDP

; DOS AH=48 allocation: on success assign returned AX/BX; NEG preserves the original zero-error quirk.
PUBLIC MEM_ASSIGN_DOS
EVEN
MEM_ASSIGN_DOS PROC FAR
push	BX
mov	BX,SP
parasize = MAINL_HEAP_ARG0
mov	BX,SS:[BX+parasize]
mov	AH,48h
int	21h
jc	short @@NOMEM
push	AX
push	BX
call	MEM_ASSIGN
xor	AX,AX
mov	mem_MyOwn,1
@@NOMEM:
neg	AX
pop	BX
retf	2
EVEN
MEM_ASSIGN_DOS ENDP

; Assign the caller segment and modulo-16-bit extent without validation; storage remains root-owned.
PUBLIC MEM_ASSIGN
EVEN
MEM_ASSIGN PROC FAR
push	BP
mov	BP,SP
top_seg  = MAINL_HEAP_ARG1
parasize = MAINL_HEAP_ARG0
mov	AX,[BP+top_seg]
mov	mem_TopSeg,AX
mov	mem_EndMark,AX
add	AX,[BP+parasize]
mov	mem_OutSeg,AX
mov	mem_TopHeap,AX
mov	mem_FirstHole,0
mov	mem_MyOwn,0
clc
pop	BP
retf	4
EVEN
MEM_ASSIGN ENDP

; Ask DOS for its largest extent, reserve only when strictly smaller, then assign the second allocation.
PUBLIC MEM_ASSIGN_ALL
EVEN
MEM_ASSIGN_ALL PROC FAR
push	BX
mov	BX,-1
mov	AH,48h
int	21h
mov     AX,mem_Reserve
cmp     BX,AX
jbe     short ALL_ALLOC
sub     BX,AX
ALL_ALLOC:
mov	AH,48h
int	21h
jc	short NOMEM
push	AX
push	AX
push	BX
call	MEM_ASSIGN
mov	mem_MyOwn,1
pop	AX
NOMEM:
pop	BX
retf
EVEN
MEM_ASSIGN_ALL ENDP
MEMHEAD STRUC
using	dw	?
nextseg	dw	?
mem_id	dw	?
MEMHEAD	ENDS

; Carry-aware 17-bit ceil(bytes/16); share the allocation entry after its argument load.
PUBLIC HMEM_ALLOCBYTE
EVEN
HMEM_ALLOCBYTE PROC FAR
push	BX
mov	BX,SP
bytesize = MAINL_HEAP_ARG0
mov	BX,SS:[BX+bytesize]
add	BX,15
rcr	BX,1
shr	BX,1
shr	BX,1
shr	BX,1
jmp	short hmem_allocb
EVEN
HMEM_ALLOCBYTE ENDP

; Lazy DOS initialization, first-hole search/split, then downward central allocation. Transfer and clear AllocID.
PUBLIC HMEM_ALLOC
EVEN
HMEM_ALLOC PROC FAR
push	BX
mov	BX,SP
parasize = MAINL_HEAP_ARG0
mov	BX,SS:[BX+parasize]
hmem_allocb:
cmp	mem_TopSeg,0
jne	short A_S
call	MEM_ASSIGN_ALL
A_S:
push	CX
push	ES
test	BX,BX
jz	short NO_MEMORY
mov	AX,mem_OutSeg
sub	AX,mem_EndMark
cmp	BX,AX
jae	short NO_MEMORY
inc	BX
mov	AX,mem_FirstHole
test	AX,AX
jz	short ALLOC_CENTER
SEARCH_HOLE_S:
mov	CX,mem_OutSeg
SEARCH_HOLE:
mov	ES,AX
mov	AX,ES:[MEMHEAD.nextseg]
cmp	ES:[MEMHEAD.using],0
jne	short SEARCH_HOLE_E
mov	CX,ES
add	CX,BX
jc	short SEARCH_HOLE_E0
cmp	CX,AX
jbe	short FOUND_HOLE
SEARCH_HOLE_E0:
mov	CX,mem_OutSeg
SEARCH_HOLE_E:
cmp	AX,CX
jne	short SEARCH_HOLE
ALLOC_CENTER:
mov	AX,mem_TopHeap
mov	CX,AX
sub	AX,BX
jc	short NO_MEMORY
cmp	AX,mem_EndMark
jb	short NO_MEMORY
mov	mem_TopHeap,AX
mov	ES,AX
mov	ES:[MEMHEAD.nextseg],CX
mov	ES:[MEMHEAD.using],1
mov	BX,AX
jmp	short RETURN
NO_MEMORY:
mov	AX,0
mov	mem_AllocID,AX
stc
pop	ES
pop	CX
pop	BX
retf	2
FOUND_HOLE:
sub	AX,CX
cmp	AX,1
jbe	short JUST_FIT
add	AX,CX
mov	ES:[MEMHEAD.using],1
mov	ES:[MEMHEAD.nextseg],CX
mov	BX,ES
mov	ES,CX
mov	ES:[MEMHEAD.nextseg],AX
mov	ES:[MEMHEAD.using],0
cmp	BX,mem_FirstHole
jne	short RETURN
mov	mem_FirstHole,CX
jmp	short RETURN
JUST_FIT:
mov	ES:[MEMHEAD.using],1
mov	BX,ES
cmp	BX,mem_FirstHole
jne	short RETURN
mov	AX,mem_OutSeg
mov	CX,BX
push	BX
SEARCH_NEXT_HOLE:
les	CX,ES:[0]
jcxz	short FOUND_NEXT_HOLE
mov	BX,ES
cmp	BX,AX
jb	short SEARCH_NEXT_HOLE
xor	BX,BX
FOUND_NEXT_HOLE:
mov	mem_FirstHole,BX
pop	BX
RETURN:	mov	ES,BX
mov	AX,0
xchg	AX,mem_AllocID
mov	ES:[MEMHEAD.mem_id],AX
lea	AX,[BX+1]
clc
NO_THANKYOU:
pop	ES
pop	CX
pop	BX
retf	2
EVEN
HMEM_ALLOC ENDP

; Release/coalesce a header without an upper-bound check. Invalid inputs share the allocation epilogue.
PUBLIC HMEM_FREE
EVEN
HMEM_FREE PROC FAR
push	BX
mov	BX,SP
push	CX
push	ES
memseg = MAINL_HEAP_ARG0
mov	BX,SS:[BX+memseg]
dec	BX
mov	ES,BX
cmp	BX,mem_TopHeap
je	short EXPAND_CENTER
jb	short NO_THANKYOU
xor	BX,BX
cmp	ES:[BX].MEMHEAD.using,1
jne	short NO_THANKYOU
mov	ES:[BX].MEMHEAD.using,BX
mov	CX,mem_FirstHole
mov	AX,ES
mov	mem_FirstHole,AX
jcxz	short FREE_RETURN
cmp	AX,CX
jb	short CONNECT_START
mov	AX,CX
mov	mem_FirstHole,AX
CONNECT_START:
mov	CX,AX
mov	AX,ES:[BX].MEMHEAD.nextseg
cmp	AX,mem_OutSeg
jne	short NO_TAIL
mov	AX,ES
NO_TAIL:
push	DS
CONNECT_FREE:
mov	DS,CX
mov	CX,[BX].MEMHEAD.nextseg
cmp	CX,AX
ja	short CONNECT_SKIP_OVER
cmp	[BX].MEMHEAD.using,BX
jne	short CONNECT_FREE
CONNECT_FREE2:
mov	ES,CX
cmp	ES:[BX].MEMHEAD.using,BX
jne	short CONNECT_FREE
mov	CX,ES:[BX].MEMHEAD.nextseg
mov	[BX].MEMHEAD.nextseg,CX
cmp	CX,AX
jbe	short CONNECT_FREE2
CONNECT_SKIP_OVER:
pop	DS
jmp	short FREE_RETURN
EVEN
EXPAND_CENTER:
xor	BX,BX
mov	AX,ES:[BX].MEMHEAD.nextseg
mov	mem_TopHeap,AX
cmp	AX,mem_OutSeg
je	short FREE_RETURN
mov	ES,AX
cmp	ES:[BX].MEMHEAD.using,BX
jne	short FREE_RETURN
mov	AX,ES:[BX].MEMHEAD.nextseg
mov	mem_TopHeap,AX
mov	CX,mem_OutSeg
cmp	AX,CX
je	short FREE_LOST_HOLE
jmp	short X_SEARCH_HOLE
EVEN
X_SEARCH_NEXT_HOLE:
mov	AX,ES:[BX].MEMHEAD.nextseg
cmp	AX,CX
je	short FREE_LOST_HOLE
X_SEARCH_HOLE:
mov	ES,AX
cmp	ES:[BX].MEMHEAD.using,BX
jne	short X_SEARCH_NEXT_HOLE
mov	BX,ES
FREE_LOST_HOLE:
mov	mem_FirstHole,BX
FREE_RETURN:
clc
pop	ES
pop	CX
pop	BX
retf	2
EVEN
HMEM_FREE ENDP

; GAME=3 removes management even with live allocations. Keep the emitted unreachable failure return.
PUBLIC MEM_UNASSIGN
EVEN
MEM_UNASSIGN PROC FAR
cmp	mem_TopSeg,0
je	short @@SUCCESS
mov	AX,mem_TopSeg
mov	ES,AX
xor	AX,AX
cmp	mem_MyOwn,AX
mov	mem_TopSeg,AX
je	short @@SUCCESS
mov	AH,49h
int	21h
@@SUCCESS:
mov	AX,1
retf
@@FAILURE:
xor	AX,AX
stc
retf
EVEN
MEM_UNASSIGN ENDP
