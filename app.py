import os
from flask import *  
from just import filter
app = Flask(__name__) 
UPLOAD_DIRECTORY = "/Users/VAISHNAVI/Desktop/mini/uploadedfiles"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@app.route('/')  
def upload():  
    return render_template("filter.html")  
 
@app.route('/uploadfiles', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(os.path.join(UPLOAD_DIRECTORY, f.filename)) 
        c=filter()            
        c.convert(UPLOAD_DIRECTORY+"/",f.filename)
        #path+filename+"filtered"+".mp4"
        
        r=f.filename[:len(f.filename)-4]
        return send_from_directory(UPLOAD_DIRECTORY,r+"filtered"+".mp4", as_attachment=True)


        
@app.route("/about1.html")
def send1():
    return render_template("about1.html")

@app.route("/filter.html")
def send2():
    return render_template("filter.html")

@app.route("/contact1.html")
def send3():
    return render_template("contact1.html")

@app.route("/contact")
def send4():
    return render_template("thanks.html")



if __name__ == '__main__':  
    app.run()  