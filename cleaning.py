import pandas as pd
import re
from calendar import month_abbr

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
    清洗 data_country 数据，用于预测功能：
    - 仅保留 Dates, Top_10_Gross, Overall_Gross, Releases 三列
    - 移除美元符号和千位分隔符，转为数值
    - 将时间段按实际顺序编号为 Dates_number
    - 缺失值用线性插值填充

    返回清洗后的 pandas.DataFrame
    """
    df = data_country.copy()

    # 1. 保留所需列
    df = df[['Dates', 'Top_10_Gross', 'Overall_Gross', 'Releases']].copy()

    # 2. 清洗货币列
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

    # 3. Releases 数值化
    df['Releases'] = pd.to_numeric(df['Releases'], errors='coerce')

    # 4. 提取起始月和日用于排序
    def extract_month_day(date_str):
        match = re.match(r'([A-Za-z]+)\s+(\d+)', str(date_str))
        if match:
            month_str, day = match.groups()
            try:
                month_num = list(month_abbr).index(month_str[:3])
                return month_num, int(day)
            except ValueError:
                return 0, 0
        return 0, 0

    df[['Month', 'Day']] = df['Dates'].apply(lambda x: pd.Series(extract_month_day(x)))

    # 5. 按时间排序并生成编号
    df.sort_values(by=['Month', 'Day'], inplace=True)
    df['Dates_number'] = range(1, len(df) + 1)
    df.drop(columns=['Month', 'Day'], inplace=True)

    # 6. 用线性插值填补缺失值
    df['Top_10_Gross'] = df['Top_10_Gross'].interpolate(method='linear')
    df['Overall_Gross'] = df['Overall_Gross'].interpolate(method='linear')
    df['Releases'] = df['Releases'].interpolate(method='linear')

    df.reset_index(drop=True, inplace=True)
    return df


def clean_data3(data_comments: pd.DataFrame) -> pd.DataFrame:
    """
    对 data_comments 进行清洗：
    - 去除标点符号
    - 去除停用词（示例词）··
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
