"""Restore genuine FAR CALL producer policy uniformly, never emit padding."""
import hashlib
INPUT_SHA='62ecdf5ac2486f3e8f3134254f85caec436e8b207195781f8f72be9053058246'
OLD=b'nopcall macro func\r\nif LDATA\r\n\tnop\t; PC-98 Touhou compatibility\r\nendif\r\n\tcall func\r\nendm'
NEW=b'nopcall macro func\r\nif LDATA\r\n\tnosmart\r\n\tcall far ptr func\r\n\tsmart\r\nelse\r\n\tcall func\r\nendif\r\nendm'
def compose(raw):
 if hashlib.sha256(raw).hexdigest()!=INPUT_SHA or raw.count(OLD)!=1:raise ValueError('exact OPVA181 ReC98.inc source required')
 return {'ReC98.inc':raw.replace(OLD,NEW)}
