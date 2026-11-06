; Semantic DATA declarations; source/ABI roles retained from libs/master.lib/grp[data].asm.
	public _graph_VramSeg,graph_VramSeg
graph_VramSeg label word
_graph_VramSeg	dw 0a800h
	public _graph_VramWords,graph_VramWords
graph_VramWords label word
_graph_VramWords	dw 16000
	public _graph_VramLines,graph_VramLines
graph_VramLines label word
_graph_VramLines	dw 400
	public _graph_VramWidth,graph_VramWidth
graph_VramWidth label word
_graph_VramWidth	dw 80
	public _graph_VramZoom,graph_VramZoom
graph_VramZoom label word
_graph_VramZoom	dw 0
	public _graph_MeshByte,graph_MeshByte
graph_MeshByte label word
_graph_MeshByte	db 55h
	; Original master.lib GRP storage initializes its following word-alignment byte.
	; This byte is alignment, not source function or independent DATA-owner credit.
	db 0
