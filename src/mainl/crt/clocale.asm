; Complete original Japanese CRT clocale DATA/metadata owner.
.8086
include locale_fields.inc
extrn _strcmp:far
extrn _strxfrm:far
extrn __ctype:byte
extrn __lower:byte
extrn __upper:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
public __Clocale,__LocaleCatNames,__pLocale,__LocaleLibName
; Fixed-capacity original locale strings; unused characters initialize to NUL.
LOCALE_TEXT macro field_name,capacity,text_value
field_name db text_value
db capacity-($-field_name) dup (0)
endm
; Pointer chunks follow original BCC field chronology; every other byte has a field owner.
org LOCALE_STRXFRM
dd _strxfrm
org LOCALE_STRCOLL
dd _strcmp
org 346
dd DGROUP:__upper
org 342
dd DGROUP:__lower
org 338
dd DGROUP:__ctype
org 2491
__pLocale dd DGROUP:__Clocale
org 2487
dd DGROUP:category_name_7
org 2483
dd DGROUP:category_name_6
org 2479
dd DGROUP:category_name_5
org 2475
dd DGROUP:category_name_4
org 2471
dd DGROUP:category_name_3
org 2467
dd DGROUP:category_name_2
org 2463
dd DGROUP:category_name_1
org 2459
__LocaleCatNames label dword
dd DGROUP:category_name_0
org 0
__Clocale label byte
LOCALE_TEXT c_locale_name_slot,32,<'C'>
locale_header_words dw 1,0
locale_dynamic_owner dw 0
locale_format_words dw 1,0
locale_format_versions db 1,1
locale_category_count dw 6
locale_header_status dw 0
locale_category_mask dw 3fh
locale_category_offsets dd 7 dup (0)
LOCALE_TEXT locale_all_names,224,<'C;C;C;C;C;C;;'>
ctype_format_word dw 424h
LOCALE_TEXT ctype_name,32,<'C'>
ctype_status dw 0
org 350
collation_format_word dw 0
LOCALE_TEXT collation_name,32,<'C'>
collation_state db 32 dup (0)
org 424
monetary_format_word dw 4ch
LOCALE_TEXT monetary_name,32,<'C'>
monetary_status dw 0
LOCALE_TEXT international_currency,5,<0>
LOCALE_TEXT currency_symbol,5,<0>
LOCALE_TEXT monetary_decimal_point,2,<0>
LOCALE_TEXT monetary_thousands_separator,5,<0>
LOCALE_TEXT monetary_grouping,5,<0>
LOCALE_TEXT positive_sign,5,<0>
LOCALE_TEXT negative_sign,5,<0>
monetary_numeric_flags db 8 dup (7fh)
numeric_format_word dw 44h
LOCALE_TEXT numeric_name,32,<'C'>
numeric_status dw 0
LOCALE_TEXT decimal_point,2,<'.'>
LOCALE_TEXT thousands_separator,10,<0>
LOCALE_TEXT digit_grouping,20,<0>
time_format_word dw 709h
LOCALE_TEXT time_name,32,<'C'>
time_status dw 0
LOCALE_TEXT weekday_abbreviation_0,10,<'Sun'>
LOCALE_TEXT weekday_abbreviation_1,10,<'Mon'>
LOCALE_TEXT weekday_abbreviation_2,10,<'Tue'>
LOCALE_TEXT weekday_abbreviation_3,10,<'Wed'>
LOCALE_TEXT weekday_abbreviation_4,10,<'Thu'>
LOCALE_TEXT weekday_abbreviation_5,10,<'Fri'>
LOCALE_TEXT weekday_abbreviation_6,10,<'Sat'>
LOCALE_TEXT weekday_name_0,20,<'Sunday'>
LOCALE_TEXT weekday_name_1,20,<'Monday'>
LOCALE_TEXT weekday_name_2,20,<'Tuesday'>
LOCALE_TEXT weekday_name_3,20,<'Wednesday'>
LOCALE_TEXT weekday_name_4,20,<'Thursday'>
LOCALE_TEXT weekday_name_5,20,<'Friday'>
LOCALE_TEXT weekday_name_6,20,<'Saturday'>
LOCALE_TEXT month_abbreviation_0,10,<'Jan'>
LOCALE_TEXT month_abbreviation_1,10,<'Feb'>
LOCALE_TEXT month_abbreviation_2,10,<'Mar'>
LOCALE_TEXT month_abbreviation_3,10,<'Apr'>
LOCALE_TEXT month_abbreviation_4,10,<'May'>
LOCALE_TEXT month_abbreviation_5,10,<'Jun'>
LOCALE_TEXT month_abbreviation_6,10,<'Jul'>
LOCALE_TEXT month_abbreviation_7,10,<'Aug'>
LOCALE_TEXT month_abbreviation_8,10,<'Sep'>
LOCALE_TEXT month_abbreviation_9,10,<'Oct'>
LOCALE_TEXT month_abbreviation_10,10,<'Nov'>
LOCALE_TEXT month_abbreviation_11,10,<'Dec'>
LOCALE_TEXT month_name_0,20,<'January'>
LOCALE_TEXT month_name_1,20,<'February'>
LOCALE_TEXT month_name_2,20,<'March'>
LOCALE_TEXT month_name_3,20,<'April'>
LOCALE_TEXT month_name_4,20,<'May'>
LOCALE_TEXT month_name_5,20,<'June'>
LOCALE_TEXT month_name_6,20,<'July'>
LOCALE_TEXT month_name_7,20,<'August'>
LOCALE_TEXT month_name_8,20,<'September'>
LOCALE_TEXT month_name_9,20,<'October'>
LOCALE_TEXT month_name_10,20,<'November'>
LOCALE_TEXT month_name_11,20,<'December'>
LOCALE_TEXT day_period_0,10,<'AM'>
LOCALE_TEXT day_period_1,10,<'PM'>
LOCALE_TEXT date_time_format_0,25,<'%a %b %d %X %Y'>
LOCALE_TEXT date_time_format_1,25,<'%a %b %d'>
LOCALE_TEXT date_time_format_2,25,<'%H:%M:%S'>
LOCALE_TEXT date_time_format_3,25,<'%I:%M:%S %p'>
LOCALE_TEXT time_extended_format_0,25,<' '>
LOCALE_TEXT time_extended_format_1,25,<' '>
LOCALE_TEXT time_extended_format_2,25,<' '>
; Fixed serialized LC_TIME extension, copied as part of the original 709h-byte category.
time_extension db 1000 dup (0)
messages_format_word dw 2eh
LOCALE_TEXT messages_name,32,<'C'>
messages_status dw 0
LOCALE_TEXT yes_response,5,<'y'>
LOCALE_TEXT no_response,5,<'n'>
user_format_word dw 2eh
LOCALE_TEXT user_name,32,<0>
user_status dw 0
c_locale_user_buffer_pointer dd 0
locale_user_context dd 0
org 2495
LOCALE_TEXT __LocaleLibName,81,<'LOCALE.BLL'>
category_name_0 db 'LC_ALL',0
category_name_1 db 'LC_COLLATE',0
category_name_2 db 'LC_CTYPE',0
category_name_3 db 'LC_MONETARY',0
category_name_4 db 'LC_NUMERIC',0
category_name_5 db 'LC_TIME',0
category_name_6 db 'LC_MESSAGES',0
category_name_7 db 'LC_userdef',0
_DATA ends
end
