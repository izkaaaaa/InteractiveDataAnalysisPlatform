from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
import io
from io import BytesIO
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from sklearn.decomposition import PCA

def visual1_1(data_manager):
    """生成三维散点图"""
    df = data_manager.export_analysis_result_top250()['clustered_data']

    fig = px.scatter_3d(
        df,
        x='评分',
        y='评分人数',
        z='年份',
        color='cluster',
        hover_name='电影名字',
        title='豆瓣TOP250三维聚类分布',
        opacity=0.7,
        color_continuous_scale=px.colors.sequential.Viridis
    )

    # 转换为base64存储
    img_bytes = fig.to_image(format="png")
    img_str = base64.b64encode(img_bytes).decode('utf-8')
    data_manager.store_visual1_1('3d_scatter', img_str)
    return img_str


def visual1_2(data_manager):
    """生成平行坐标图"""
    df = data_manager.export_analysis_result_top250()['clustered_data']

    fig = px.parallel_coordinates(
        df,
        color='cluster',
        dimensions=['评分', '评分人数', '年份'],
        title='豆瓣TOP250平行坐标图',
        color_continuous_scale=px.colors.sequential.Viridis
    )

    img_bytes = fig.to_image(format="png")
    img_str = base64.b64encode(img_bytes).decode('utf-8')
    data_manager.store_visual1_2('parallel_coords', img_str)
    return img_str


def visual1_3(data_manager):
    """生成雷达图"""
    cluster_centers = data_manager.export_analysis_result_top250()['cluster_centers']

    features = ['评分', '评分人数', '年份']
    fig = go.Figure()

    for i in range(cluster_centers.shape[0]):
        fig.add_trace(go.Scatterpolar(
            r=np.append(cluster_centers[i], cluster_centers[i][0]),
            theta=np.append(features, features[0]),
            fill='toself',
            name=f'Cluster {i}'
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title='聚类中心雷达图'
    )

    img_bytes = fig.to_image(format="png")
    img_str = base64.b64encode(img_bytes).decode('utf-8')
    data_manager.store_visual1_3('radar_chart', img_str)
    return img_str


def visual1_4(data_manager):
    """生成PCA降维图"""
    result = data_manager.export_analysis_result_top250()
    scaled_data = result['model']._fit_X

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        pca_result[:, 0],
        pca_result[:, 1],
        c=result['clustered_data']['cluster'],
        cmap='viridis',
        alpha=0.6
    )
    plt.colorbar(scatter)
    plt.title('PCA降维可视化 (解释方差: {:.2f})'.format(pca.explained_variance_ratio_.sum()))

    # 保存为base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    data_manager.store_visual1_4('pca_plot', img_str)
    return img_str


def visual1_5(data_manager):
    """生成箱线图"""
    df = data_manager.export_analysis_result_top250()['clustered_data']

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for i, col in enumerate(['评分', '评分人数', '年份']):
        sns.boxplot(x='cluster', y=col, data=df, ax=axes[i])
        axes[i].set_title(f'各簇的{col}分布')

    plt.tight_layout()

    # 保存为base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    data_manager.store_visual1_5('box_plot', img_str)
    return img_str
def visual2(data_manager, country_name, historical_points=10):
    """
    生成特定国家电影票房历史数据与预测数据的对比折线图
    使用同色系颜色区分历史/预测数据，并用实线/虚线加强区分

    参数:
        data_manager: DataManager实例
        country_name: 国家名称(如"中国")
        historical_points: 显示的历史数据点数(默认10)
    """
    # 获取数据
    cleaned_data = data_manager.export_cleaned_data_country(country_name)
    predicted_data = data_manager.export_prediction_result_country(country_name)

    if cleaned_data is None or predicted_data is None:
        raise ValueError(f"找不到国家 {country_name} 的数据")

    # 创建画布
    plt.figure(figsize=(14, 7))

    # 时间轴处理
    if 'Year' in cleaned_data.columns:
        # 使用实际年份
        historical_time = cleaned_data['Year'].iloc[-historical_points:].values
        last_year = historical_time[-1]
        predicted_time = np.arange(last_year + 1, last_year + 1 + 10)  # 预测未来10年
    else:
        # 使用索引作为时间点
        historical_time = np.arange(-historical_points, 0)
        predicted_time = np.arange(0, 10)

    # 定义同色系配色方案 (历史数据用深色，预测数据用浅色)
    color_palette = {
        'Top_10_Gross': ('#1f77b4', '#8ab4d8'),  # 蓝色系
        'Overall_Gross': ('#2ca02c', '#98df8a'),  # 绿色系
        'Releases': ('#d62728', '#ff9896')  # 红色系
    }

    # 绘制三条指标线
    for metric in ['Top_10_Gross', 'Overall_Gross', 'Releases']:
        # 获取对应颜色
        hist_color, pred_color = color_palette[metric]

        # 历史数据 (深色实线)
        hist_values = cleaned_data[metric].iloc[-historical_points:].values
        plt.plot(historical_time, hist_values,
                 color=hist_color, linestyle='-', linewidth=2.5,
                 marker='o', markersize=6, markerfacecolor=hist_color,
                 label=f'{metric} (历史)')

        # 预测数据 (浅色虚线)
        pred_values = predicted_data[metric][:10]  # 取前10个预测点
        plt.plot(predicted_time, pred_values,
                 color=pred_color, linestyle='--', linewidth=2,
                 marker='o', markersize=6, markerfacecolor=pred_color,
                 label=f'{metric} (预测)')

        # 连接线 (半透明)
        plt.plot([historical_time[-1], predicted_time[0]],
                 [hist_values[-1], pred_values[0]],
                 color=pred_color, linestyle='--', alpha=0.5)

    # 图表装饰
    plt.title(f'{country_name}电影市场趋势预测', fontsize=16, pad=20)
    plt.xlabel('年份' if 'Year' in cleaned_data.columns else '时间周期', fontsize=12)
    plt.ylabel('数值', fontsize=12)

    # 优化图例
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # 网格和边框
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # 保存图像
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=120, bbox_inches='tight')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    # 存储并清理
    data_manager.store_visual2('prediction_comparison', img_str)
    plt.close()
def visual3(data_manager, movie_name, width=800, height=600,
            background_color='white', max_words=200, colormap='viridis'):
    """
    根据已清洗的评论数据生成词云并存储到DataManager
    :param data_manager: DataManager实例
    :param movie_name: 电影名称
    :param width: 词云宽度
    :param height: 词云高度
    :param background_color: 背景颜色
    :param max_words: 最大显示词数
    :param colormap: 颜色映射
    :return: 是否生成成功
    """
    try:
        # 检查数据是否存在
        if movie_name not in data_manager.cleaned_data_comments:
            raise ValueError(f"No cleaned comment data available for {movie_name}")

        # 获取清洗后的评论数据
        df = data_manager.cleaned_data_comments[movie_name]

        # 合并所有评论文本
        text = ' '.join(df['cleaned_comment'].astype(str))

        # 生成词云
        wc = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words,
            colormap=colormap
        ).generate(text)

        # 将词云转换为base64编码的图片
        plt.figure(figsize=(10, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')

        # 保存到内存缓冲区
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0, dpi=100)
        plt.close()

        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # 存储到DataManager
        data_manager.store_visual3(f"{movie_name}_wordcloud", {
            'type': 'wordcloud',
            'data': img_base64,
            'format': 'png',
            'params': {
                'width': width,
                'height': height,
                'max_words': max_words
            }
        })

        return True

    except Exception as e:
        print(f"生成词云时出错: {str(e)}")
        return False
