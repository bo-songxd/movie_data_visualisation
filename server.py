from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_paginate import Pagination,get_page_parameter
from pyecharts import Line

from jinja2 import Markup
app = Flask(__name__)
#sqlalchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie.db'
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#创建对象
class RESULT(db.Model):
    ID = db.Column(db.Integer, primary_key = True)
    NAME = db.Column(db.String(100))
    AREA=db.Column(db.String(100))
    TOTALBOX = db.Column(db.FLOAT)
    SCHEDULEPERCENTAGE =db.Column(db.Float(10))
    PERSONTIME = db.Column(db.Float(10))
    TIME = db.Column(db.Integer)

    def __init__(self, ID,NAME,AREA,TOTALBOX,SCHEDULEPERCENTAGE,PERSONTIME,TIME):
        self.ID = ID
        self.NAME = NAME
        self.AREA = AREA
        self.TOTALBOX = TOTALBOX
        self.SCHEDULEPERCENTAGE = SCHEDULEPERCENTAGE
        self.PERSONTIME = PERSONTIME
        self.TIME = TIME


db.create_all()



#初始网页
@app.route('/')
def index():
    return render_template('index.html',result = [])
#搜索结果呈现网页

@app.route('/submit',methods = ['POST','GET'])
def submit():
    selected = []
    name, time, area, startdate, enddate='','','','2018-01-01','2018-12-31'
    list = [name, time, area, startdate, enddate]
    #尝试取得value
    try:
        name = request.form['moviename']
    except:
        pass
    try:
        time = request.form['time']
        selected.append(time)
    except:pass
    try:
        area = request.form['area']
        selected.append(area)
    except:pass
    print(name,time,area,startdate,enddate)

    conn = sqlite3.connect('movie.db')
    name = str(name)
    #根据条件创建sql
    if name != '':
        sql = '''
            SELECT DISTINCT ID,NAME,MAX(TOTALBOX),MAX(SCHEDULEPERCENTAGE),SUM(PERSONTIME)
            FROM MOVIESALE WHERE NAME LIKE '%{}%'  GROUP BY ID;
            '''
        c = conn.cursor()
        c.execute(sql.format(name))
        namelist = []
        idlist = []
        totalbox = []
        schedulepercentage = []
        persontime = []
        for row in c:
            idlist.append(row[0])
            namelist.append(row[1])
            totalbox.append(row[2])
            schedulepercentage.append(row[3])
            persontime.append(row[4])

        sql = '''
                    SELECT DISTINCT ID,AREA,TIME
                    FROM MOVIEINFO WHERE
                '''
        sql += '('
        for i in range(len(idlist)):
            sql+=" ID = '{}' OR "

        sql = sql[0:-3]
        sql += ')AND('
        if time != '':

            if time == 'less':
                sql += " TIME < 90  AND"
            else:
                sql += " TIME >= 90  AND"
        if area != '':
            idlist.append(area)
            sql += " AREA LIKE '%{}%'  AND"

        sql = sql[0:-4]
        sql +=')'

        c.execute(sql.format(*idlist))

        for row in c:
            index = indexsearch(row[0],idlist)
            result = RESULT(row[0],namelist[index],row[1],totalbox[index],schedulepercentage[index],persontime[index],row[2])

            db.session.add(result)
        conn.close()
    else:
        sql = '''
            SELECT ID,AREA,TIME
            FROM MOVIEINFO WHERE
        '''
        if time != '':
            if time == 'less':
                sql += " TIME < 90  AND"
            else:
                sql += " TIME >= 90  AND"
        if area != '':
            sql += " AREA LIKE '%{}%'  AND"

        sql = sql[0:-4]

        c = conn.cursor()
        c.execute(sql.format(area))
        idlist = []
        arealist = []
        timelist = []
        for row in c:

            idlist.append(row[0])
            arealist.append(row[1])
            timelist.append(row[2])
        for item in idlist:
            sql = '''
                    SELECT ID,NAME,MAX(TOTALBOX),MAX(SCHEDULEPERCENTAGE),SUM(PERSONTIME)
                    FROM MOVIESALE WHERE ID = '{}'  GROUP BY ID;
                    '''
            sql = sql.format(item)
            c.execute(sql)
            for row in c:
                index = indexsearch(row[0],idlist)
                result = RESULT(row[0],row[1],arealist[index],row[2],row[3],row[4],timelist[index])

                db.session.add(result)
        conn.close()


    #最后分页
    limit = 10
    data = RESULT.query.all()
    page = request.args.get(get_page_parameter(),type = int,default=1)
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    pagination = Pagination(page=page, total=RESULT.query.count())
    ret = RESULT.query.slice(start, end)

    return render_template('web.html',result = ret,pagination=pagination,area = area)





def indexsearch(id,list):
    for i in range(len(list)):
        if list[i] == id:
            return i


#画图
@app.route('/draw/<id>')
def draw1(id):
    s3d = draw(id)
    return render_template('draw.html',
                           myechart=s3d.render_embed(),
                           host='http://chfw.github.io/jupyter-echarts/echarts',
                           script_list=s3d.get_js_dependencies())

def draw(id):
    conn = sqlite3.connect('movie.db')
    c= conn.cursor()
    sql = '''
            SELECT DATE,REALTIMEBOX
            FROM MOVIESALE
            WHERE ID = {}
    '''

    sql = sql.format(id)
    print(sql)
    c.execute(sql)
    datelist = []
    boxlist = []
    for row in c:
        print(row)
        datelist.append(row[0])
        box = row[1]
        #将str数据转为int
        if type(box) == int or type(box) == float:
            pass
        elif box.isdigit():
            box = float(box)
        elif box[-1] == '万':
            box = float(box[0:-1]) * 10000.0
        elif box[-1] == '亿':
            box = float(box[0:-1]) * 100000000.0
        boxlist.append(box)


    line = Line('票房数据', width=1200, height=600)
    attr = datelist
    line.add(name = '票房',x_axis=datelist,y_axis = boxlist)
    return line

if __name__ == '__main__':
    app.run()
