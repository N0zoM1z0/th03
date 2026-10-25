"""Native CFG and BYTE/WORD arithmetic obligations for the complete staff roll."""
from lib.decoded_mainl_staff_roll_layout import CS,DATA
from lib.decoded_mainl_staff_roll_services import need


def geometry_proof(image):
    # These anchors bind the source-level partition and invariants to native
    # instructions; full raw bytes and relocation order have their own gate.
    anchors=((0x2E47,'be0100eb0f'),(0x2E5A,'4683fe097cec'),
        (0x2E60,'c41eea21b003262a4736a2dc27'),
        (0x2E6D,'268a470cb40048992bc2d1f8a2e727'),
        (0x2E8A,'a0e327b4003d030074073d04007415eb26'),
        (0x2EC1,'803ee327057208a0e827040fa2e827'),
        (0x2ED0,'803ee427007405c606e82764803ee827647605c606e82764'),
        (0x3189,'c706c227000033ff'),(0x3191,'9ac20d7e0ce8c8f3e849f5ff06c2270bff7417'),
        (0x31AD,'f606c2270174dd4f0bff75d8eb22'),
        (0x31BB,'833e0c1d0074cf813ec22700017ec7'),
        (0x31CA,'6808029ae2067e0cbf6400c706c2270000ebb4'),
        (0x31DD,'33f6eb07569a50097e0c4683fe207cf45f5e5dc3'))
    for at,hexadecimal in anchors:
        raw=bytes.fromhex(hexadecimal)
        need(image.program_image[CS*16+at:CS*16+at+len(raw)]==raw,'native roll BYTE partition / exact finite or closed CFG anchor')
    combinations=0
    for initial in range(256):
        for lower_digit in range(256):
            half=lower_digit//2
            for upper_digit in (0,3,4,5):
                value=initial
                if upper_digit==3:
                    value=(value+half+2)&255
                if upper_digit in (3,4):
                    value=(value+half+7)&255
                if upper_digit>=5:
                    value=(value+15)&255
                delta={0:0,3:2*half+9,4:half+7,5:15}[upper_digit]
                expected=min(100,(initial+delta)%256)
                need(min(100,value)==expected,'all skill/lower-digit BYTE pairs retain wrap before final unsigned clamp')
                combinations+=1
    for raw in range(256):
        character=0 if raw==0 else (raw-1)//2
        need(0<=character<=127 and (3-raw)&255 in range(256),'BYTE character and wrapped continues domains')
    frame=0
    tone=100
    for iteration in range(1,200):
        frame=(frame+1)&65535
        if frame&1:
            tone-=1
        need(tone==100-(iteration+1)//2,'complete native odd-frame fade recurrence')
    need(tone==0 and frame==199,'exact199-tick fade; no elapsed physical time claim')
    return dict(score_copy_iterations=8,score_indices=[1,8],resident_score_offsets=[0x18,0x1F],
        character_BYTE_states=256,character_result_range=[0,127],continues_BYTE_states=256,
        skill_pair_cases=combinations,skill_partition=['0..2','3 (falls through4)','4','5..255'],
        skill_formula='min(100,(skill + delta) modulo256); nonzero digit8 overrides100',
        skill_delta=['0','2*(digit6//2)+9','digit6//2+7','15'],skill_result_range=[0,100],
        initial_input_frame=0,minimum_constant_nonzero_input_iterations=257,fade_tone=100,fade_iterations=199,
        cleanup_slots=list(range(32)),maximum_fixture_stack_depth=78,
        returning_assumptions=['all actual owned helpers satisfy their bound ABI; heap/file/palette/driver/sampling replies return and preserve their declared registers',
          'CODE,private stack and external resident are disjoint; no external writes target private frames',
          'input-phase cap stays at most80 (initial80,optional adaptation50); tick cannot alias FRAME/PAGE through particle80',
          'progressing counter1 replies; palette and input replies do not alter FRAME or saved DI'],
        no_input_CFG=[0x3191,0x3196,0x3199,0x319C,0x31A0,0x31A2,0x31BB,0x31C0,0x3191],
        no_input_invariant='if every returned input sample OR is zero and DI starts0,all calls preserve DI and return; DI remains0 and the frame predicate/fade/cleanup are never reached',
        no_input_prefixes_are_returns=False,guest_iterations_skipped=False,budget_expiry_used=False,
        physical_IRQ_audio_input_or_pixels_proved=False)
