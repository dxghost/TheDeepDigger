from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import Searcher
import time


app = Flask(__name__)
data = None
result_data = ''
@app.route('/', methods = ['POST', 'GET'])
def main():
    global data
    global result_data
    if request.method == 'POST':
        start = time.time()
        data = request.form['search']
        if not data:
            return render_template('searchforms.html')        
        search_obj = Searcher.Searcher()
        result_data = search_obj.general_search(data)

        if len(result_data[0]) == 0:
            return render_template('no_result.html',data=data)
        number = len(result_data)
        end = time.time()
        timer = round(end - start,5) 
        return render_template('result.html', has_result = True,name = data,result= result_data,number=number,timer=timer)
    return render_template('searchforms.html')

@app.route('/imagesearch',methods=['POST', 'GET'])
def picresult():
    global data
    global result_data
    if request.method == 'POST':
        data = request.form['search']
        search_obj = Searcher.Searcher()
        result_data = search_obj.general_search(data)
        return render_template('result_pic.html', data=data, result_data=result_data)    
    return render_template('result_pic.html', data=data, result_data=result_data)



@app.route('/result', methods = ['POST', 'GET'])
def result():    
    global result_data
    global data
    name = data
    '''
    if not name:
        has_result = False
    else:
        has_result = True
    print(result_data)
    '''
    if request.method == 'POST':
        data = request.form['search']            
        if  data:
            has_result = True
            search_obj = Searcher.Searcher()
            result_data = search_obj.general_search(data)
            return render_template('result.html',name = data,has_result=has_result, result= result_data)
            
    return render_template('result.html', name=name, has_result=True, result= result_data)

@app.route('/preview/<int:id>', methods=['GET','POST'])
def preview(id):
    search_obj = Searcher.Searcher()
    result_data = search_obj.search_by_id(id)[0][0]
    #result_data = [1838, 'Bridges and Rails', 'Jindrich Novacek,Dusan Palencar,Michael Pitthan,Alla Velts', "    'Bridges and rails' is a documentary essay on public suicide. Suicide by jumping under a train or jumping from a bridge represents around 10% of the 1.600 suicides successfully committed every year in the Czech Republic. This film focuses on its impact through the experiences of people who have to deal with it.", ' Documentary, Documentary, Drama, History', 'f rated', 'Czech Republic', 'Czech', '2013 (Colombia)    ', 'https://www.imdb.com/title/tt1997298/', None]
    return render_template('imdb.html', result_data=result_data)


if __name__ == '__main__':
    app.run(debug=True)
