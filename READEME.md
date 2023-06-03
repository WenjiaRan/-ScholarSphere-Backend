项目的根目录应该为`./Scholarship`, 所以请在`./Scholarship`打开pycharm
在`./Scholarship`目录下用powershell运行下面的代码创建虚拟环境并运行代码(操作系统需要是windows)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```


论文上传命令使用方法：
```
python manage.py import_pdf article/articleList
```
所有需要上传的pdf文件以.pdf后缀形式储存在article/articleList目录下