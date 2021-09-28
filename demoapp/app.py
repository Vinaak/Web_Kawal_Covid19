from flask import Flask, render_template
import requests, schedule

app= Flask(__name__)

def indo():
    api_url="https://api.kawalcorona.com/indonesia/"
    rstl= requests.get(api_url).json()
    return rstl

def provinsi():
    api_url="https://api.kawalcorona.com/indonesia/provinsi/"
    result = list(map(lambda x:x["attributes"], requests.get(api_url).json()))
    return result

def cariProvinsi(dicari):
    result = list(filter(lambda x: x["Provinsi"] == dicari, provinsi()))
    return result

def provinsiAscending():
    result = sorted(provinsi(), key = lambda x:x["Provinsi"], reverse = False)
    return result

def provinsiDescending():
    result = sorted(provinsi(), key = lambda x:x["Provinsi"], reverse = True)
    return result


r_indo= schedule.every(2).seconds.do(indo)

data_indo=indo()
data_jateng=cariProvinsi("Jawa Tengah")
data_provinsi=list(enumerate(provinsi(), start=1))
data_provinsi_asc = list(enumerate(provinsiAscending(), start=1))
data_provinsi_dsc = list(enumerate(provinsiDescending(), start=1))

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html",data_indo=data_indo,data_jateng=data_jateng)

@app.route("/data.html")
def data():
    return render_template("data.html",data_provinsi=data_provinsi)

@app.route("/data/ascending")
def dataAsc():
    return render_template("data.html",data_provinsi = data_provinsi_asc)

@app.route("/data/descending")
def dataDsc():
    return render_template("data.html",data_provinsi = data_provinsi_dsc)

@app.route("/About.html")
def about():
    return render_template("About.html")



if __name__=="__main__":
    app.run(debug=True)

