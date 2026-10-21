"""Opt-in hybrid driver source stage: all fifty-five maintained procedures, retained remainder.

This is NOT a maintained whole-driver build or default integration. Reference
scaffold and two includes stay explicitly pinned diagnostic inputs. No target
bytes, object reuse, compiler execution, padding synthesis or acceptance changes.
"""
from pathlib import Path
import argparse,hashlib,json,re,stat
ROOT=Path(__file__).resolve().parents[1]
REFERENCE='_reference/ReC98/libs/sprite16/sprite16.asm'
REFERENCE_SHA='d0b5366a317911fcd45b6d8e9abb80331ed999a73110cd8090fac98a26b0739d'
SERVICES='src/zun/driver_services.inl'
RESIDENT='src/zun/driver_resident.inl'
RESIDENT_PROCS=(('sub_10C', 'sprite16_entry', 268, 412),
 ('sub_19C', 'sprite16_allocate_buffers', 412, 471),
 ('sub_1D7', 'sprite16_set_interrupt_argument', 471, 478),
 ('sub_1DE', 'sprite16_mask_test_command', 478, 513),
 ('sub_201', 'sprite16_draw_command', 513, 554),
 ('sub_22A', 'sprite16_interrupt_dispatch', 554, 579),
 ('sub_243', 'sprite16_install', 579, 685),
 ('sub_2AD', 'sprite16_uninstall', 685, 832))
RESIDENT_SYMBOLS={'aSprite16':'sprite16_signature','aHeader':'sprite16_banner','aUsage':'sprite16_usage','word_F40': 'sprite16_int40_signature_found',
 'word_F43': 'sprite16_resident_paragraphs',
 'word_F38': 'sprite16_previous_vector_segment',
 'word_F3A': 'sprite16_previous_vector_offset',
 'word_F3C': 'sprite16_mask_buffer_segment',
 'word_F3E': 'sprite16_solid_buffer_segment',
 'byte_F42': 'sprite16_interrupt_number',
 'word_F45': 'sprite16_dispatch_target',
 'word_1070': 'sprite16_argument_count',
 'off_103E': 'sprite16_service_table',
 'aGbgvgkpkpmvOFs': 'sprite16_resize_failed_message',
 'aGbgvgkvkslvsvV': 'sprite16_memory_failed_message',
 'aPatuvVVVBbInt0': 'sprite16_installed_message',
 'aVVVPatuvVVvvVB': 'sprite16_already_installed_message',
 'aKLlcIci': 'sprite16_environment_free_failed_message',
 'aGGxgngfbGCIci': 'sprite16_mask_free_failed_message',
 'aGxgGfbGCIci': 'sprite16_solid_free_failed_message',
 'aGrbGhcIci': 'sprite16_code_free_failed_message',
 'aI': 'sprite16_removed_message',
 'aPatuvVVvvVV': 'sprite16_not_installed_message',
 'loc_137': 'entry_no_int40_signature',
 'loc_13D': 'entry_resize_block',
 'loc_161': 'entry_parse_command_tail',
 'loc_186': 'entry_no_arguments',
 'loc_191': 'entry_optional_int40',
 'locret_19B': 'entry_return',
 'loc_1B0': 'allocate_solid_buffer',
 'loc_1CD': 'allocate_buffers_done',
 'loc_2A6': 'install_already_present',
 'locret_2AC': 'install_return',
 'loc_2FC': 'uninstall_free_mask',
 'loc_30F': 'uninstall_free_solid',
 'loc_322': 'uninstall_free_code',
 'loc_331': 'uninstall_removed',
 'loc_339': 'uninstall_not_present',
 'locret_33F': 'uninstall_return'}
COMMAND_GROUPS=(('src/zun/driver_command.inl',
  (('sub_920', 'sprite16_tokenize_command', 2336, 2434),
   ('sub_982', 'sprite16_skip_separators', 2434, 2457),
   ('sub_999', 'sprite16_find_token_end', 2457, 2485),
   ('sub_9B5', 'sprite16_find_quote_end', 2485, 2509),
   ('sub_9CD', 'sprite16_require_argument', 2509, 2543),
   ('sub_9EF', 'sprite16_optional_argument', 2543, 2570),
   ('sub_A0A', 'sprite16_require_number', 2570, 2596),
   ('sub_A24', 'sprite16_optional_number_legacy', 2596, 2614),
   ('sub_A36', 'sprite16_dispatch_options', 2614, 2697))),
 ('src/zun/driver_numbers.inl',
  (('sub_A90', 'sprite16_parse_number', 2704, 2821),
   ('sub_B05', 'sprite16_parse_decimal', 2821, 2891),
   ('sub_B4B', 'sprite16_parse_hex', 2891, 2933),
   ('sub_B75', 'sprite16_parse_binary', 2933, 2978),
   ('sub_BA2', 'sprite16_parse_switch', 2978, 3014))),
 ('src/zun/driver_strings.inl',
  (('sub_C40', 'sprite16_string_length', 3136, 3154),
   ('sub_C52', 'sprite16_string_equal_folded', 3154, 3190))))
COMMAND_SYMBOLS={'byte_1072': 'sprite16_argument_vector',
 'word_10F2': 'sprite16_argument_cursor',
 'off_101C': 'sprite16_option_table',
 'aSVVVsVkmivVivs': 'sprite16_missing_quote_message',
 'aI_0': 'sprite16_missing_argument_message',
 'aRftlvVCVvtlvko': 'sprite16_invalid_number_message',
 'aGigvgvgzguvkcM': 'sprite16_invalid_option_message',
 'aOn': 'sprite16_switch_on',
 'aOff': 'sprite16_switch_off',
 'loc_92F': 'tokenize_next',
 'loc_940': 'tokenize_terminate',
 'loc_945': 'tokenize_check_quote',
 'loc_964': 'tokenize_close_quote',
 'loc_96D': 'tokenize_plain',
 'loc_97B': 'tokenize_return',
 'loc_992': 'skip_separator',
 'locret_998': 'skip_separators_return',
 'loc_9AF': 'find_token_done',
 'loc_9B1': 'find_token_advance',
 'locret_9B4': 'find_token_return',
 'loc_9BE': 'find_quote_check_end',
 'loc_9C6': 'find_quote_missing',
 'loc_9C9': 'find_quote_advance',
 'locret_9CC': 'find_quote_return',
 'loc_9DF': 'require_argument_consume',
 'loc_9F9': 'optional_argument_consume',
 'locret_A09': 'optional_argument_return',
 'loc_A21': 'require_number_return',
 'loc_A33': 'optional_number_return',
 'loc_A3C': 'dispatch_option_next',
 'loc_A50': 'dispatch_option_consume',
 'loc_A5E': 'dispatch_option_begin',
 'loc_A61': 'dispatch_option_search',
 'loc_A71': 'dispatch_option_compare',
 'loc_A81': 'dispatch_option_advance',
 'loc_A86': 'dispatch_option_continue',
 'locret_A88': 'dispatch_option_return',
 'loc_AA8': 'parse_number_two_chars',
 'loc_AB6': 'parse_number_invalid_quote',
 'loc_ABB': 'parse_number_prefix',
 'loc_AC6': 'parse_number_suffix',
 'loc_AE6': 'parse_number_binary_suffix',
 'loc_AF9': 'parse_number_decimal_or_switch',
 'loc_B01': 'parse_number_return',
 'loc_B1B': 'parse_decimal_plus',
 'loc_B21': 'parse_decimal_digit',
 'loc_B30': 'parse_decimal_accumulate',
 'loc_B3E': 'parse_decimal_sign',
 'loc_B45': 'parse_decimal_success',
 'loc_B46': 'parse_decimal_return',
 'loc_B4F': 'parse_hex_digit',
 'loc_B5A': 'parse_hex_value',
 'loc_B66': 'parse_hex_accumulate',
 'loc_B6F': 'parse_hex_invalid',
 'loc_B70': 'parse_hex_return',
 'loc_B85': 'parse_binary_digit',
 'loc_B94': 'parse_binary_accumulate',
 'loc_B99': 'parse_binary_test_end',
 'loc_B9E': 'parse_binary_return',
 'loc_BC2': 'parse_switch_success',
 'loc_BC3': 'parse_switch_return',
 'loc_C47': 'string_length_next',
 'loc_C56': 'string_compare_next',
 'loc_C6F': 'string_compare_return'}
SCATTERED_GROUPS=(('src/zun/driver_graphics.inl',
  (('sub_364', 'sprite16_draw_clipped', 868, 1026),
   ('sub_402', 'sprite16_blit_egc', 1026, 1271),
   ('sub_4F8', 'sprite16_copy_rows', 1272, 1302),
   ('sub_520', 'sprite16_prepare_vram', 1312, 1344),
   ('sub_540', 'sprite16_build_mask', 1344, 1424),
   ('sub_590', 'sprite16_accumulate_plane', 1424, 1444),
   ('sub_5A4', 'sprite16_copy_lower_page', 1444, 1488),
   ('sub_5D0', 'sprite16_compress_rows', 1488, 1527),
   ('sub_5F7', 'sprite16_copy_upper_to_lower', 1527, 1552),
   ('sub_610', 'sprite16_clear_upper', 1552, 1585),
   ('sub_BD0', 'sprite16_egc_begin', 3024, 3088),
   ('sub_C10', 'sprite16_egc_end', 3088, 3132))),
 ('src/zun/driver_format.inl',
  (('sub_640', 'sprite16_format_print', 1600, 1632),
   ('sub_660', 'sprite16_print_string', 1632, 1654),
   ('sub_676', 'sprite16_print_stack_string', 1654, 1673),
   ('sub_689', 'sprite16_is_decimal_digit', 1673, 1684),
   ('sub_694', 'sprite16_is_ascii_lower', 1684, 1693),
   ('sub_69D', 'sprite16_ascii_upper', 1693, 1701),
   ('sub_6B0', 'sprite16_format_into', 1712, 2173),
   ('sub_87D', 'sprite16_pad_zeroes', 2173, 2179),
   ('sub_883', 'sprite16_pad_spaces', 2179, 2185),
   ('sub_889', 'sprite16_pad_field', 2185, 2199),
   ('sub_897', 'sprite16_append_string', 2199, 2207),
   ('sub_89F', 'sprite16_format_unsigned', 2207, 2268),
   ('sub_8EC', 'sprite16_reverse_string', 2284, 2332))))
SCATTERED_SYMBOLS={'word_1050': 'sprite16_bit_shift',
 'word_1052': 'sprite16_has_shift',
 'word_1054': 'sprite16_clipped_rows',
 'word_1056': 'sprite16_row_skip_bytes',
 'word_1058': 'sprite16_row_words',
 'word_105A': 'sprite16_draw_x',
 'word_105C': 'sprite16_draw_y',
 'word_105E': 'sprite16_draw_source_offset',
 'word_1060': 'sprite16_draw_width',
 'word_1062': 'sprite16_draw_height',
 'loc_3A1': 'draw_clip_top',
 'loc_3C1': 'draw_check_bottom',
 'loc_3CD': 'draw_clip_bottom',
 'loc_3EE': 'draw_apply_clipping',
 'loc_3F8': 'draw_restore',
 'loc_49C': 'draw_color_mode',
 'loc_4CB': 'draw_no_overlap',
 'loc_4DA': 'draw_color_copy',
 'loc_4EB': 'draw_copy_mask',
 'loc_508': 'copy_next_row',
 'loc_586': 'mask_invert_next',
 'loc_597': 'mask_accumulate_next',
 'loc_5B9': 'copy_page_next_word',
 'loc_5E4': 'compress_next_row',
 'var_D0': 'print_buffer',
 'arg_0': 'print_string_argument',
 'var_50': 'format_number_buffer',
 'var_18': 'format_lowercase',
 'var_14': 'format_radix',
 'var_10': 'format_zero_pad',
 'var_C': 'format_left_align',
 'var_8': 'format_output_length',
 'var_4': 'format_field_width',
 'loc_665': 'print_next_character',
 'loc_672': 'print_string_return',
 'loc_692': 'digit_not_decimal',
 'loc_69B': 'character_not_lower',
 'locret_6A4': 'uppercase_return',
 'loc_6BC': 'format_next',
 'loc_6E3': 'format_check_zero_pad',
 'loc_6EE': 'format_width_begin',
 'loc_6F4': 'format_width_digit',
 'loc_701': 'format_width_test',
 'loc_70B': 'format_check_unsigned',
 'loc_723': 'format_convert_number',
 'loc_74D': 'format_leading_spaces',
 'loc_750': 'format_append_number',
 'loc_75F': 'format_left_number',
 'loc_779': 'format_check_signed',
 'loc_796': 'format_signed_radix',
 'loc_7A3': 'format_check_lower_hex',
 'loc_7C3': 'format_check_upper_hex',
 'loc_7E3': 'format_check_binary',
 'loc_802': 'format_check_string',
 'loc_826': 'format_left_string',
 'loc_82C': 'format_string_restore',
 'loc_830': 'format_check_character',
 'loc_83F': 'format_check_newline',
 'loc_850': 'format_check_carriage',
 'loc_85E': 'format_check_tab',
 'loc_86C': 'format_literal',
 'loc_86D': 'format_test_end',
 'locret_896': 'padding_return',
 'loc_8AB': 'unsigned_next_digit',
 'loc_8C2': 'unsigned_store_digit',
 'a0123456789abcd': 'sprite16_hex_digits',
 'loc_904': 'reverse_swap',
 'loc_90C': 'reverse_test',
 'loc_915': 'reverse_return'}
SETTERS=(
 ('sub_340','sprite16_set_mono_enabled','word_1064','sprite16_mono_enabled'),
 ('sub_346','sprite16_set_mono_color','word_1066','sprite16_mono_color'),
 ('sub_34C','sprite16_set_overlap','word_1068','sprite16_overlap'),
 ('sub_352','sprite16_set_access_plane','word_106E','sprite16_access_plane'),
 ('sub_358','sprite16_set_rop','word_106A','sprite16_rop'),
 ('sub_35E','sprite16_set_mask','word_106C','sprite16_mask'),
)
INCLUDES=(
 ('_reference/ReC98/libs/master.lib/macros.inc','6e38bd2a6af911890250376d7e3d87343a6e726eced227958669d6f420427ae9','retained/master.inc'),
 ('_reference/ReC98/th01/hardware/egc.inc','29e30717870bb69635bf082114ccb4a0e9795803c80adbd1283449f80e32a188','retained/egc.inc'),
)
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def tokens(text):
 return [re.sub(r'\s+',' ',line.split(';',1)[0].strip()).lower() for line in text.splitlines() if line.split(';',1)[0].strip()]
def validate_services(text):
 expected=[]
 for _,name,_,field in SETTERS:expected += ['public '+name,name+' proc near','mov cs:'+field+', dx','retn',name+' endp']
 need(tokens(text)==expected,'six complete setter bodies/ABI differ')
def rename_symbols(text):
 for old,new,field,name in SETTERS:
  text=re.sub(r'\b'+old+r'\b',new,text,flags=re.I)
  text=re.sub(r'\b'+field+r'\b',name,text,flags=re.I)
 for old,new in [(a,b) for a,b,_,_ in RESIDENT_PROCS]+list(RESIDENT_SYMBOLS.items())+[(a,b) for _,group in COMMAND_GROUPS for a,b,_,_ in group]+list(COMMAND_SYMBOLS.items())+[(a,b) for _,group in SCATTERED_GROUPS for a,b,_,_ in group]+list(SCATTERED_SYMBOLS.items()):
  text=re.sub(r'\b'+old+r'\b',new,text,flags=re.I)
 return text
def compose(reference,services):
 """Replace only six complete procedures; rename their true references/state."""
 validate_services(services)
 spans=[]
 for old,name,field,state in SETTERS:
  pattern=r'(?im)^'+old+r'\s+proc near\b.*?^'+old+r'\s+endp\b[^\n]*'
  found=list(re.finditer(pattern,reference,flags=re.S))
  need(len(found)==1,'unique retained procedure '+old)
  match=found[0]
  need(tokens(match.group())==[old.lower()+' proc near','mov cs:'+field.lower()+', dx','retn',old.lower()+' endp'],'retained setter body differs')
  spans.append(match.span())
 need(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),'setter order/overlap')
 for a,b in zip(spans,spans[1:]):need(not tokens(reference[a[1]:b[0]]),'unowned code/data between setters')
 first,last=spans[0][0],spans[-1][1]
 composed=reference[:first]+'include src\\zun\\driver_services.inl'+reference[last:]
 return rename_symbols(composed)
def compose_resident(reference,resident):
 """Consume all eight complete procedures, preserving unowned gaps and data."""
 spans=[];expected=[]
 for old,name,start,end in RESIDENT_PROCS:
  found=list(re.finditer(r'(?im)^'+old+r'\s+proc (?:near|far)\b.*?^'+old+r'\s+endp\b[^\n]*',reference,flags=re.S))
  need(len(found)==1,'unique resident procedure '+old)
  match=found[0];spans.append(match.span())
  expected+=['public '+name]+tokens(rename_symbols(match.group()))
 need(tokens(resident)==expected,'resident procedure instruction/ABI contract differs')
 need(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),'resident order/overlap')
 for a,b in zip(spans,spans[1:]):need(not tokens(reference[a[1]:b[0]]),'unowned code/data between resident procedures')
 first,last=spans[0][0],spans[-1][1]
 return reference[:first]+'include src\\zun\\driver_resident.inl'+reference[last:]
def compose_command_group(reference,owned,path,procedures):
 """Replace one contiguous code group only; all following zero gaps stay retained."""
 spans=[];expected=[]
 for old,name,start,end in procedures:
  found=list(re.finditer(r'(?im)^'+old+r'\s+proc near\b.*?^'+old+r'\s+endp\b[^\n]*',reference,flags=re.S))
  need(len(found)==1,'unique command procedure '+old)
  match=found[0];spans.append(match.span());expected+=['public '+name]+tokens(rename_symbols(match.group()))
 need(tokens(owned)==expected,'command procedure instruction/ABI contract differs')
 need(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),'command order/overlap')
 for a,b in zip(spans,spans[1:]):need(not tokens(reference[a[1]:b[0]]),'unowned code/data between command procedures')
 first,last=spans[0][0],spans[-1][1]
 return reference[:first]+'include '+path.replace('/','\\')+reference[last:]
def compose_scattered(reference,owned,procedures):
 """Place actual maintained procedure source, never surrounding retained data/gaps."""
 replacements=[];expected=[]
 for old,name,start,end in procedures:
  pattern=lambda n:r'(?im)^'+n+r'\s+proc near\b.*?^'+n+r'\s+endp\b[^\n]*'
  retained=list(re.finditer(pattern(old),reference,flags=re.S))
  maintained=list(re.finditer(pattern(name),owned,flags=re.S))
  need(len(retained)==len(maintained)==1,'unique scattered procedure '+name)
  original=retained[0];body=maintained[0].group()
  expected+=['public '+name]+tokens(rename_symbols(original.group()))
  replacements.append((original.start(),original.end(),'public '+name+'\n'+body))
 need(tokens(owned)==expected,'scattered complete instruction/ABI contract differs')
 for start,end,body in sorted(replacements,reverse=True):reference=reference[:start]+body+reference[end:]
 return reference
def dos_text(text):
 text=text.replace('\r\n','\n')
 need('\r' not in text and text.endswith('\n'),'strict LF text with final newline required')
 return text.replace('\n','\r\n').encode('shift_jis',errors='strict')
def plain(path):
 path=Path(path)
 for p in (path,*path.parents):need(not p.is_symlink(),'symlink path')
 return path
def read(path):
 path=plain(path);a=path.stat();need(stat.S_ISREG(a.st_mode),'regular source required')
 raw=path.read_bytes();b=path.stat()
 need((a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_mode)==(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_mode),'source changed')
 return raw
def stage(output,root=ROOT):
 root=Path(root);output=Path(output).absolute();plain(output.parent);need(output.parent.is_dir(),'stage parent missing')
 reference=read(root/REFERENCE);need(sha(reference)==REFERENCE_SHA,'frozen retained driver identity')
 own=read(root/SERVICES);need(b'\r' not in own,'maintained source must be UTF8 LF')
 resident=read(root/RESIDENT);need(b'\r' not in resident,'maintained resident source must be UTF8 LF')
 text=compose_resident(reference.decode('shift_jis'),resident.decode('utf-8'))
 command_inputs={}
 for path,procedures in COMMAND_GROUPS:
  raw=read(root/path);need(b'\r' not in raw,'maintained command source must be UTF8 LF');command_inputs[path]=raw
  text=compose_command_group(text,raw.decode('utf-8'),path,procedures)
 scattered_inputs={}
 for path,procedures in SCATTERED_GROUPS:
  raw=read(root/path);need(b'\r' not in raw,'maintained scattered source must be UTF8 LF');scattered_inputs[path]=raw
  text=compose_scattered(text,raw.decode('utf-8'),procedures)
 text=compose(text,own.decode('utf-8'))
 for old,new in (('libs/master.lib/macros.inc','retained\\master.inc'),('th01/hardware/egc.inc','retained\\egc.inc')):
  need(text.count('include '+old)==1,'retained include statement differs')
  text=text.replace('include '+old,'include '+new)
 files={'driver.asm':dos_text(text),SERVICES:dos_text(own.decode('utf-8')),
        RESIDENT:dos_text(resident.decode('utf-8')),
        'link.rsp':b'-c -s -t -3 driver.obj,driver.com,driver.map,\r\n'}
 files.update({path:dos_text(raw.decode('utf-8')) for path,raw in (command_inputs|scattered_inputs).items()})
 inputs={REFERENCE:sha(reference),SERVICES:sha(own),RESIDENT:sha(resident)}
 inputs.update({path:sha(raw) for path,raw in (command_inputs|scattered_inputs).items()})
 for source,expected,dest in INCLUDES:
  raw=read(root/source);need(sha(raw)==expected,'retained include identity')
  need(not re.search(rb'(?im)^\s*include\b',raw),'unexpected transitive retained include')
  files[dest]=dos_text(raw.decode('utf-8'));inputs[source]=sha(raw)
 output.mkdir()  # Never reuse any previous stage, even an empty one.
 for name,raw in files.items():
  path=output/name;path.parent.mkdir(parents=True,exist_ok=True)
  with path.open('xb') as f:f.write(raw)
 for name,expected in inputs.items():need(sha(read(root/name))==expected,'input changed during stage')
 result=dict(kind='zun-driver-all-procedures-hybrid-stage',inputs=inputs,
             outputs={n:sha(v) for n,v in files.items()},maintained_procedures=55,maintained_instruction_bytes=2844,all_driver_procedures_owned=True,
             complete_driver_source_owned=False,native_invocations=0,exact_acceptance=False)
 with (output/'stage.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 return result
def native_commands(wine,msdos):
 """Recipe only. A parent-owned bounded supervisor must execute these."""
 return ([str(wine),r'C:\TASM50\BIN\TASM32.EXE','/m','/mx','/kh32768','/t','/dTHIEF','driver.asm,driver.obj'],
         [str(wine),str(msdos),'-e','-x','tlink','@link.rsp'])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 print(json.dumps(stage(args.output),indent=2))
if __name__=='__main__':main()
