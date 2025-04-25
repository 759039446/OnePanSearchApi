import re


def extract_info(text):
    # 修改后的正则表达式：使后续数字或英文组合变为可选
    pattern = r'(https?://[^\s\u4e00-\u9fff]+)'  # 匹配完整链接（不含中文）
    pattern += r'[^0-9a-zA-Z]*'  # 修改前: [\s\u4e00-\u9fff]*
    pattern += r'([0-9a-zA-Z]*)'  # 匹配后续的数字或英文组合（可选）
    res = []
    for line in text.split('\n'):
        matches = re.findall(pattern, line)
        for match in matches:
            link, word = match
            if word:  # 只有当后续部分存在时才拼接
                res.append(f'{link} {word}')
            else:
                res.append(link)  # 如果没有后续部分，仅保留链接
    return res


def extract_info_entity(text):
    # 修改后的正则表达式：使后续数字或英文组合变为可选
    pattern = r'(https?://[^\s\u4e00-\u9fff]+)'  # 匹配完整链接（不含中文）
    pattern += r'[^0-9a-zA-Z]*'  # 修改前: [\s\u4e00-\u9fff]*
    pattern += r'([0-9a-zA-Z]*)'  # 匹配后续的数字或英文组合（可选）
    res = []
    seen = set()  # 新增：用于去重的集合
    for line in text.split('\n'):
        matches = re.findall(pattern, line)
        for match in matches:
            link, pwd = match
            current_pair = (link, pwd)
            if current_pair in seen:
                continue
            seen.add(current_pair)
            res.append({'url': link, 'pwd': pwd})
    return res


def extract_info_entity_next_line(text):
    """
    处理包含下载链接和提取码的文本，合并关联行

    参数：
    text (str): 需要处理的原始文本

    返回：
    list: 处理后的行列表（可在此方法基础上继续添加业务逻辑）
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    processed = []
    prev_line = None

    for current_line in lines:
        # 检查当前行特征
        has_http = re.search(r'https?://', current_line)
        has_code = re.search(r'提取码|密码', current_line)

        # 当符合合并条件时（当前行有提取码且没有链接，前一行有链接但没有提取码）
        if not has_http and has_code and prev_line:
            prev_has_http = re.search(r'https?://', prev_line)
            prev_has_code = re.search(r'提取码|密码', prev_line)

            if prev_has_http and not prev_has_code:
                # 合并到前一行
                processed[-1] += f" {current_line}"
                prev_line = None  # 重置前一行防止重复合并
                continue

        # 正常添加行
        processed.append(current_line)
        prev_line = current_line

    return processed


def extract_info_entity2(text):
    text = "\n".join(extract_info_entity_next_line(text))
    return extract_info_entity(text)