from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from storage import DataManager  # 确保你已经导入了DataManager类
import pandas as pd
from io import BytesIO

data_manager = DataManager()

app = Flask(__name__, template_folder='templates')

@app.route('/')
def main():
    return render_template('index.html')

# ================== API Analyze Block ==================

@app.route('/api_analyze', methods=['GET'])
def call_api_analyze():
    # 分析豆瓣TOP250 - 静态文件路径
    data_manager.load_data1('data/douban_top250.csv')
    data_manager.clean_data1()
    data_manager.analyze_data()
    return data_manager.visual1() 

@app.route('/export_analyze', methods=['GET'])
def export_analyze():
    if data_manager.cleaned_data_top250 is None:
        return jsonify({'error': '暂无可用的分析结果，请先完成分析操作'}), 400
    data_manager.load_data1('data/douban_top250.csv')
    data_manager.clean_data1()
    data_manager.analyze_data()
    df = data_manager.export_analysis_result_top250()

    csv_bytes = BytesIO()
    df.to_csv(csv_bytes, index=False, encoding='utf-8-sig')
    csv_bytes.seek(0)

    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name='豆瓣top250_分析结果.csv'
    )

# ================== API Predict Block ==================

@app.route('/api_predict', methods=['GET'])
def call_api_predict():
    country = request.args.get('country', '中国')  # 默认为中国
    file_path = f'data/country_data_{country}.csv'
    data_manager.load_data2(country, file_path)
    data_manager.clean_data2(country)
    data_manager.predict_data(country)
    return data_manager.visual2() 

@app.route('/export_predict', methods=['GET'])
def export_predict():
    country = request.args.get('country', '中国')
    file_path = f'data/country_data_{country}.csv'
    data_manager.load_data2(country, file_path)
    data_manager.clean_data2(country)
    data_manager.predict_data(country)
    df = data_manager.export_prediction_result_country(country)

    if df is None:
        return jsonify({'error': f'暂无 {country} 的预测结果，请先完成预测操作'}), 400

    csv_bytes = BytesIO()
    df.to_csv(csv_bytes, index=False, encoding='utf-8-sig')
    csv_bytes.seek(0)

    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'票房预测_{country}_分析结果.csv'
    )

# ================== API Comments Block ==================

@app.route('/api_comments', methods=['GET'])
def call_api_comments():
    movie = request.args.get('movie', '肖申克的救赎')
    file_path = f'data/comments_{movie}.csv'
    data_manager.load_data3(movie, file_path)
    data_manager.clean_data3(movie)
    data_manager.analyze_data3(movie) 
    return data_manager.visual3()  

@app.route('/export_comments', methods=['GET'])
def export_comments():
    movie = request.args.get('movie', '肖申克的救赎')
    file_path = f'data/comments_{movie}.csv'
    data_manager.load_data3(movie, file_path)
    data_manager.clean_data3(movie)
    data_manager.analyze_data3(movie) 
    df = data_manager.export_analysis_result_comments(movie)

    if df is None:
        return jsonify({'error': f'暂无 {movie} 的评论分析结果，请先完成分析操作'}), 400

    csv_bytes = BytesIO()
    df.to_csv(csv_bytes, index=False, encoding='utf-8-sig')
    csv_bytes.seek(0)

    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'评论分析_{movie}_词频统计.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
