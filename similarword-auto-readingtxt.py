from nlpcda import Similarword
from datetime import datetime


def read_formatted_text(file_path):
    """
    读取格式化的文本文件，提取故障描述句子

    参数:
    file_path: str, 文本文件路径

    返回:
    list: 故障描述句子列表
    """
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # 只提取包含"故障部件"的行
            if '故障部件：' in line:
                sentences.append(line.strip())
    return sentences


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
            for original, replacements in results.items():
                f.write(f'### 原始句子\n')
                f.write(f'{original}\n\n')
                f.write('### 替换结果：\n')
                for replaced in replacements:
                    f.write(f'- {replaced}\n')
                f.write('\n')
        else:
            # TXT 格式
            for original, replacements in results.items():
                f.write(f'{original}\n')  # 直接写入原始句子
                for replaced in replacements:
                    f.write(f'{replaced}\n')  # 直接写入替换后的句子
                f.write('\n')  # 每个原始句子与替换结果之间空一行

    return filename


def main():
    """
    主函数：自动读取文本并进行同义词替换
    """
    # 配置参数
    input_file = 'equipment_faults_20250116_135636.txt'  # 替换为实际的输入文件名
    create_num = 10  # 每个句子生成的替换结果数量
    change_rate = 0.2  # 词语被替换的概率

    try:
        # 读取格式化文本文件
        print(f'正在读取文件: {input_file}')
        sentences = read_formatted_text(input_file)
        print(f'成功读取 {len(sentences)} 条故障描述')

        # 执行批量替换
        print('正在进行同义词替换...')
        results = batch_similar_replace(sentences, create_num, change_rate)

        # 保存结果
        txt_file = save_results(results, 'txt')
        md_file = save_results(results, 'md')

        print(f'\n处理完成！结果已保存到以下文件：')
        print(f'TXT 格式：{txt_file}')
        print(f'Markdown 格式：{md_file}')

        # 打印预览
        print('\n结果预览（第一条）：')
        first_sentence = next(iter(results))
        print(f'\n原始句子: {first_sentence}')
        print('替换结果:')
        for replaced in results[first_sentence][:3]:
            print(f'- {replaced}')

    except Exception as e:
        print(f'处理过程中出现错误：{str(e)}')


if __name__ == '__main__':
    main()
