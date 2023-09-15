from flask import Flask, render_template, request,redirect,url_for,flash
import mysql.connector
from flask import *

con=mysql.connector.connect(host='localhost',
                            user='root',
                            password='',
                            database='phonebook')

app=Flask(__name__)
app.secret_key = "my_secret_key"

@app.route('/',methods=["GET","POST"])
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('login.html')

@app.route('/suc',methods=["POST","GET"])
def my_admin():
    if request.method=="POST":
        a_name=request.form["ad_name"]
        a_psw=request.form["ad_psw"]
        if a_name=="Admin" and a_psw=="123":
            return render_template("index.html")
        else:
            flash("Enter valid details")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/index',methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('save.html')

@app.route('/cnt_list',methods=["GET","POST"])
def cnt_list():
    if request.method=="POST":
      name=request.form["uname"]
      n_name=request.form["nickname"]
      ph1=request.form["phn1"]
      ph2=request.form["phn2"]
      el=request.form["eml"]
      ad=request.form["addr"]
      r=request.form["rel"]
      cur=con.cursor()
      cur.execute("select * from my_contacts")
      l_cnt=cur.fetchall()
      cur.execute("select count(*) from my_contacts")
      tot_rec=cur.fetchall()
      if len(tot_rec)>5:
          flash("You can't add more than 5 contacts")
          return render_template("save.html")
      else:
          if ((name in l_cnt) or (ph1 in l_cnt) or (ph2 in l_cnt) or (el in l_cnt)):
            flash("Contact details entered are already existed")
            return render_template("save.html")
          else:
            cur.execute("insert into my_contacts (uname,nick_name,phn1,phn2,eml,addr,rel) values(%s,%s,%s,%s,%s,%s,%s)",(name,n_name,ph1,ph2,el,ad,r))
            con.commit()
            return redirect('/get')
    else:
        return render_template('save.html')
    
@app.route('/view')
def view():
    return render_template("view_nm.html")

@app.route('/view_cnt',methods=["GET","POST"])
def view_cnt():
    v_name=request.form["cname"]
    cur=con.cursor()
    cur.execute("select * from my_contacts where uname=%s",(v_name,))
    cnt_det=cur.fetchone()
    if cnt_det:
        return render_template("view_cnt.html",req_cnt=cnt_det)
    else:
        flash("Contact name does not existed")
        return render_template("view_nm.html")
    
@app.route('/get')
def get():
    cur=con.cursor()
    cur.execute("SELECT * from my_contacts order by uname")
    data=cur.fetchall()
    if data:
        return render_template('print_cnt.html',my_cnt=data)
    else:
        flash("No contacts are available")
        return render_template('print_cnt.html')

@app.route('/update/<string:r_id>',methods=["GET","POST"])
def re_update(r_id):
    cur=con.cursor()
    cur.execute("select * from my_contacts where id=%s",(r_id,))
    data=cur.fetchone()
    return render_template("edit_cnt.html",ref=data)

@app.route('/delete/<string:r_id>',methods=["GET","POST"])
def re_delete(r_id):
    cur=con.cursor()
    cur.execute('delete from my_contacts where id= %s', (r_id,))
    con.commit()
    return render_template('index.html')

@app.route('/edit')
def edit():
    return render_template("edit_nm.html")

@app.route('/edit_sub',methods=["GET","POST"])
def edit_sub():
    if request.method=="POST":
        e_name=request.form["mname"]
        cur=con.cursor()
        cur.execute("select * from my_contacts where uname=%s",(e_name,))
        req_rec=cur.fetchone()
        if req_rec:
            return render_template("edit_cnt.html",ref=req_rec)
        else:
            flash("Contact doesn't existed")
            return render_template("edit_nm.html")
    else:
        return render_template("edit_nm.html")
    
@app.route('/edit_list',methods=["GET","POST"])
def edit_list():
    if request.method=="POST":
        n_id=request.form["uid"]
        n_uname=request.form["uname"]
        n_nkname=request.form["nickname"]
        n_phn1=request.form["phn1"]
        n_phn2=request.form["phn2"]
        n_eml=request.form["eml"]
        n_addr=request.form["addr"]
        n_rel=request.form["rel"]
        cur=con.cursor()
        cur.execute("update my_contacts set uname=%s,nick_name=%s,phn1=%s, phn2=%s, eml=%s, addr=%s, rel=%s where id=%s",(n_uname,n_nkname,n_phn1,n_phn2,n_eml,n_addr,n_rel,n_id))
        con.commit()
        return redirect('/get')
    else:
        return render_template("edit_cnt.html")
        
@app.route('/delete')
def delete():
    return render_template('delete_nm.html')

@app.route('/del_sub',methods=["GET","POST"])
def del_sub():
    if request.method=="POST":
        d_name=request.form["del_name"]
        cur=con.cursor()
        cur.execute("select uname from my_contacts where uname=%s",(d_name,))
        d_nm=cur.fetchone()
        if d_nm:
            cur.execute("delete from my_contacts where uname=%s",(d_name,))
            con.commit()
            return redirect('/get')
        else:
            flash("Contact name doesn't existed")
            return render_template("delete_nm.html")
    else:
        return render_template("delete_nm.html")
    
@app.route('/meet_team')
def meet():
    return render_template("meet.html")

@app.route('/about')
def about():
    return render_template("about.html")
                           
@app.route('/feed')
def feed():
    return render_template("feedback.html")
                          
@app.route('/res',methods=["GET","POST"])
def result():
    if request.method=="POST":
        f_name=request.form["u_name"]
        f_email=request.form["u_email"]
        f_feedback=request.form["u_feedback"]
        f_queries=request.form["u_queries"]
        cur=con.cursor()
        if f_queries:
            cur.execute("insert into feedback (u_name,u_email,u_feedback,u_queries) values(%s,%s,%s,%s)",(f_name,f_email,f_feedback,f_queries))
            con.commit()
            flash("Thank You for your feedback"+"We will reach you soon..")
            return render_template("res.html")
        else:
            cur.execute("insert into feedback (u_name,u_email,u_feedback,u_queries) values(%s,%s,%s,%s)",(f_name,f_email,f_feedback,f_queries))
            con.commit()
            return render_template("res.html")
    else:
        return render_template("feedback.html")
  
if __name__=='__main__':
    app.run(debug=True)