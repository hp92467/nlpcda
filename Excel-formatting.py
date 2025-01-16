import pandas as pd
from datetime import datetime


def format_fault_description(row):
    """
    将单行故障信息格式化为可读性好的句子
    """
    return (f"故障部件：{row['部件']}  "
            f"故障原因：{row['故障模式']}  "
            f"特征量：{row['信号特征量']}  "
            f"诊断标准：{row['诊断标准']}")


def process_equipment_faults(excel_path):
    """
    处理设备故障Excel文件并生成格式化文档

    参数:
    excel_path: str, Excel文件路径

    返回:
    list: 格式化后的故障描述列表
    """
    # 读取Excel文件
    df = pd.read_excel(excel_path)

    # 确保所需列都存在
    required_columns = ['部件', '故障模式', '信号特征量', '诊断标准']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Excel文件必须包含以下列: {', '.join(required_columns)}")

    # 按部件分组处理
    formatted_descriptions = []
    for part in df['部件'].unique():
        part_data = df[df['部件'] == part]
        for _, row in part_data.iterrows():
            formatted_descriptions.append(format_fault_description(row))

    return formatted_descriptions


def save_formatted_results(descriptions, output_format='txt'):
    """
    保存格式化的故障描述到文件

    参数:
    descriptions: list, 格式化后的故障描述列表
    output_format: str, 输出格式 ('txt' 或 'md')
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'equipment_faults_{timestamp}.{output_format}'

    with open(filename, 'w', encoding='utf-8') as f:
        if output_format == 'md':
            # Markdown 格式
            f.write('# 设备故障描述汇总\n\n')
            for i, desc in enumerate(descriptions, 1):
                f.write(f'## {i}. 故障描述\n')
                f.write(f'{desc}\n\n')
                f.write('---\n\n')
        else:
            # TXT 格式
            f.write('设备故障描述汇总\n')
            f.write('=' * 50 + '\n\n')
            for i, desc in enumerate(descriptions, 1):
                f.write(f'{i}. 故障描述：\n')
                f.write(f'{desc}\n\n')
                f.write('-' * 50 + '\n\n')

    return filename


def main():
    """
    主函数
    """
    # Excel文件路径
    excel_path = 'F:\\pycharmprojects\\nlpcda\\pump-trouble.xlsx'  # 替换为实际的Excel文件路径

    try:
        # 处理Excel文件
        descriptions = process_equipment_faults(excel_path)

        # 保存结果（同时生成txt和md格式）
        txt_file = save_formatted_results(descriptions, 'txt')
        md_file = save_formatted_results(descriptions, 'md')

        print(f'处理完成！共处理 {len(descriptions)} 条故障记录')
        print(f'结果已保存到以下文件：')
        print(f'TXT 格式：{txt_file}')
        print(f'Markdown 格式：{md_file}')

        # 打印预览
        print('\n结果预览（前3条）：')
        for i, desc in enumerate(descriptions[:3], 1):
            print(f'\n{i}. {desc}')

    except Exception as e:
        print(f'处理过程中出现错误：{str(e)}')


if __name__ == '__main__':
    main()