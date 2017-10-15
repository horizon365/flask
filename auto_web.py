# -*- coding: utf-8 -*-
"""

created on '2017/10/12'
@author: 'lWX465581'
"""
import os
import time
import subprocess
from flask import Flask, request, make_response, render_template, redirect, current_app
from flask.ext.wtf import Form
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, IPAddress, Regexp

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'hard to guess string'
moment = Moment(app)
bootstrap = Bootstrap(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


class TodoForm(Form):
    style = RadioField(u'Lable', choices=[('realtime', u"实时构建（较耗时）"), ('notrealtime', u'缓存构建（分支、版本号不可修改）')],
                       default='notrealtime', validators=[DataRequired()])
    choice = StringField('''fiber_fault:    -> a
                            data_cvt:       -> b
                            data_mgt:       -> c
                            ui_int:         -> d
                            hadoop:         -> e
                            aabd            -> k
                            spark           -> l
                            model_mgt       -> m
                            omc_alarm       -> n
                            capacity_prediction_mgt -> o''', validators=[DataRequired(), Regexp("\w*")])
    hosts = StringField(u'目标ip：', validators=[IPAddress(ipv4=True, message=u"格式错误"), DataRequired()])
    version = StringField(u'版本号：（0.0.x格式）', validators=[DataRequired()],
                          default='0.0.%s' % time.strftime("%Y%m%d", time.localtime()))
    branch = StringField(u'Git分支：', validators=[DataRequired()], default='dev')
    submit = SubmitField('Submit')


def check_output(target):
    process1 = subprocess.Popen(target, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = process1.stdout.readline()
        if not line:
            break
        print line.rstrip()

@app.route('/', methods=['POST', "GET"])
def login():
    form = TodoForm()

    if form.validate_on_submit():
        choice = request.form.get('choice')
        version = request.form.get('version')
        hosts = request.form.get('hosts')
        branch = request.form.get('branch')
        style = request.form.get('style')

        if style == 'realtime':
            target = "fab -f /home/liuyiqun/Fab_auto_deploy/fabfile_auto.py reload_docker --set=version='%s',choice='%s',branch='%s' --hosts='%s'" % (
                version, choice, branch, hosts)
        else:
            target = "fab -f /home/liuyiqun/Fab_auto_deploy/fabfile_auto_reload.py reload_docker --set=choice='%s' --hosts='%s'" % (choice, hosts)
        try:
            target = 'ping 127.0.0.1 -c 80 >> /tmp/tmp.txt &'
            os.system(target)
            #output = subprocess.check_output(target)
            return redirect('/result/tmp')
        except Exception:
            return render_template('result.html', result="失败")
    else:
        make_response("not support")
    return render_template('show_entries.html', form=form)

@app.route('/result/<id>')
def result(id):
    process1 = subprocess.Popen('tail -10000 /tmp/%s.txt' % id, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process1.stdout.readlines()
    return render_template('result.html', result=output)

if __name__   == '__main__':
    app.run(host="0.0.0.0", threaded=True, debug=True)
