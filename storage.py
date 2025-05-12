import pandas as pd


class DataManager:
    def __init__(self):
        self.raw_data = None  # 原始上传的数据
        self.cleaned_data = None  # 清洗后的数据
        self.analysis_result = None  # 分析结果（如类标签、预测结果等）
        self.visuals = {}  # 图表数据缓存, key: 图类型, value: 图表对象或参数

    def load_data(self, file_path):
        """
        加载原始数据
        :param file_path: 数据文件路径
        """
        if file_path.endswith('.csv'):
            self.raw_data = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            self.raw_data = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Supported formats are csv, xls, xlsx")
        self.cleaned_data = self.raw_data.copy()  # 初始化清洗后数据为原始数据副本

    def clean_data(self, cleaning_function):
        """
        清洗数据
        :param cleaning_function: 数据清洗函数，需返回清洗后的DataFrame
        """
        if self.raw_data is not None:
            self.cleaned_data = cleaning_function(self.raw_data)
        else:
            raise ValueError("No raw data loaded yet. Please load data first.")

    def analyze_data(self, analysis_function):
        """
        分析数据
        :param analysis_function: 数据分析函数，需返回分析结果的DataFrame
        """
        if self.cleaned_data is not None:
            self.analysis_result = analysis_function(self.cleaned_data)
        else:
            raise ValueError("No cleaned data available. Please clean data first.")

    def export_raw_data(self):
        """导出原始数据"""
        return self.raw_data.copy() if self.raw_data is not None else None

    def export_cleaned_data(self):
        """导出清洗后的数据"""
        return self.cleaned_data.copy() if self.cleaned_data is not None else None

    def export_analysis_result(self):
        """导出分析结果"""
        return self.analysis_result.copy() if self.analysis_result is not None else None

    def store_visual(self, vis_type, visual_obj):
        """
        存储图表对象
        :param vis_type: 图表类型
        :param visual_obj: 图表对象或参数
        """
        self.visuals[vis_type] = visual_obj

    def get_visual(self, vis_type):
        """
        获取指定类型的图表对象
        :param vis_type: 图表类型
        """
        return self.visuals.get(vis_type)