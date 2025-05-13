import pandas as pd

import re


def clean_data1(data_top250: pd.DataFrame) -> pd.DataFrame:
    """
    对豆瓣 Top250 数据进行清洗
    - 删除缺失值严重的行
    - 去除无效列（如链接、空白字段）
    - 统一数据格式（如评分转为 float）
    """
    df = data_top250.copy()

    # 删除完全空的列
    df.dropna(axis=1, how='all', inplace=True)

    # 去除无用列（示例）
    df.drop(columns=['评分'], errors='ignore', inplace=True)

    # 清理评分列（示例）
    df['评分'] = pd.to_numeric(df['评分'], errors='coerce')

    # 删除缺失值严重的行
    df.dropna(thresh=int(0.7 * len(df.columns)), inplace=True)

    return df


def clean_data2(data_country: pd.DataFrame) -> pd.DataFrame:
    """
    对国家相关数据进行插值补全
    - 插值方法：线性插值 / 样条插值（可选）
    """
    df = data_country.copy()

    # 假设以年份为索引（样条插值适合时间序列）
    df.interpolate(method='linear', inplace=True)

    return df


def clean_data3(data_comments: pd.DataFrame) -> pd.DataFrame:
    """
    对评论数据进行清洗
    - 删除短于特定长度的评论
    - 去除停用词、无意义符号
    - 情感分析可选（可借助情感词典）
    """
    df = data_comments.copy()

    def clean_comment(text):
        if pd.isnull(text): return ''
        # 去除特殊符号
        text = re.sub(r'[^\w\s]', '', text)
        # 去除无意义短语（可引入停用词列表）
        stop_words = set(['的', '了', '是', '我', '也', '很', '不'])  # 示例
        text = ''.join([w for w in text if w not in stop_words])
        return text

    df['cleaned_comment'] = df['comment'].apply(clean_comment)
    df.dropna(subset=['cleaned_comment'], inplace=True)

    return df


def clean_all(data_top250, data_country, data_comments):
    cleaned_data_top250 = clean_data1(data_top250)
    cleaned_data_country = clean_data2(data_country)
    cleaned_data_comments = clean_data3(data_comments)

    return {
        'cleaned_data_top250': cleaned_data_top250,
        'cleaned_data_country': cleaned_data_country,
        'cleaned_data_comments': cleaned_data_comments
    }
