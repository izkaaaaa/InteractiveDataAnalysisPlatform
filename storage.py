import pandas as pd
from cleaning import clean_data1, clean_data2, clean_data3
from analysis import analysis_function
from predict import prediction_function
from visualization import visual3

class DataManager:
    def __init__(self):
        self.data_top250 = None  # 豆瓣TOP250数据
        self.data_country = {}  # 特定国家数据，key: 国家名, value: 对应的数据
        self.data_comments = {}  # 电影评论数据，key: 电影名, value: 对应的数据

        self.cleaned_data_top250 = None  # 清洗后的豆瓣TOP250数据
        self.cleaned_data_country = {}  # 清洗后的特定国家数据
        self.cleaned_data_comments = {}  # 清洗后的电影评论数据

        self.analysis_data = None  # 豆瓣TOP250数据分析结果
        self.predict_data = {}  # 特定国家数据预测结果

        # 扩展豆瓣TOP250可视化存储, key: 图类型, value: 图表对象或参数
        self.visuals_top250_1 = {}  # 三维散点图
        self.visuals_top250_2 = {}  # 平行坐标图
        self.visuals_top250_3 = {}  # 雷达图
        self.visuals_top250_4 = {}  # PCA降维图
        self.visuals_top250_5 = {}  # 箱线图
        self.visuals_country = {}  # 特定国家数据可视化图表数据缓存, key: 图类型, value: 图表对象或参数
        self.visuals_comments = {}  # 电影评论数据词云图数据缓存, key: 图类型, value: 图表对象或参数

    def _check_file_format(self, file_path):
        """检查文件格式是否支持"""
        supported_extensions = ['.csv', '.xls', '.xlsx']
        for ext in supported_extensions:
            if file_path.endswith(ext):
                return True
        return False

    def load_data1(self, file_path):
        """
        加载豆瓣TOP250数据
        :param file_path: 数据文件路径
        """
        if not self._check_file_format(file_path):
            raise ValueError("Unsupported file format. Supported formats are csv, xls, xlsx")
        if file_path.endswith('.csv'):
            self.data_top250 = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            self.data_top250 = pd.read_excel(file_path)
        self.cleaned_data_top250 = self.data_top250.copy()  # 初始化清洗后数据为原始数据副本

    def load_data2(self, country_name, file_path):
        """
        加载特定国家数据
        :param country_name: 国家名
        :param file_path: 数据文件路径
        """
        if not self._check_file_format(file_path):
            raise ValueError("Unsupported file format. Supported formats are csv, xls, xlsx")
        if file_path.endswith('.csv'):
            self.data_country[country_name] = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            self.data_country[country_name] = pd.read_excel(file_path)
        self.cleaned_data_country[country_name] = self.data_country[country_name].copy()  # 初始化清洗后数据为原始数据副本

    def load_data3(self, movie_name, file_path):
        """
        加载电影评论数据
        :param movie_name: 电影名
        :param file_path: 数据文件路径
        """
        if not self._check_file_format(file_path):
            raise ValueError("Unsupported file format. Supported formats are csv, xls, xlsx")
        if file_path.endswith('.csv'):
            self.data_comments[movie_name] = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            self.data_comments[movie_name] = pd.read_excel(file_path)
        self.cleaned_data_comments[movie_name] = self.data_comments[movie_name].copy()  # 初始化清洗后数据为原始数据副本

    def clean_data1(self):
        """
        清洗豆瓣TOP250数据
        """
        if self.data_top250 is not None:
            self.cleaned_data_top250 = clean_data1(self.data_top250)
        else:
            raise ValueError("No TOP250 data loaded yet. Please load data first.")

    def clean_data2(self, country_name):
        """
        清洗特定国家数据
        :param country_name: 国家名
        """
        if country_name in self.data_country:
            self.cleaned_data_country[country_name] = clean_data2(self.data_country[country_name])
        else:
            raise ValueError(f"No data loaded for {country_name}. Please load data first.")

    def clean_data3(self, movie_name):
        """
        清洗电影评论数据
        :param movie_name: 电影名
        """
        if movie_name in self.data_comments:
            self.cleaned_data_comments[movie_name] = clean_data3(self.data_comments[movie_name])
        else:
            raise ValueError(f"No data loaded for {movie_name}. Please load data first.")

    def analyze_data(self):
        """
        分析豆瓣TOP250数据
        """
        if self.cleaned_data_top250 is not None:
            self.analysis_data = analysis_function(self.cleaned_data_top250)
        else:
            raise ValueError("No cleaned TOP250 data available. Please clean data first.")

    def predict_data(self, country_name):
        """
        预测特定国家数据
        :param country_name: 国家名
        """
        if country_name in self.cleaned_data_country:
            self.predict_data[country_name] = prediction_function(self.cleaned_data_country[country_name])
        else:
            raise ValueError(f"No cleaned data available for {country_name}. Please clean data first.")


    def export_data_top250(self):
        """导出豆瓣TOP250数据"""
        return self.data_top250.copy() if self.data_top250 is not None else None

    def export_data_country(self, country_name):
        """导出特定国家数据"""
        return self.data_country.get(country_name).copy() if country_name in self.data_country else None

    def export_data_comments(self, movie_name):
        """导出电影评论数据"""
        return self.data_comments.get(movie_name).copy() if movie_name in self.data_comments else None

    def export_cleaned_data_top250(self):
        """导出清洗后的豆瓣TOP250数据"""
        return self.cleaned_data_top250.copy() if self.cleaned_data_top250 is not None else None

    def export_cleaned_data_country(self, country_name):
        """导出清洗后的特定国家数据"""
        return self.cleaned_data_country.get(country_name).copy() if country_name in self.cleaned_data_country else None

    def export_cleaned_data_comments(self, movie_name):
        """导出清洗后的电影评论数据"""
        return self.cleaned_data_comments.get(movie_name).copy() if movie_name in self.cleaned_data_comments else None

    def export_analysis_result_top250(self):
        """导出豆瓣TOP250数据分析结果"""
        return self.analysis_data.copy() if self.analysis_data is not None else None

    def export_prediction_result_country(self, country_name):
        """导出特定国家数据预测结果"""
        return self.predict_data.get(country_name).copy() if country_name in self.predict_data else None

        # 新增可视化存储和获取方法

    def store_visual1_1(self, vis_type, visual_obj):
        """存储三维散点图"""
        self.visuals_top250_1[vis_type] = visual_obj

    def get_visual1_1(self, vis_type):
        """获取三维散点图"""
        return self.visuals_top250_1.get(vis_type)

    def store_visual1_2(self, vis_type, visual_obj):
        """存储平行坐标图"""
        self.visuals_top250_2[vis_type] = visual_obj

    def get_visual1_2(self, vis_type):
        """获取平行坐标图"""
        return self.visuals_top250_2.get(vis_type)

    def store_visual1_3(self, vis_type, visual_obj):
        """存储雷达图"""
        self.visuals_top250_3[vis_type] = visual_obj

    def get_visual1_3(self, vis_type):
        """获取雷达图"""
        return self.visuals_top250_3.get(vis_type)

    def store_visual1_4(self, vis_type, visual_obj):
        """存储PCA降维图"""
        self.visuals_top250_4[vis_type] = visual_obj

    def get_visual1_4(self, vis_type):
        """获取PCA降维图"""
        return self.visuals_top250_4.get(vis_type)

    def store_visual1_5(self, vis_type, visual_obj):
        """存储箱线图"""
        self.visuals_top250_5[vis_type] = visual_obj

    def get_visual1_5(self, vis_type):
        """获取箱线图"""
        return self.visuals_top250_5.get(vis_type)
    def store_visual2(self, vis_type, visual_obj):
        """
        存储特定国家数据可视化图表对象
        :param vis_type: 图表类型
        :param visual_obj: 图表对象或参数
        """
        self.visuals_country[vis_type] = visual_obj

    def get_visual2(self, vis_type):
        """
        获取特定国家数据可视化指定类型的图表对象
        :param vis_type: 图表类型
        """
        return self.visuals_country.get(vis_type)

    def store_visual3(self, vis_type, visual_obj):
        """
        存储电影评论数据词云图图表对象
        :param vis_type: 图表类型
        :param visual_obj: 图表对象或参数
        """
        self.visuals_comments[vis_type] = visual_obj

    def get_visual3(self, vis_type):
        """
        获取电影评论数据词云图指定类型的图表对象
        :param vis_type: 图表类型
        """
        return self.visuals_comments.get(vis_type)
