; SCOPED, INCOMPLETE SOURCE: Borland isteldbl long-double parser CODE+0..459.
; Covers ipfx, sign, streambuf refill, EOF, zero x87 initialization and
; integer digit accumulation. Never link as a complete CRT member.
 ; parser_eof is a genuinely UNRECOVERED near label outside the prefix,
; intentionally left as symbolic unresolved external. The original near
; displacement bytes cannot be claimed equal in this bounded object.
; fractional_start is the exact next original instruction after this prefix.
.8086
.8087
EMUL
extrn @ios@setstate$qi:far
extrn @streambuf@do_snextc$qv:far
extrn @istream@ipfx$qi:far
extrn __ctype:byte
extrn __huge_dble:qword
extrn __huge_ldble:tbyte
extrn _errno:word
extrn F_LXMUL@:far
extrn FIDRQQ:far
extrn FIERQQ:far
extrn FIWRQQ:far
extrn __turboFloat:byte
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
extrn parser_eof:near
public @istream@$brsh$qmg
@istream@$brsh$qmg proc far
    push bp
    mov bp,sp
    sub sp,2ah
    push si
    push di
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @istream@ipfx$qi
    add sp,6
    or ax,ax
    jne short parser_begin
    jmp parser_eof
parser_begin:
    mov word ptr [bp-16h],0
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-4],es
    mov [bp-6],bx
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+1eh]
    les bx,dword ptr [bp-6]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+22h]
    jb short first_buffered_char
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-8],es
    mov [bp-0ah],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,dword ptr es:[bx+2]
    mov bx,word ptr es:[bx]
    call dword ptr [bx+0ch]
    pop cx
    pop cx
    jmp short first_have_char
first_buffered_char:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    les bx,dword ptr es:[bx+1eh]
    mov al,byte ptr es:[bx]
    mov ah,0
first_have_char:
    mov [bp-0ch],ax
    cmp word ptr [bp-0ch],2dh
    jne short first_not_minus
    mov ax,1
    jmp short first_sign_ready
first_not_minus:
    xor ax,ax
first_sign_ready:
    mov [bp-0eh],ax
    cmp word ptr [bp-0ch],2bh
    je short consume_sign
    cmp word ptr [bp-0eh],0
    je short signed_char_ready
consume_sign:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+1eh]
    or ax,word ptr es:[bx+20h]
    je short sign_refill
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    inc word ptr es:[bx+1eh]
    mov ax,word ptr es:[bx+1eh]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+22h]
    jb short sign_from_buffer
sign_refill:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short sign_char_ready
sign_from_buffer:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    les bx,dword ptr es:[bx+1eh]
    mov al,byte ptr es:[bx]
    mov ah,0
sign_char_ready:
    mov [bp-0ch],ax
    jmp short parse_init
signed_char_ready:
    cmp word ptr [bp-0ch],-1
    jne short parse_init
    mov ax,4
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp,6
parse_init:
    les bx,dword ptr [bp+0ah]
    fldz
    fstp tbyte ptr es:[bx]
    fwait
    mov bx,[bp-0ch]
    test byte ptr DGROUP:__ctype[bx+1],2
    jne short first_digit
    jmp near ptr fractional_start
first_digit:
    mov word ptr [bp-16h],1
digit_loop:
    sub word ptr [bp-0ch],30h
    les bx,dword ptr [bp+0ah]
    fld tbyte ptr es:[bx]
    fmul dword ptr DGROUP:digit_ten
    mov ax,[bp-0ch]
    mov [bp-2],ax
    fild word ptr [bp-2]
    faddp st(1),st(0)
    les bx,dword ptr [bp+0ah]
    fstp tbyte ptr es:[bx]
    fwait
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+1eh]
    or ax,word ptr es:[bx+20h]
    je short digit_refill
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    inc word ptr es:[bx+1eh]
    mov ax,word ptr es:[bx+1eh]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+22h]
    jb short digit_from_buffer
digit_refill:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call @streambuf@do_snextc$qv
    pop cx
    pop cx
    jmp short digit_char_ready
digit_from_buffer:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    les bx,dword ptr es:[bx+1eh]
    mov al,byte ptr es:[bx]
    mov ah,0
digit_char_ready:
    mov [bp-0ch],ax
    mov bx,[bp-0ch]
    test byte ptr DGROUP:__ctype[bx+1],2
    je short fractional_start
    jmp near ptr digit_loop
fractional_start label near
@istream@$brsh$qmg endp
_TEXTA ends
_DATA segment word public 'DATA'
digit_ten dd 10.0
_DATA ends
end
