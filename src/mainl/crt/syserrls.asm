; Complete original Japanese CRT syserrls DATA/metadata owner.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
public __sys_errlist
__sys_errlist label byte
; Forty-eight FAR pointers retain original descending field chronology.
org 188
dd DGROUP:errno_text_47
org 184
dd DGROUP:errno_text_46
org 180
dd DGROUP:errno_text_45
org 176
dd DGROUP:errno_text_44
org 172
dd DGROUP:errno_text_43
org 168
dd DGROUP:errno_text_42
org 164
dd DGROUP:errno_text_41
org 160
dd DGROUP:errno_text_40
org 156
dd DGROUP:errno_text_39
org 152
dd DGROUP:errno_text_38
org 148
dd DGROUP:errno_text_37
org 144
dd DGROUP:errno_text_36
org 140
dd DGROUP:errno_text_35
org 136
dd DGROUP:errno_text_34
org 132
dd DGROUP:errno_text_33
org 128
dd DGROUP:errno_text_32
org 124
dd DGROUP:errno_text_31
org 120
dd DGROUP:errno_text_30
org 116
dd DGROUP:errno_text_29
org 112
dd DGROUP:errno_text_28
org 108
dd DGROUP:errno_text_27
org 104
dd DGROUP:errno_text_26
org 100
dd DGROUP:errno_text_25
org 96
dd DGROUP:errno_text_24
org 92
dd DGROUP:errno_text_23
org 88
dd DGROUP:errno_text_22
org 84
dd DGROUP:errno_text_21
org 80
dd DGROUP:errno_text_20
org 76
dd DGROUP:errno_text_19
org 72
dd DGROUP:errno_text_18
org 68
dd DGROUP:errno_text_17
org 64
dd DGROUP:errno_text_16
org 60
dd DGROUP:errno_text_15
org 56
dd DGROUP:errno_text_14
org 52
dd DGROUP:errno_text_13
org 48
dd DGROUP:errno_text_12
org 44
dd DGROUP:errno_text_11
org 40
dd DGROUP:errno_text_10
org 36
dd DGROUP:errno_text_9
org 32
dd DGROUP:errno_text_8
org 28
dd DGROUP:errno_text_7
org 24
dd DGROUP:errno_text_6
org 20
dd DGROUP:errno_text_5
org 16
dd DGROUP:errno_text_4
org 12
dd DGROUP:errno_text_3
org 8
dd DGROUP:errno_text_2
org 4
dd DGROUP:errno_text_1
org 0
dd DGROUP:errno_text_0
org 192
errno_text_0 db 'Error 0',0
errno_text_1 db 'Invalid function number',0
errno_text_2 db 'No such file or directory',0
errno_text_3 db 'Path not found',0
errno_text_4 db 'Too many open files',0
errno_text_5 db 'Permission denied',0
errno_text_6 db 'Bad file number',0
errno_text_7 db 'Memory arena trashed',0
errno_text_8 db 'Not enough memory',0
errno_text_9 db 'Invalid memory block address',0
errno_text_10 db 'Invalid environment',0
errno_text_11 db 'Invalid format',0
errno_text_12 db 'Invalid access code',0
errno_text_13 db 'Invalid data',0
errno_text_14 db 0
errno_text_15 db 'No such device',0
errno_text_16 db 'Attempted to remove current directory',0
errno_text_17 db 'Not same device',0
errno_text_18 db 'No more files',0
errno_text_19 db 'Invalid argument',0
errno_text_20 db 'Arg list too big',0
errno_text_21 db 'Exec format error',0
errno_text_22 db 'Cross-device link',0
errno_text_23 db 0
errno_text_24 db 0
errno_text_25 db 0
errno_text_26 db 0
errno_text_27 db 0
errno_text_28 db 0
errno_text_29 db 0
errno_text_30 db 0
errno_text_31 db 0
errno_text_32 db 0
errno_text_33 db 'Math argument',0
errno_text_34 db 'Result too large',0
errno_text_35 db 'File already exists',0
errno_text_36 db 'Possible deadlock',0
errno_text_37 db 0
errno_text_38 db 0
errno_text_39 db 0
errno_text_40 db 0
errno_text_41 db 0
errno_text_42 db 0
errno_text_43 db 0
errno_text_44 db 0
errno_text_45 db 0
errno_text_46 db 0
errno_text_47 db 0
_DATA ends
end
