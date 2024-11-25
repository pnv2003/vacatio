from typing import List
from src.cfg import ContextFreeGrammar
from src.dep import Dependency, DependencyGrammar, TransitionClassifier
from src.logic import Entity, LogicalForm, ThematicRole
from src.procedure import FilterProcedure, Procedure, SelectProcedure
from src.relation import Relation
from src.util import POSTagger, Tokenizer, VariableManager

NOUNS = ["phòng", "xe", "máy bay", "nhà hàng", "khách sạn", "bãi biển", "tiền", "vé", "dịch vụ", "lịch trình", "đồ ăn", "thức uống", "ẩm thực", "thời tiết", "địa điểm", "thời gian", "ngày", "giờ", "tour", "giá", "người", "vé máy bay", "không gian", "quán cà phê", "lịch trình", "xe khách"]
VERBS = ["đặt", "mua", "thuê", "đi", "tìm", "thanh toán", "trả", "nhận", "tìm hiểu", "biết", "cần", "đổi", "có", "gọi", "xem xét"]
ADJECTIVES = ["đẹp", "xấu", "tốt", "rẻ", "đắt", "nhanh", "chậm", "lạnh", "nóng", "tươi", "ngon", "khô", "đầy", "trống", "đông", "ít", "nhiều", "bận", "rảnh"]
PREPOSITIONS = ["ở", "tại", "trong", "trên", "dưới", "về", "cho", "cùng"]
ADVERBS_AHEAD = ["rất", "quá", "vô cùng", "hết sức", "không"]
ADVERBS_ATAIL = ["lắm", "quá", "vãi", "cực kỳ"]
ADVERBS_VHEAD = ["đã", "đang", "sẽ", "vẫn", "có thể", "nên", "không", "chưa", "đã từng", "muốn", "cần"]
ADVERBS_VTAIL = ["rồi", "đi", "không", "hả", "thêm", "trước", "sau"]
NUMERALS = ["một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
QUANTIFIERS = ["một ít", "nhiều", "vài", "một số", "tất cả", "những", "mấy", "các"]
PRONOUNS = ["tôi", "bạn", "anh", "chị", "em", "họ", "ai"]
DEMONSTRATIVES = ["này", "đó", "kia", "ấy", "đây"]

def context_free_grammar() -> ContextFreeGrammar:

    return ContextFreeGrammar.fromstring(
"""
S -> SUBJ PRED | PRED
SUBJ -> NP
PRED -> VP | ADJP
NP -> PRO | NPI | NPI DEMON | NPI PP
NPI -> N | NUM N | QUANT N | N ADJ
VP -> VPI | VPI ADV_VTAIL 
VPI -> V | V NP | ADV_VHEAD V | ADV_VHEAD V NP
ADJP -> ADJ | ADV_AHEAD ADJ | ADJ ADV_ATAIL
PP -> P NP
""" +
        "\n".join([
            f"{lhs} -> {' | '.join([ ' '.join(rhs) for rhs in rhslist ])}"
            for lhs, rhslist in {
                "PRO": [[pro] for pro in PRONOUNS],
                "N": [[noun] for noun in NOUNS],
                "V": [[verb] for verb in VERBS],
                "ADJ": [[adj] for adj in ADJECTIVES],
                "ADV_AHEAD": [[adv] for adv in ADVERBS_AHEAD],
                "ADV_ATAIL": [[adv] for adv in ADVERBS_ATAIL],
                "ADV_VHEAD": [[adv] for adv in ADVERBS_VHEAD],
                "ADV_VTAIL": [[adv] for adv in ADVERBS_VTAIL],
                "NUM": [[num] for num in NUMERALS],
                "QUANT": [[quant] for quant in QUANTIFIERS],
                "P": [[prep] for prep in PREPOSITIONS],
                "DEMON": [[dem] for dem in DEMONSTRATIVES]
            }.items()
        ])
    )

# Token map for multi-word tokens
TOKEN_MAP = {
    "có thể": "có_thể",
    "tất cả": "tất_cả",
    "được không": "được_không",
    "bao lâu": "bao_lâu",
    "bao nhiêu": "bao_nhiêu",
    "phương tiện": "phương_tiện",
    "Hồ Chí Minh": "Hồ_Chí_Minh",
    "Nha Trang": "Nha_Trang",
    "Phú Quốc": "Phú_Quốc",
    "Đà Nẵng": "Đà_Nẵng",
}

# POS dictionary
POS_DICT = {
    "em": "PRO",
    "có_thể": "AUX",
    "nhắc": "V",
    "lại": "ADV",
    "tất_cả": "DET",
    "các": "DET",
    "tour": "N",
    "được_không": "DISC",
    "từ": "P",
    "tới": "P",
    "đi": "V",
    "hết": "V",
    "bao_lâu": "N-Q",
    "có": "V",
    "bao_nhiêu": "DET-Q",
    "phương_tiện": "N",
    "vậy": "DISC",
    "bạn": "PRO",
    "bằng": "P",
    "gì": "PRO-Q",
    "những": "DET",
    "ngày": "N",
    "nào": "PRO-Q",
    "nhỉ": "DISC",
    "Hồ_Chí_Minh": "N-LOC",
    "Nha_Trang": "N-LOC",
    "Phú_Quốc": "N-LOC",
    "Đà_Nẵng": "N-LOC",
    "?": "PUNCT",
}


# transition getter
def get_transition(features):
    """(s = stack top item, b = buffer first item)

    - SHIFT when:
        - s = ROOT
        - b = ROOT, AUX, DET, DET-Q, P

    - LEFT_ARC label when:

        - s = AUX and b = V         -> aux
        - s = PRO/N and b = V       -> nsubj | acl (if has_main_verb)
        - s = DET/DET-Q and b = N   -> det
        - s = P and b = N-LOC/N     -> case
        - s = V and b = V           -> csubj

    - RIGHT_ARC label when:

        - s = V and b = ADV             -> advmod
        - s = V and b = PRO/N/N-Q/N-LOC -> obj | obl (if b has case)
        - s = V and b = DISC            -> discourse
        - s = V and b = PUNCT           -> punct
        - s = DISC                      -> compound
        - s = N/N-LOC and b = N/N-LOC   -> compound
        - s = N and b = PRO-Q           -> compound

    - REDUCE when:

        - s = ADV and b = DET
        - s != V and b = DISC/PUNCT
        - s = N-LOC and b = P/V
        - s = V and b = DISC/PUNCT and has_main_verb
    """

    deps = features['deps']
    sword = features['sword']
    bword = features['bword']
    spos = features['spos']
    bpos = features['bpos']
    sindex = features['sindex']
    bindex = features['bindex']
    has_main_verb = features['has_main_verb']

    if spos == 'ADV' and bpos in ['DET']:
        return 'REDUCE'
    if spos != 'V' and bpos in ['DISC', 'PUNCT']:
        return 'REDUCE'
    if spos == 'N-LOC' and bpos in ['P', 'V']:
        return 'REDUCE'
    if spos == 'V' and bpos in ['DISC', 'PUNCT']:
        if has_main_verb:
            return 'REDUCE'

    if spos == 'ROOT':
        return 'SHIFT'
    if bpos in ['ROOT', 'AUX', 'DET', 'DET-Q', 'P']:
        return 'SHIFT'
    
    if spos == 'AUX' and bpos == 'V':
        return 'LEFT_ARC aux'
    if spos in ['PRO', 'N'] and bpos == 'V':
        if has_main_verb:
            return 'RIGHT_ARC acl'
        if sword == 'tour' and bword == 'đi': # super hacky way to handle this (bruh moment)
            return 'LEFT_ARC obj'
        return 'LEFT_ARC nsubj'
    if spos in ['DET', 'DET-Q'] and bpos == 'N':
        return 'LEFT_ARC det'
    if spos == 'P' and bpos in ['N-LOC', 'N']:
        return 'LEFT_ARC case'
    if spos == 'V' and bpos == 'V':
        return 'LEFT_ARC csubj'
    
    if spos == 'V' and bpos == 'ADV':
        return 'RIGHT_ARC advmod'
    if spos == 'V' and bpos in ['PRO', 'N', 'N-Q', 'N-LOC']:

        if any([
            dep.head.index == sindex and dep.label == 'case'
            for dep in deps
        ]):
            return 'RIGHT_ARC obl'
        
        return 'RIGHT_ARC obj'
        
    if spos == 'V' and bpos == 'DISC':
        return 'RIGHT_ARC discourse'
    if spos == 'V' and bpos == 'PUNCT':
        return 'RIGHT_ARC punct'
    if spos == 'DISC':
        return 'RIGHT_ARC compound'
    if spos in ['N', 'N-LOC'] and bpos in ['N', 'N-LOC']:
        return 'RIGHT_ARC compound'
    if spos == 'N' and bpos == 'PRO-Q':
        return 'RIGHT_ARC compound'
    
    raise Exception(f'Cannot determine transition for {spos} - {bpos}')

def dependency_grammar() -> DependencyGrammar:

    return DependencyGrammar(
        tokenizer=Tokenizer(token_map=TOKEN_MAP),
        pos_tagger=POSTagger(pos_dict=POS_DICT),
        transition_classifier=TransitionClassifier(get_transition)
    )

# life is full of heuristics
# this is one of them
def relationalize(dependencies: List[Dependency]):

    # extract useful relations based on database in input/database.txt
    relations = []
    from_loc = None
    to_loc = None
    tour_name = None
    varm = VariableManager()

    for dep in dependencies:

        # for main predicates
        if dep.label == 'root':
            relations.append(Relation('VERB', dep.tail.word))

        # for quantifiers
        if dep.label == 'det':
            if dep.tail.word == 'bao_nhiêu':
                relations.append(Relation('HOW-MANY', dep.head.word))
            if dep.tail.word == 'tất_cả':
                relations.append(Relation('ALL', dep.head.word))
            if dep.tail.word in ['các', 'những']:
                relations.append(Relation('PLUR', dep.head.word))

        # for command speech acts
        if dep.tail.word == 'được_không':
            relations.append(Relation('COMMAND', dep.head.word))

        # for locations
        if dep.label == 'case':
            if dep.tail.word == 'từ':
                from_loc = dep.head.word
            if dep.tail.word == 'đến':
                to_loc = dep.head.word

        # for themes
        if dep.label == 'obj':

            if dep.head.word == 'đi':
                if dep.tail.pos == 'N-LOC':
                    if dep.tail.word not in [from_loc, to_loc]:
                        to_loc = dep.tail.word
                elif dep.tail.word == 'tour':
                    if tour_name:
                        to_loc = tour_name
                    relations.append(Relation('THEME', dep.tail.word))

            elif dep.tail.word == 'bao_lâu':
                relations.append(Relation('HOW-MUCH', 'TIME'))
            else:
                relations.append(Relation('THEME', dep.tail.word))

        # for compound nouns
        if dep.label == 'compound' and dep.head.pos in ['N', 'N-LOC']:

            if dep.tail.word in ['gì', 'nào']:
                relations.append(Relation('WH', dep.head.word))
            else:
                relations.append(Relation('THE', dep.head.word))
                if dep.head.word == 'tour':
                    tour_name = dep.tail.word
                else:
                    relations.append(Relation('COMP', dep.head.word, dep.tail.word))        

    if from_loc:
        relations.append(Relation('FROM-LOC', from_loc))
    if to_loc:
        relations.append(Relation('TO-LOC', to_loc))

    for rel in relations:
        entity = rel.args[0]
        key = varm.set(entity, entity)
        rel.make_variable(key)

    return relations

def logicalize(relations: List[Relation]) -> LogicalForm:
    
    # speech act
    lf_spact = None
    lf_verb = None
    entities = []
    thematic_roles = []

    for rel in relations:

        if rel.pred == 'COMMAND':
            lf_spact = LogicalForm('COMMAND')
        if rel.pred in ['HOW-MANY', 'HOW-MUCH', 'WH']:
            lf_spact = LogicalForm('WH-QUERY')

            if rel.pred in ['HOW-MANY', 'WH']:
                thematic_roles.append(ThematicRole(
                    'INSTR' if rel.args[0] == 'phương_tiện' else 'THEME',
                    Entity(rel.pred, rel.var, rel.args[0])
                ))

            elif rel.pred == 'HOW-MUCH' and rel.args[0] == 'TIME':
                thematic_roles.append(ThematicRole(
                    'THEME',
                    Entity('HOW-MUCH', rel.var, rel.args[0]),
                ))

        if rel.pred == 'VERB':
            lf_verb = LogicalForm(rel.args[0])
            lf_verb.var = rel.var

        if rel.pred in ['ALL', 'THE']:
            entities.append(Entity(rel.pred, rel.var, rel.args[0]))
        if rel.pred == 'THEME':
            thematic_roles.append(ThematicRole('THEME', None, rel.var))
        if rel.pred == 'FROM-LOC':
            thematic_roles.append(ThematicRole(
                'FROM-LOC', 
                Entity('NAME', rel.var, rel.args[0]), 
                rel.var
            ))
        if rel.pred == 'TO-LOC':
            thematic_roles.append(ThematicRole(
                'TO-LOC', 
                Entity('NAME', rel.var, rel.args[0]), 
                rel.var
            ))

    for tr in thematic_roles:
        for e in entities:
            if tr.var == e.var:
                tr.entity = e
                break
        
        if tr.entity:
            lf_verb.add_argument(tr)
    
    lf_spact.add_argument(lf_verb)
    return lf_spact

def proceduralize(logical_form: LogicalForm) -> Procedure:
    
    DATA = {
        'tour': 'TOUR',
        'phương_tiện': 'BY',
        'ngày': 'TIME',
    }

    VEHICLE = {
        'máy bay': 'airplane',
        'tàu hỏa': 'train',
    }

    LOCATION = {
        'Hồ_Chí_Minh': 'HCM',
        'Nha_Trang': 'NT',
        'Phú_Quốc': 'PQ',
        'Đà_Nẵng': 'DN',
    }

    lf = logical_form

    proc = None
    thematic_roles = lf.args[0].args

    # type
    if lf.predicate == 'COMMAND':
    
        tr = thematic_roles[0]
        proc = FilterProcedure(
            'TIME' if tr.entity.name == 'tour' else '', # TODO: more cases
            []
        )
        
    for tr in thematic_roles:

        emod = tr.entity.modifier

        if emod == 'HOW-MUCH':
            proc = SelectProcedure(
                4,
                'RUN-TIME',
                []
            )
            
            break
    
        elif emod == 'HOW-MANY':
            proc = FilterProcedure(
                'TIME' if tr.entity.name == 'tour' else '', # TODO: more cases
                []
            )
            break

        elif emod == 'WH':

            query = None
            if tr.entity.name == 'ngày':
                query = 3, 5
            elif tr.entity.name == 'phương_tiện':
                query = 2
            # TODO: more wh-queries

            proc = SelectProcedure(
                query,
                DATA[tr.entity.name],
                []
            )
            break

    if proc.data == 'TOUR':
        pass

    elif proc.data == 'TIME':
        
        tour, dloc, dtime, aloc, atime  = None, None, None, None, None

        for tr in thematic_roles:
            if tr.role == 'FROM-LOC':
                dloc = LOCATION[tr.entity.name]
            elif tr.role == 'TO-LOC':
                tour = LOCATION[tr.entity.name]
                aloc = LOCATION[tr.entity.name]
            elif tr.role == 'TIME':
                atime = tr.entity.name

            # TODO: FROM-TIME, TO-TIME

        proc.criteria = [tour, dloc, dtime, aloc, atime]

    elif proc.data == 'RUN-TIME':

        tour, dloc, what, runtime = None, None, None, None

        for tr in thematic_roles:
            if tr.role == 'FROM-LOC':
                dloc = LOCATION[tr.entity.name]
            elif tr.role == 'TO-LOC':
                tour = LOCATION[tr.entity.name]
            elif tr.role == 'TIME':
                runtime = tr.entity.name

            # TODO: FOR-TIME

        proc.criteria = [tour, dloc, what, runtime]

    elif proc.data == 'BY':

        tour, vehicle = None, None

        for tr in thematic_roles:
            if tr.role == 'TO-LOC':
                tour = LOCATION[tr.entity.name]
            elif tr.role == 'INSTR' and tr.entity.name in VEHICLE:
                vehicle = VEHICLE[tr.entity.name]

        proc.criteria = [tour, vehicle]

    return proc

def answer(proc: Procedure, db: dict):

    LANG = {
        'PQ': 'Phú Quốc',
        'NT': 'Nha Trang',
        'DN': 'Đà Nẵng',
        'HCM': 'Hồ Chí Minh',
        'HCMC': 'Thành phố Hồ Chí Minh',
        'airplane': 'máy bay',
        'train': 'tàu hỏa',
    }

    def time2lang(time):
        hour, date = time.split(' ')

        return f"{hour[:-2]} giờ {'sáng' if hour[-2:] == 'AM' else 'chiều'} ngày {date}"
    
    def duration2lang(dur):

        dur, unit = dur.split(' ')
        hour, minute = dur.split(':')
        
        return f"{hour} giờ {minute} phút"
    
    res = proc.execute(db)

    if proc.action == 'SELECT':

        if not res:
            return 'Không tìm thấy thông tin phù hợp.'
        if proc.data == 'TOUR':
            if proc.query == 1:
                return f'Từ viết tắt của tour này là {res}.'
            
            elif proc.query == 2:
                return f'Tên đầy đủ của tour này là {res}.'
        elif proc.data == 'TIME':
            if proc.query == (3,5):

                tour = f'Tour {LANG[proc.criteria[0]]}' if proc.criteria[0] else 'Tour'
                dloc = f' đi từ {LANG[proc.criteria[1]]} ' if proc.criteria[1] else ' '
                aloc = f' đến {LANG[proc.criteria[3]]} ' if proc.criteria[3] else ' '

                return f'{tour}{dloc}có lịch trình như sau:\n' + ''.join([
                    f'{i + 1}. Từ {time2lang(d)} đến {time2lang(a)}.\n'
                    for i, (d, a) in enumerate(res)
                ])

        elif proc.data =='RUN-TIME':

            if proc.query == 4:
                return f'Tour {LANG[proc.criteria[0]]} đi từ {LANG[proc.criteria[1]]} chạy trong khoảng thời gian {duration2lang(res[0])}.'
            
        elif proc.data == 'BY':

            if proc.query == 2:
                return (
                    f'Tour {LANG[proc.criteria[0]]} đi bằng {LANG[res[0]]}.' if len(res) == 1
                    else f'Tour {LANG[proc.criteria[0]]} có thể đi bằng các phương tiện sau: {", ".join([LANG[r] for r in res])}.'
                )
            
    elif proc.action == 'FILTER':

        if proc.data == 'TIME':

            if not res:
                return 'Không tìm thấy tour phù hợp.'
            
            ans = f'Có {len(res)} tour:\n' + ''.join([
                f'{i + 1}. Tour {LANG[tour]} từ {LANG[dloc]} đến {LANG[aloc]} xuất phát vào lúc {time2lang(dtime)} và kết thúc vào lúc {time2lang(atime)}.\n'
                for i, (tour, dloc, dtime, aloc, atime) in enumerate(res)
            ])

            return ans            


                


            
        

            

            



                




        
   