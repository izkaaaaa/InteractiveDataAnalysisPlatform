from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from storage import DataManager
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
    # 路径加载豆瓣TOP250数据
    data_manager.load_data1('path/to/douban_top250.csv')
    data_manager.clean_data1()
    data_manager.analyze_data()
    return data_manager.visual1()

@app.route('/export_analyze', methods=['GET'])
def export_analyze():
    df = data_manager.export_analysis_result_top250()
    if df is None:
        return jsonify({'error': '暂无可用的分析结果，请先完成分析操作'}), 400

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
    country = request.args.get('country', 'China')  # 默认为中国
    data_manager.load_data2(country, f'path/to/country_data_{country}.csv')
    data_manager.clean_data2(country)
    data_manager.predict_data(country)
    return data_manager.visual2()

@app.route('/export_predict', methods=['GET'])
def export_predict():
    country = request.args.get('country', 'China')
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
    data_manager.load_data3(movie, f'path/to/comments_{movie}.csv')
    data_manager.clean_data3(movie)
    data_manager.analyze_data3() 
    return data_manager.visual3()

@app.route('/export_comments', methods=['GET'])
def export_comments():
    movie = request.args.get('movie', '肖申克的救赎')
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
