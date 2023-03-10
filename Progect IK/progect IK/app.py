from flask import Flask, render_template, request, redirect    #pip install Flask
import cv2                                           #pip install opencv-python
from flask_cors import CORS                          #pip install Flask-Cors
import pandas as pd                                  #pip install pandas
import time                                          #pip install openpyxl


#Сотрите Ivan Kizikin из таблицы Excel и добавьте его снова через http://127.0.0.1:5000/        pls :)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


cors = CORS(app, resources={r"/uploader": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

result = ''



@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():

    file = request.files.get('file')
    print(f'Got file: {request.files}')

    file.save('./photo/original.png')

    
    img = cv2.imread('photo/original.png')
    detector = cv2.QRCodeDetector()
    data, bbox, temp = detector.detectAndDecode(img)
    print(data)

    ep_time = time.time()
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ep_time))

    new = [data, time_now]

    df = pd.read_excel('names.xlsx')
    print(df['ФИО'])

    if len(df[df['ФИО'] == data]) != 0:
        print('#######################################################################################                 YYYYYYYYYYYYYYYYY')
        df1 = pd.read_excel('test.xlsx')
        df1 = df1.append(pd.Series (new, index=df1.columns [: len (new)]), ignore_index= True)
        df1.to_excel('test.xlsx', index=False)
        # return redirect('/data')
    else:
        print('//////////////////////////////////////////////////////////////////////////////////////////               NONONONONONONONONO')
        # return redirect('/no_data')

@app.route('/data')
def data():
    return render_template('auth.html')

@app.route('/no_data')
def no_data():
    return render_template('not_auth.html')


    #     result = 'success'        
    #     print('all OK' )
    # else: 
    #     result = 'false'
    #     print('U are not in shell')

    # return render_template('index1.html', result=result)


    






@app.route('/', methods = ['GET', 'POST'])
def new():

    if request.method == 'POST':


        name = request.form['name']

        new = [name]
        # new = [name, time_now]


        df = pd.read_excel('names.xlsx')
        print(type(name))

        df = df.append(pd.Series (new, index=df.columns [: len (new)]), ignore_index= True)


        df.to_excel('names.xlsx', index=False)
        
    return render_template('new_people.html')






if __name__ == "__main__":
    app.run(debug=True)
