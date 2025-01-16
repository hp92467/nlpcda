from nlpcda import Similarword
from datetime import datetime


def batch_similar_replace(sentences, create_num=10, change_rate=0.2):
    """
    批量处理多个句子的同义词替换

    参数:
    sentences: list, 需要进行同义词替换的句子列表
    create_num: int, 每个句子生成的替换结果数量
    change_rate: float, 词语被替换的概率

    返回:
    dict: 键为原始句子，值为替换后的句子列表
    """
    smw = Similarword(create_num=create_num, change_rate=change_rate)
    results = {}

    for sentence in sentences:
        replaced = smw.replace(sentence)
        results[sentence] = replaced

    return results


def save_results(results, output_format='txt'):
    """
    保存替换结果到文件

    参数:
    results: dict, 替换结果字典
    output_format: str, 输出格式 ('txt' 或 'md')
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'similar_words_results_{timestamp}.{output_format}'

    with open(filename, 'w', encoding='utf-8') as f:
        if output_format == 'md':
            # Markdown 格式
            f.write('# 同义词替换结果\n\n')
            for i, (original, replacements) in enumerate(results.items(), 1):
                f.write(f'## {i}. 原始句子\n')
                f.write(f'{original}\n\n')
                f.write('### 替换结果：\n')
                for j, replaced in enumerate(replacements, 1):
                    f.write(f'{j}. {replaced}\n')
                f.write('\n---\n\n')
        else:
            # TXT 格式
            f.write('同义词替换结果\n')
            f.write('=' * 50 + '\n\n')
            for i, (original, replacements) in enumerate(results.items(), 1):
                f.write(f'{i}. 原始句子：\n')
                f.write(f'{original}\n\n')
                f.write('替换结果：\n')
                for j, replaced in enumerate(replacements, 1):
                    f.write(f'{j}) {replaced}\n')
                f.write('\n' + '-' * 50 + '\n\n')

    return filename


# 使用示例
if __name__ == '__main__':
    test_sentences = [
        '故障部件：泵轴  故障原因：轴弯曲  特征量：RMS、1xRPM幅值、2xRPM幅值、相位差  诊断标准：RMS > 4.5mm/s； 1xRPM幅值占比 > 60%；',
        '故障部件：轴承  故障原因：磨损  特征量：峭度、波形指标  诊断标准：峭度 > 3.5；',
        # 添加更多句子...
    ]

    # 执行批量替换
    results = batch_similar_replace(test_sentences)

    # 保存结果到文件（可选 txt 或 md 格式）
    txt_file = save_results(results, 'txt')
    md_file = save_results(results, 'md')

    print(f'结果已保存到以下文件：')
    print(f'TXT 格式：{txt_file}')
    print(f'Markdown 格式：{md_file}')

    # 打印结果预览
    print('\n结果预览 >>>>>>')
    for original, replacements in results.items():
        print(f'\n原始句子: {original}')
        print('替换结果:')
        for i, replaced in enumerate(replacements, 1):
            print(f'{i}. {replaced}')