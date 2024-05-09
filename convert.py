#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Usage:
#   convert.py input_filename
# input_filename is a file of Wikipedia article titles, one title per line.

import logging
import re
import sys

import opencc
from pypinyin import TONE3, lazy_pinyin

# 限制文本长度
_MINIMUM_LEN = 2
_MAXIMUM_LEN = 4

_LIST_PAGE_ENDINGS = [
    '列表',
    '对照表',
]

_LIST_SURNAME = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹', '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾', '路', '娄', '危', '江', '童', '颜', '郭', '梅', '盛', '林', '刁', '钟', '徐', '邱', '骆', '高', '夏', '蔡', '田', '樊', '胡', '凌', '霍', '虞', '万', '支', '柯', '昝', '管', '卢', '莫', '房', '裘', '缪', '干', '解', '应', '宗', '丁', '宣', '贲', '邓', '郁', '单', '杭', '洪', '包', '诸', '左', '石', '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴', '陆', '荣', '翁', '荀', '羊', '惠', '甄', '曲', '家', '封', '芮', '羿', '储', '靳', '汲', '邴', '糜', '松', '井', '段', '富', '巫', '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋', '仲', '伊', '宫', '宁', '仇', '栾', '暴', '甘', '钭', '历', '戎', '祖', '武', '符', '刘', '景', '詹', '束', '龙', '叶', '幸', '司', '韶', '郜', '黎', '蓟', '溥', '印', '宿', '白', '怀', '蒲', '邰', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙', '池', '乔', '阳', '胥', '能', '苍', '双', '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄', '姬', '申', '扶', '堵', '冉', '宰', '郦', '雍', '却', '璩', '桑', '桂', '濮', '牛', '寿', '通', '边', '扈', '燕', '冀', '浦', '尚', '农', '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连', '茹', '习', '宦', '艾', '鱼', '容', '向', '古', '易', '慎', '戈', '廖', '庾', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', '匡', '国', '文', '寇', '广', '禄', '阙', '东', '欧', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾', '敖', '融', '冷', '訾', '辛', '阚', '那', '简', '饶', '空', '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查', '后', '荆', '红', '游', '竺', '权', '逮', '盍', '益', '桓', '公', '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方', '赫连', '皇甫', '尉迟', '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙', '轩辕', '令狐', '徐离', '宇文', '长孙', '慕容', '司徒', '司空', '亓官', '司寇', '仉督', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正', '壤驷', '公良', '拓拔', '夹谷', '宰父', '谷梁', '晋楚', '闫法', '汝鄢', '涂钦', '段干', '百里', '东郭', '南门', '呼延', '归海', '羊舌', '微生', '岳帅', '缑亢', '况后', '有琴', '梁丘', '左丘', '东门', '西门', '商牟', '佘佴', '伯赏', '南宫']

_LIST_SURNAME_DOUBLE = ['万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方', '赫连', '皇甫', '尉迟', '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙', '轩辕', '令狐', '徐离', '宇文', '长孙', '慕容', '司徒', '司空', '亓官', '司寇', '仉督', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正', '壤驷', '公良', '拓拔', '夹谷', '宰父', '谷梁', '晋楚', '闫法', '汝鄢', '涂钦', '段干', '百里', '东郭', '南门', '呼延', '归海', '羊舌', '微生', '岳帅', '缑亢', '况后', '有琴', '梁丘', '左丘', '东门', '西门', '商牟', '佘佴', '伯赏', '南宫']

_LOG_EVERY = 10000

_PINYIN_SEPARATOR = ' '
_HANZI_RE = re.compile('^[\u4e00-\u9fa5]+$')
_TO_SIMPLIFIED_CHINESE = opencc.OpenCC('t2s.json')

_PINYIN_FIXES = {
    'n': 'en',  # https://github.com/felixonmars/fcitx5-pinyin-zhwiki/issues/13
}

logging.basicConfig(level=logging.INFO)

def is_chinese_date(text):
    pattern = r'^[零一二三四五六七八九十百千万亿廿年代月日]+$'
    return bool(re.match(pattern, text))

def is_good_title(title, previous_title=None):
    if not _HANZI_RE.match(title):
        return False

    # Skip single character & too long pages
    if len(title) < _MINIMUM_LEN:
        return False

    if len(title) > _MAXIMUM_LEN:
        return False

    # 3字词语 过滤姓氏开头
    if len(title) == 3:
        if title.startswith(tuple(_LIST_SURNAME)):
            return False

    # 4字词语 过滤复姓
    if len(title) == 4:
        if title.startswith(tuple(_LIST_SURNAME_DOUBLE)):
            return False

    # Skip list pages
    if title.endswith(tuple(_LIST_PAGE_ENDINGS)):
        return False

    # 如果全部为中文日期 则过滤
    if is_chinese_date(title):
        return False

    if previous_title and \
      len(previous_title) >= 3 and \
      title.startswith(previous_title):
        return False

    return True

def log_count(count):
    logging.info(f'{count} words generated')

def make_output(word, pinyin):
    return '\t'.join([word, pinyin])

def main():
    previous_title = None
    result_count = 0
    with open(sys.argv[1]) as f:
        for line in f:
            title = _TO_SIMPLIFIED_CHINESE.convert(line.strip())
            if is_good_title(title, previous_title):
                pinyin = [_PINYIN_FIXES.get(item, item) for item in lazy_pinyin(title, style=TONE3)]
                pinyin = _PINYIN_SEPARATOR.join(pinyin)
                if pinyin == title:
                    logging.info(
                        f'Failed to convert to Pinyin. Ignoring: {pinyin}')
                    continue
                print(make_output(title, pinyin))
                result_count += 1
                if result_count % _LOG_EVERY == 0:
                    log_count(result_count)
                previous_title = title
    log_count(result_count)

if __name__ == '__main__':
    main()
