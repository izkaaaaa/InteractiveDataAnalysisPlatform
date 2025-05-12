from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

def upload_data(file_path):
    """
    从文件路径读取数据并返回DataFrame
    :param file_path: 文件路径
    :return: pandas.DataFrame
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Supported formats are csv, xls, xlsx")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # 如果用户没有选择文件，浏览器也会提交一个空文件
        if file.filename == '':
            return 'No selected file'
        if file:
            try:
                # 保存文件到临时位置
                file_path = 'temp_file.' + file.filename.split('.')[-1]
                file.save(file_path)
                # 读取文件数据
                df = upload_data(file_path)
                return f"File uploaded successfully. Data shape: {df.shape}"
            except ValueError as e:
                return str(e)
    # 渲染 HTML 表单
    html = '''
    <!doctype html>
    <html>
    <head>
        <title>Upload File</title>
    </head>
    <body>
        <h1>Upload a CSV, XLS or XLSX file</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)