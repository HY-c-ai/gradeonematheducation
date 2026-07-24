import json
import random
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def counter(request):
    return render(request, 'counter.html')


def make_ten(request):
    return render(request, 'make_ten.html')


def clock(request):
    return render(request, 'clock.html')


def length_units(request):
    return render(request, 'length_units.html')


def rmb(request):
    return render(request, 'rmb.html')


def number_line(request):
    return render(request, 'number_line.html')


def multiplication(request):
    return render(request, 'multiplication.html')


def division(request):
    return render(request, 'division.html')


# ============================================================
#  拼音模块 - 数据定义
#  声母、韵母、声调三部分完全分离，各自独立管理
# ============================================================

PINYIN_INITIALS = [
    'b', 'p', 'm', 'f',
    'd', 't', 'n', 'l',
    'g', 'k', 'h',
    'j', 'q', 'x',
    'zh', 'ch', 'sh', 'r',
    'z', 'c', 's',
    'y', 'w'
]

PINYIN_FINALS = [
    'a', 'o', 'e', 'i', 'u', 'ü',
    'ai', 'ei', 'ui', 'ao', 'ou', 'iu', 'ie', 'üe',
    'an', 'en', 'in', 'un', 'ün',
    'ang', 'eng', 'ing', 'ong'
]

PINYIN_VALID_COMBINATIONS = {
    'b':  ['a','o','i','u','ai','ei','ao','an','en','ang','eng','ie','ian','in','iang','ing'],
    'p':  ['a','o','i','u','ai','ei','ao','ou','an','en','ang','eng','ie','ian','in','iang','ing'],
    'm':  ['a','o','e','i','u','ai','ei','ao','ou','an','en','ang','eng','ie','ian','in','iang','ing','iu'],
    'f':  ['a','o','u','ei','ou','an','en','ang','eng'],
    'd':  ['a','e','i','u','ai','ei','ao','ou','an','en','ang','eng','ia','ie','ian','iao','iu','uan','ui','un','uo','ing'],
    't':  ['a','e','i','u','ai','ei','ao','ou','an','ang','eng','ia','ie','ian','iao','iu','uan','ui','un','uo','ing'],
    'n':  ['a','e','i','u','ü','ai','ei','ao','ou','an','en','ang','eng','ia','ie','ian','iao','iu','uan','ui','un','uo','üe','ing'],
    'l':  ['a','e','i','u','ü','ai','ei','ao','ou','an','ang','eng','ia','ie','ian','iao','iu','uan','ui','un','uo','üe','ing'],
    'g':  ['a','e','u','ai','ei','ao','ou','an','en','ang','eng','ua','uai','uan','uang','ui','un','uo'],
    'k':  ['a','e','u','ai','ei','ao','ou','an','en','ang','eng','ua','uai','uan','uang','ui','un','uo'],
    'h':  ['a','e','u','ai','ei','ao','ou','an','en','ang','eng','ua','uai','uan','uang','ui','un','uo'],
    'j':  ['i','ia','ie','ian','iang','iao','iu','in','ing','ü','üe','ün'],
    'q':  ['i','ia','ie','ian','iang','iao','iu','in','ing','ü','üe','ün'],
    'x':  ['i','ia','ie','ian','iang','iao','iu','in','ing','ü','üe','ün'],
    'zh': ['a','e','i','u','ai','ei','ao','ou','an','en','ang','eng','ua','uai','uan','uang','ui','un','uo'],
    'ch': ['a','e','i','u','ai','ei','ao','ou','an','en','ang','eng','ua','uai','uan','uang','ui','un','uo'],
    'sh': ['a','e','i','u','ai','ei','ao','ou','an','en','ang','eng','ua','uai','uan','uang','ui','un','uo'],
    'r':  ['e','i','u','ao','ou','an','en','ang','eng','ua','uai','uan','ui','un','uo'],
    'z':  ['a','e','i','u','ai','ei','ao','ou','an','en','ang','eng','ua','uai','uan','ui','un','uo'],
    'c':  ['a','e','i','u','ai','ei','ao','ou','an','en','ang','eng','ua','uai','uan','ui','un','uo'],
    's':  ['a','e','i','u','ai','ei','ao','ou','an','en','ang','eng','ua','uai','uan','ui','un','uo'],
    'y':  ['a','e','i','u','ai','ao','ou','an','ang','in','ing','ie','ian','iang','iao'],
    'w':  ['a','o','u','ai','ei','ao','ou','an','en','ang','eng']
}

PINYIN_ER_TONES = [
    {'text': 'ér', 'tone': 2, 'name': '二声', 'char': '儿'},
    {'text': 'ěr', 'tone': 3, 'name': '三声', 'char': '耳'},
    {'text': 'èr', 'tone': 4, 'name': '四声', 'char': '二'}
]

PINYIN_TONE_MAP = {
    'a': ['a', 'ā', 'á', 'ǎ', 'à'],
    'o': ['o', 'ō', 'ó', 'ǒ', 'ò'],
    'e': ['e', 'ē', 'é', 'ě', 'è'],
    'i': ['i', 'ī', 'í', 'ǐ', 'ì'],
    'u': ['u', 'ū', 'ú', 'ǔ', 'ù'],
    'ü': ['ü', 'ǖ', 'ǘ', 'ǚ', 'ǜ']
}

PINYIN_TONE_NAMES = ['', '一声 ˉ', '二声 ˊ', '三声 ˇ', '四声 ˋ']


# ============================================================
#  拼音模块 - 核心逻辑函数
#  每个函数职责单一，不产生副作用
# ============================================================

def pinyin_get_vowel_position(final):
    """确定韵母中哪个元音承载声调标记。返回 (位置, 元音字符)。"""
    if 'a' in final:
        return final.index('a'), 'a'
    if 'e' in final:
        return final.index('e'), 'e'
    if 'ou' in final:
        return final.index('ou'), 'o'
    if 'iu' in final:
        return final.index('iu') + 1, 'u'
    vowels = 'aoeiuü'
    for i in range(len(final) - 1, -1, -1):
        if final[i] in vowels:
            return i, final[i]
    return -1, ''


def pinyin_apply_tone(raw_pinyin, tone):
    """给原始拼音字符串添加声调标记。返回带声调的拼音字符串。"""
    if tone == 0 or tone is None:
        return raw_pinyin
    pos, vowel = pinyin_get_vowel_position(raw_pinyin)
    if pos >= 0 and vowel in PINYIN_TONE_MAP:
        chars = PINYIN_TONE_MAP[vowel]
        if tone < len(chars):
            return raw_pinyin[:pos] + chars[tone] + raw_pinyin[pos + 1:]
    return raw_pinyin


def pinyin_is_valid_combination(initial, final):
    """验证声母和韵母是否可以合法拼读。"""
    if final == 'er':
        return initial == ''
    if not initial:
        return False
    return final in PINYIN_VALID_COMBINATIONS.get(initial, [])


def pinyin_extract_initial():
    """【独立抽取】仅随机抽取一个声母，不依赖其他组件。"""
    return random.choice(PINYIN_INITIALS)


def pinyin_extract_final(initial=None):
    """【独立抽取】仅随机抽取一个韵母。
    若提供 initial，优先返回与之兼容的韵母；否则随机返回任意韵母。
    """
    if initial and initial in PINYIN_VALID_COMBINATIONS:
        return random.choice(PINYIN_VALID_COMBINATIONS[initial])
    return random.choice(PINYIN_FINALS)


def pinyin_extract_tone(final=None):
    """【独立抽取】仅随机抽取一个声调（1-4）。
    若 final 为 'er'，仅返回 2、3、4（er 没有一声）。
    """
    if final == 'er':
        return random.choice([2, 3, 4])
    return random.randint(1, 4)


def pinyin_combine(initial, final, tone):
    """将声母、韵母、声调组合为完整拼音。
    返回包含完整拼音及元数据的字典，方便前端独立渲染各组件。
    """
    is_er = (final == 'er' and not initial)

    if is_er:
        er_info = next(
            (e for e in PINYIN_ER_TONES if e['tone'] == tone),
            PINYIN_ER_TONES[0]
        )
        full_pinyin = er_info['text']
    else:
        raw_pinyin = initial + final
        full_pinyin = pinyin_apply_tone(raw_pinyin, tone)

    return {
        'initial': initial,
        'final': final,
        'tone': tone,
        'full_pinyin': full_pinyin,
        'tone_name': PINYIN_TONE_NAMES[tone] if 1 <= tone <= 4 else '',
        'is_er': is_er
    }


# ============================================================
#  拼音模块 - 视图
# ============================================================

def pinyin(request):
    """渲染拼音学习页面，同时注入完整的拼音数据供前端使用。"""
    context = {
        'pinyin_data': {
            'initials': PINYIN_INITIALS,
            'finals': PINYIN_FINALS,
            'valid_combinations': PINYIN_VALID_COMBINATIONS,
            'er_tones': PINYIN_ER_TONES,
            'tone_map': PINYIN_TONE_MAP,
            'tone_names': PINYIN_TONE_NAMES,
        }
    }
    return render(request, 'pinyin.html', context)
