from src.cfg import ContextFreeGrammar

NOUNS = [
    # Vietnamese nouns related to tourism and customer service
    "phòng",
    "xe",
    "máy bay",
    "nhà hàng",
    "khách sạn",
    "bãi biển",
    "tiền",
    "vé",
    "dịch vụ",
    "lịch trình",
    "đồ ăn",
    "thức uống",
    "ẩm thực",
    "thời tiết",
    "địa điểm",
    "thời gian",
    "ngày",
    "giờ",

    "tour",
    "giá",
    "người",
    "vé máy bay",
    "không gian",
    "quán cà phê",
    "lịch trình",
    "xe khách"
]

VERBS = [
    # common verbs in Vietnamese, used in the context of tourism and customer service
    "đặt",
    "mua",
    "thuê",
    "đi",
    "tìm",
    "thanh toán",
    "trả",
    "nhận",

    "tìm hiểu",
    "biết",
    "cần",
    "đổi",
    "có",
    "gọi",
    "xem xét"
]

ADJECTIVES = [
    # Vietnamese adjectives related to tourism and customer service
    "đẹp",
    "xấu",
    "tốt",
    "rẻ",
    "đắt",
    "nhanh",
    "chậm",
    "lạnh",
    "nóng",
    "tươi",
    "ngon",
    "khô",
    "đầy",
    "trống",
    "đông",
    "ít",
    "nhiều",

    "bận",
    "rảnh"
]

PREPOSITIONS = [
    # Vietnamese prepositions
    "ở",
    "tại",
    "trong",
    "trên",
    "dưới",

    "về",
    "cho",
    "cùng"
]

ADVERBS_AHEAD = [
    # Vietnamese adverbs that can come before adjectives
    "rất",
    "quá",
    "vô cùng",
    "hết sức",
    "không"
]

ADVERBS_ATAIL = [
    # Vietnamese adverbs that can come after adjectives
    "lắm",
    "quá",
    "vãi",
    "cực kỳ"
]

ADVERBS_VHEAD = [
    # Vietnamese adverbs that can come before verbs
    "đã",
    "đang",
    "sẽ",
    "vẫn",
    "có thể",
    "nên",
    "không",
    "chưa",
    "đã từng",

    "muốn",
    "cần"
]

ADVERBS_VTAIL = [
    # Vietnamese adverbs that can come after verbs
    "rồi",
    "đi",
    "không",
    "hả",

    "thêm",
    "trước",
    "sau"
]

NUMERALS = [
    # Vietnamese numerals
    "một",
    "hai",
    "ba",
    "bốn",
    "năm",
    "sáu",
    "bảy",
    "tám",
    "chín"
]

QUANTIFIERS = [
    # Vietnamese quantifiers
    "một ít",
    "nhiều",
    "vài",
    "một số",
    "tất cả",
    "những",
    "mấy",
    "các"
]

PRONOUNS = [
    # Vietnamese pronouns
    "tôi",
    "bạn",
    "anh",
    "chị",
    "em",
    "họ",
    "ai"
]

DEMONSTRATIVES = [
    # Vietnamese demonstratives
    "này",
    "đó",
    "kia",
    "ấy",
    "đây"
]

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





