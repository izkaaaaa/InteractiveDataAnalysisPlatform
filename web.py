from flask import Flask, request, jsonify, send_file, render_template
from storage import DataManager
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# 主页，显示上传按钮
@app.route('/')
def main():
    return render_template('index.html')

# API接口：处理文件上传
@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 保存文件到临时位置
        filepath = 'tempuploadedfile.' + file.filename.split('.')[-1]
        file.save(filepath)

        # 初始化数据管理器
        datamanager = DataManager()
        datamanager.load_data(filepath)

        # 获取数据信息
        df = datamanager.export_raw_data()

        # 返回成功响应
        return jsonify({
            "success": True,
            "message": "File uploaded and processed successfully",
            "data_shape": str(df.shape),
            "columns": list(df.columns)
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# API接口：获取分析结果
@app.route('/api/analyze', methods=['GET'])
def api_analyze():
    try:
        # 初始化数据管理器
        datamanager = DataManager()

        datamanager.analyze()

        # 返回成功响应
        return jsonify({
            "success": True,
            "message": "Analysis completed successfully"
        }), 200

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

# API接口：显示图片
@app.route('/api/show_image/<vistype>', methods=['GET'])
def api_show_image(vistype):
    try:
        # 初始化数据管理器
        datamanager = DataManager()
        # 获取指定类型的图表对象
        image_path = datamanager.get_visual(vistype)

        # 返回图片文件
        return send_file(image_path, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": f"Image display failed: {str(e)}"}), 500

# API接口：导出数据
@app.route('/api/export/<datatype>', methods=['GET'])
def api_export(datatype):
    try:
        # 初始化数据管理器
        datamanager = DataManager()
        # 根据类型导出数据
        if datatype == 'raw':
            data = datamanager.export_raw_data()
        elif datatype == 'cleaned':
            data = datamanager.export_cleaned_data()
        elif datatype == 'result':
            data = datamanager.export_analysis_result()
        else:
            return jsonify({"error": "Invalid data type"}), 400

        # 将数据转换为CSV格式并返回文件
        csvfile = BytesIO()
        data.to_csv(csvfile, index=False)
        csvfile.seek(0)
        return send_file(csvfile, mimetype='text/csv', as_attachment=True, download_name=f'{datatype}.csv')

    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
