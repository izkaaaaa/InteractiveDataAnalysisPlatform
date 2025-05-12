from flask import Flask, request, jsonify
from storage import DataManager

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    """API接口：处理文件上传"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 获取数据类型参数
    data_type = request.form.get('data_type')
    if data_type not in ['data_top250', 'data_country', 'data_comments']:
        return jsonify({"error": "Invalid data type. Supported types are 'data_top250', 'data_country', 'data_comments'"}), 400

    try:
        # 保存文件到临时位置
        file_path = 'temp_uploaded_file.' + file.filename.split('.')[-1]
        file.save(file_path)

        # 初始化数据管理器
        data_manager = DataManager()

        if data_type == 'data_top250':
            data_manager.load_data1(file_path)
            df = data_manager.export_data_top250()
        elif data_type == 'data_country':
            country_name = request.form.get('country_name')
            if not country_name:
                return jsonify({"error": "Country name is required for 'data_country' type"}), 400
            data_manager.load_data2(country_name, file_path)
            df = data_manager.export_data_country(country_name)
        elif data_type == 'data_comments':
            movie_name = request.form.get('movie_name')
            if not movie_name:
                return jsonify({"error": "Movie name is required for 'data_comments' type"}), 400
            data_manager.load_data3(movie_name, file_path)
            df = data_manager.export_data_comments(movie_name)

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

if __name__ == '__main__':
    app.run(debug=True)
