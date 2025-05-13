from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from collections import Counter
import numpy as np
from PIL import Image
import base64
import io


def visual3(data_manager, movie_name, font_path='simhei.ttf',
            width=800, height=600, background_color='white',
            max_words=200, mask_image=None):
    """
    生成电影评论词云图并存储到DataManager
    :param data_manager: DataManager实例
    :param movie_name: 电影名称
    :param font_path: 字体文件路径
    :param width: 词云宽度
    :param height: 词云高度
    :param background_color: 背景颜色
    :param max_words: 最大显示词数
    :param mask_image: 词云形状掩码图片路径
    :return: 是否生成成功
    """
    try:
        # 检查数据是否存在
        if movie_name not in data_manager.cleaned_data_comments:
            raise ValueError(f"No cleaned comment data available for {movie_name}")

        # 获取清洗后的评论数据
        df = data_manager.cleaned_data_comments[movie_name]

        # 合并所有评论
        text = ' '.join(df['cleaned_comment'].astype(str))

        # 中文分词
        word_list = jieba.lcut(text)
        word_count = Counter(word_list)

        # 过滤单字和停用词
        filtered_words = {k: v for k, v in word_count.items()
                          if len(k) > 1 and not k.isspace()}

        # 设置词云形状
        mask = None
        if mask_image:
            mask = np.array(Image.open(mask_image))

        # 生成词云
        wc = WordCloud(
            font_path=font_path,
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words,
            colormap='viridis',
            mask=mask,
            contour_width=1,
            contour_color='steelblue'
        ).generate_from_frequencies(filtered_words)

        # 将词云转换为base64编码的图片
        plt.figure(figsize=(12, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
        plt.close()

        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # 存储到DataManager
        data_manager.store_visual3(f"{movie_name}_wordcloud", {
            'type': 'wordcloud',
            'data': img_base64,
            'format': 'png',
            'params': {
                'font_path': font_path,
                'width': width,
                'height': height,
                'max_words': max_words
            }
        })

        return True

    except Exception as e:
        print(f"生成词云时出错: {str(e)}")
        return False