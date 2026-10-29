; End joystick use by invoking the original keyboard-buffer clear API.
func JS_END
	call DOS_KEYCLEAR
	ret
endfunc
