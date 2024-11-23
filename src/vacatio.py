from src.cfg import ContextFreeGrammar
from src.dep import DependencyGrammar
from src.util import POSTagger, Tokenizer

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
def get_transition(features, dependencies):

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
            for dep in dependencies
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
        get_transition=get_transition
    )
