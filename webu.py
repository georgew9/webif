#coding=utf-8
from flask import Flask,flash,request, render_template, redirect, url_for
import configparser
from flask_login import LoginManager,UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import simconf
from useradmin import User, Loginm
import os

app = Flask(__name__)

app.secret_key = 'abc'

Loginm.load_user()
#Loginm.save_user()
#Loginm.init(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader  # 定义获取登录用户的方法



def load_user(user_id):
    return User.get(user_id)

ipconfig= {'static ip_address':'192.168.1.120/24','static routers':'','static domain_name_servers':''}
wificonfig= {'ssid':'IOT','psk':'123456'}
#with open('dhcpcd.conf', 'r') as f:
#    config_string = '[dummy_section]\n' + f.read()
#conf = configparser.ConfigParser()
#conf.read_string(config_string)
confs = simconf.simconf()

options = confs.parse_config(ipconfig,'/etc/dhcpcd.conf')
wifioptions = confs.parse_config(wificonfig,'/etc/wpa_supplicant/wpa_supplicant.conf',1)

#options['static ip_address']='192.168.77.1/24'
#confs.save_config(options,'dhcpcd.conf')

#创建一个名为app的Flask对象
evtname= {'poll':'轮询 Poll','new':'发现 New','loss':'遗失 Loss'}
detname= {'person':'人','car':'车','bicycle':'自行车','motorcycle':'电动车','cat':'猫','dog':'狗','cell phone':'手机'}


@app.route('/login', methods=('GET', 'POST'))  # 登录
def login():
    #form = LoginForm()
    emsg = ""
    if request.method == 'POST':


        user_name = request.form['username']
        password = request.form['password']
        user_info = Loginm.get_user(user_name)  # 从用户数据中查找用户记录
        if user_info is None:
            emsg = "用户名或密码有误"
        else:
            user = User(user_info)  # 创建用户实体
            if user.verify_password(password):  # 校验密码
                login_user(user)  # 创建用户 Session
                flash('login ok')
                return redirect(request.args.get('next') or url_for('index'))
            else:
            	#flash("用户名或密码密码有误")
            	emsg = "用户名或密码有误"
    return render_template('login.html', emsg=emsg)


@app.route("/logout")
@login_required
def logout():
    logout_user()

    Loginm.save_user()
    return redirect("/")

@app.route("/chpass", methods=['GET', 'POST'])
@login_required
def chpass():
    
    emsg = ""

    if request.method == 'POST':
        # Form being submitted; grab data from form.

        user_name = request.form['username']
        password = request.form['password']
        newpassword = request.form['newpassword']
        cnewpassword = request.form['cnewpassword']        

        user_info = Loginm.get_user(user_name)  # 从用户数据中查找用户记录
        if user_info is None:
            emsg = "用户名或密码有误"
        else:
            user = User(user_info)
            if user.verify_password(password):  # 校验密码
 
                if newpassword==cnewpassword:

                    Loginm.chpass_user(user_name,newpassword)
                    Loginm.save_user()

                    emsg = "密码已修改"
                else:

                    emsg = "新密码不一致"


                #return redirect(request.args.get('next') or url_for('index'))
            else:
                #flash("用户名或密码密码有误")
                emsg = "用户名或密码密码有误"
       

    return render_template('chpass.html', emsg=emsg)


#@app.route("/")

#当有人访问网页服务器的根目录是，执行下面的代码
#def hello():
    #return "Hello World!"
	#return render_template('child.html')

@app.route("/")
@app.route("/setip", methods=['GET', 'POST'])
@login_required
def setip():

    error = ""
    showmodal = False

    if request.method == 'POST':
        # Form being submitted; grab data from form.

        options['static ip_address'] = request.form['ipadd']
        options['static routers'] = request.form['routers']
        options['static domain_name_servers'] = request.form['dns']
        
        confs.save_config(options,'/etc/dhcpcd.conf')

        showmodal = True
        #conf.write('dhcpcd.conf')


    return render_template('setip.html',conf=options,showmodal=showmodal)


@app.route("/setwifi", methods=['GET', 'POST'])
@login_required
def setwifi():

    error = ""
    showmodal = False
    if request.method == 'POST':
        # Form being submitted; grab data from form.

        wifioptions['ssid'] = request.form['ssid']
        wifioptions['psk'] = request.form['psk']
                
        confs.save_config(wifioptions,'/etc/wpa_supplicant/wpa_supplicant.conf',1)
        showmodal = True

    return render_template('setwifi.html',conf=wifioptions,showmodal=showmodal)


@app.route("/reboot", methods=['POST'])
@login_required
def reboot():
    #logout_user()
    print ('reboot called')
    os.system('sudo reboot')
    return redirect("/")




if __name__ == "__main__":
#判断是否这个脚本是从命令行直接运行
    app.run(host = "0.0.0.0", port = 80, debug = True)