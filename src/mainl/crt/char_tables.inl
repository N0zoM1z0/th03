; Original 8-bit classification/folding rules; expands only into DATA owners.
C_SPACE equ 1
C_DIGIT equ 2
C_UPPER equ 4
C_LOWER equ 8
C_HEX equ 16
C_CONTROL equ 32
C_PUNCT equ 64
C_BLANK equ 128
MB_KALPHA equ 1
MB_KPUNCT equ 2
MB_LEAD equ 4
MB_TRAIL equ 8

CRT_CASE_MAP macro lower_case
character_value = 0
rept 256
if lower_case
 if (character_value ge 'A') and (character_value le 'Z')
  db character_value+'a'-'A'
 else
  db character_value
 endif
else
 if (character_value ge 'a') and (character_value le 'z')
  db character_value-'a'+'A'
 else
  db character_value
 endif
endif
character_value = character_value+1
endm
endm

CRT_CTYPE_TABLE macro
    db 0 ; EOF sentinel
character_value = 0
rept 256
class_flags = 0
if (character_value lt 20h) or (character_value eq 7fh)
class_flags = class_flags or C_CONTROL
endif
if ((character_value ge 9) and (character_value le 13)) or (character_value eq 20h)
class_flags = class_flags or C_SPACE
endif
if character_value eq 20h
class_flags = class_flags or C_BLANK
endif
if (character_value ge '0') and (character_value le '9')
class_flags = class_flags or C_DIGIT or C_HEX
endif
if (character_value ge 'A') and (character_value le 'Z')
class_flags = class_flags or C_UPPER
endif
if (character_value ge 'a') and (character_value le 'z')
class_flags = class_flags or C_LOWER
endif
if ((character_value ge 'A') and (character_value le 'F')) or ((character_value ge 'a') and (character_value le 'f'))
class_flags = class_flags or C_HEX
endif
if ((character_value ge 21h) and (character_value le 2fh)) or ((character_value ge 3ah) and (character_value le 40h)) or ((character_value ge 5bh) and (character_value le 60h)) or ((character_value ge 7bh) and (character_value le 7eh))
class_flags = class_flags or C_PUNCT
endif
    db class_flags
character_value = character_value+1
endm
endm

CRT_MBCTYPE_TABLE macro
    db 0 ; EOF sentinel
character_value = 0
rept 256
class_flags = 0
if (character_value ge 40h) and (character_value le 0fch) and (character_value ne 7fh)
class_flags = class_flags or MB_TRAIL
endif
if ((character_value ge 81h) and (character_value le 9fh)) or ((character_value ge 0e0h) and (character_value le 0fch))
class_flags = class_flags or MB_LEAD
endif
if (character_value ge 0a1h) and (character_value le 0a5h)
class_flags = class_flags or MB_KPUNCT
endif
if (character_value ge 0a6h) and (character_value le 0dfh)
class_flags = class_flags or MB_KALPHA
endif
    db class_flags
character_value = character_value+1
endm
endm
