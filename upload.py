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

    try:
        # 保存文件到临时位置
        file_path = 'temp_uploaded_file.' + file.filename.split('.')[-1]
        file.save(file_path)

        # 初始化数据管理器
        data_manager = DataManager()
        data_manager.load_data(file_path)

        # 获取数据信息
        df = data_manager.export_raw_data()

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
