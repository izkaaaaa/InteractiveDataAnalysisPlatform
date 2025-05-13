import pandas as pd
import re

def clean_data1(data_top250: pd.DataFrame) -> pd.DataFrame:
    """
    对 data_top250 进行清洗：
    - 只保留：电影名、评分、评分人数、年份
    - 数据类型：
        电影名：str
        评分：float
        评分人数：int
        年份：int
    """
    df = data_top250.copy()


    keep_cols = ['电影名字', '评分', '评分人数', '年份']
    df = df[keep_cols]

    # 类型转换
    df['电影名字'] = df['电影名字'].astype(str)
    df['评分'] = pd.to_numeric(df['评分'], errors='coerce')
    df['评分人数'] = pd.to_numeric(df['评分人数'], errors='coerce', downcast='integer')
    df['年份'] = pd.to_numeric(df['年份'], errors='coerce', downcast='integer')

    # 删除缺失值
    df.dropna(inplace=True)
    #异常值处理
    df = df[(df['评分'] >= 0) & (df['评分'] <= 10)]
    df = df[df['评分人数'] > 0]
    df = df[(df['年份'] >= 1900) & (df['年份'] <= 2025)]
    # 重置索引
    df.reset_index(drop=True, inplace=True)

    return df


def clean_data2(data_country: pd.DataFrame) -> pd.DataFrame:
    """
    清洗 box office 数据：
    - 仅保留需要的列：Dates、Top_10_Gross、Overall_Gross、Releases
    - 转换日期为编号 Dates_number
    - 去掉美元符号、逗号，转为 float 类型
    - 使用线性插值补全缺失值
    """
    df = data_country.copy()

    # 1. 仅保留指定列
    df = df[['Dates', 'Top_10_Gross', 'Overall_Gross', 'Releases']].copy()

    # 2. 生成时间编号列
    df['Dates_number'] = range(1, len(df) + 1)

    # 3. 清洗货币格式为数值
    def clean_money(value):
        if pd.isnull(value):
            return None
        value = re.sub(r'[$,]', '', str(value))
        try:
            return float(value)
        except ValueError:
            return None

    df['Top_10_Gross'] = df['Top_10_Gross'].apply(clean_money)
    df['Overall_Gross'] = df['Overall_Gross'].apply(clean_money)

    # 4. 线性插值
    df['Top_10_Gross'] = df['Top_10_Gross'].interpolate(method='linear')
    df['Overall_Gross'] = df['Overall_Gross'].interpolate(method='linear')
    df['Releases'] = pd.to_numeric(df['Releases'], errors='coerce')
    df['Releases'] = df['Releases'].interpolate(method='linear')

    # 5. 重置索引
    df.reset_index(drop=True, inplace=True)

    return df


def clean_data3(data_comments: pd.DataFrame) -> pd.DataFrame:
    """
    对 data_comments 进行清洗：
    - 去除标点符号
    - 去除停用词（示例词）
    - 删除空或无意义评论
    """
    df = data_comments.copy()

    stop_words = set(['的', '了', '是', '我', '也', '很', '不'])  # 可拓展停用词列表

    def clean_comment(text):
        if pd.isnull(text):
            return ''
        # 去除标点符号
        text = re.sub(r'[^\w\s]', '', text)
        # 去除停用词
        cleaned = ''.join([char for char in text if char not in stop_words])
        return cleaned.strip()

    df['cleaned_comment'] = df['comment'].apply(clean_comment)
    df.dropna(subset=['cleaned_comment'], inplace=True)
    df = df[df['cleaned_comment'].str.len() > 0]

    return df
