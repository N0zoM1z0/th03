; Semantic DATA declarations; source/ABI roles retained from libs/master.lib/tx[data].asm.
	public _TextVramAdr,TextVramAdr
	public _TextVramSeg,TextVramSeg
	public _TextVramWidth,TextVramWidth
	public _TextShown,TextShown
TextVramAdr label dword
_TextVramAdr label dword
	    dw 0
TextVramSeg label word
_TextVramSeg dw 0a000h
TextVramWidth label word
_TextVramWidth dw 80
TextShown label word
_TextShown dw 1
