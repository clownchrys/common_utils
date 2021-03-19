import re


class ChineseUnit:
    CONVERT_METHODS = {
        '斤': lambda x: '{value}kg'.format(value=float(x) * 0.5),
    }
    RANGE_SELECTORS = [
        '-', '~'
    ]

    ORDINAL_NUMS = {
        '一': {'level': 1, 'value': 1},
        '二': {'level': 1, 'value': 2},
        '三': {'level': 1, 'value': 3},
        '四': {'level': 1, 'value': 4},
        '五': {'level': 1, 'value': 5},
        '六': {'level': 1, 'value': 6},
        '七': {'level': 1, 'value': 7},
        '八': {'level': 1, 'value': 8},
        '九': {'level': 1, 'value': 9},

        '十': {'level': 2, 'value': 10},
        '百': {'level': 2, 'value': 10 ** 2},
        '千': {'level': 2, 'value': 10 ** 3},

        '万': {'level': 3, 'value': 10 ** 4},
        '亿': {'level': 3, 'value': 10 ** 5},
        '兆': {'level': 3, 'value': 10 ** 6},
        '万亿': {'level': 3, 'value': 10 ** 6},
    }

    @classmethod
    def ordinal_to_cardinal(cls, string: str) -> int:
        string = string.strip().replace(' ', '')
        result = stack2 = stack1 = 0
        last_level = 0

        for char in string:
            info = cls.ORDINAL_NUMS[char]

            if info['level'] == last_level:
                raise Exception(f"Invalid ordinal number: {string!r}")
            else:
                last_level = info['level']

            if info['level'] == 3:
                result += (stack2 + stack1 if stack2 + stack1 else 1) * info['value']
                stack2 = stack1 = 0

            elif info['level'] == 2:
                result += (stack1 if stack1 else 1) * info['value']
                stack1 = 0

            elif info['level'] == 1:
                stack1 += info['value']

            else:
                raise Exception(f"Invalid ordinal level: {info['level']}")

        return result + stack2 + stack1

    @classmethod
    def convert(cls, string: str, search_start: int=0) -> str:
        CARDINALS = '\d+\.*\d*'
        ORDINALS = f"[{'|'.join(cls.ORDINAL_NUMS)}][{'|'.join(cls.ORDINAL_NUMS)}|\s]*"
        RANGES = f"[{'|'.join(cls.RANGE_SELECTORS)}]"
        UNITS = f"{'|'.join(cls.CONVERT_METHODS)}"
        
        regex = f"({CARDINALS}|{ORDINALS})\s*({RANGES})*\s*({CARDINALS}|{ORDINALS})*\s*({UNITS})"
        search_string = string[search_start:]
        search_result = re.search(regex, search_string)

        if not search_result:
            return string

        else:
            start, end = search_result.span()
            src_value1, range_selector, src_value2, unit = search_result.groups()

        try:
            dst_values = []

            for src_value in [src_value1, src_value2]:
                if src_value:
                    src_value = cls.ordinal_to_cardinal(src_value) if re.search(ORDINALS, src_value) else src_value
                    dst_value = cls.CONVERT_METHODS[unit](src_value)
                else:
                    dst_value = ''
                dst_values.append(dst_value)

            dst_value = (range_selector if range_selector else '').join(dst_values)
            string = string[:search_start] + search_string[:start] + str(dst_value) + search_string[end:]

        except Exception as e:
            print(e)
            search_start += end

        else:
            search_start += start + len(str(dst_value))

        return cls.convert(string, search_start)
