; Typed Borland class RTTI for one derived exception and its xmsg base.
; Each invocation belongs to its enclosing native TU's _TEXTC segment.
; STRING_BODY_SIZE excludes these inline descriptors. name_bytes includes
; the original two terminators; this is metadata, never executable padding.
STRING_THROW_RTTI macro object_size,type_name,name_bytes
org STRING_BODY_SIZE+38+name_bytes+20+30
    dd @xmsg@$bdtr$qv
    dw 5,52
    db 'xmsg',0,0
    dw 0,0,0,0,0,0 ; reserved class control fields

org STRING_BODY_SIZE+38+name_bytes
rtti_throw_base:
    dd rtti_xmsg
    dw 0,3
    dw 0,0,0,0,0,0
rtti_xmsg:
    dw 4,3,38,-1,3,44,48
    dw 0,0,0,0,0,0
    dw 1,1

org STRING_BODY_SIZE+30
    dd xmsg_cleanup
    dw 5,54+name_bytes
    db type_name,0,0

org STRING_BODY_SIZE
rtti_throw:
    dw object_size,3,38,-1,7,38+name_bytes,50+name_bytes
    dw 0,0,0,0,0,0
    dw 2,2
endm
