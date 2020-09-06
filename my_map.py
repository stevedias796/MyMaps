from flask import Flask, render_template, request, jsonify
import gmplot #for drawing maps and plotting 
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError

app = Flask(__name__)


@app.route('/index')
def home():
    return render_template("place_form.html")


@app.route('/search', methods=['POST', 'GET'])
def searching():
    #if request.method == 'POST':
    src_loc = request.args.get['src_loc']
    des_loc = request.args.get['des_loc']
    '''if (src_loc.len() == 0 or src_loc == "") and (des_loc.len() == 0 or des_loc == ""):
        return HttpResponse("<p>Please Enter Source and Destination</p>")'''
    src_loc = src_loc.replace(" ", "+")
    des_loc = des_loc.replace(" ", "+")
    #resp = "<html><body>"+src_loc+", "+des_loc+"</body></html>"

    src_lat_and_lon = []
    des_lat_and_lon = []
    lat = []
    lon = []
    resp1 = get_lat_long(src_loc, src_lat_and_lon) #function to get lat and long of the location
    resp = "<html><body>"+resp1+"</body></html>"
    return resp
    lat.append(src_lat_and_lon[0])
    lon.append(src_lat_and_lon[1])   

    #gmap = gmplot.GoogleMapPlotter(src_lat_and_lon[0], src_lat_and_lon[1], 15) #vikhroli

    get_lat_long(des_loc, des_lat_and_lon) 
    lat.append(des_lat_and_lon[0])
    lon.append(des_lat_and_lon[1]) 

    #gmap.scatter(lat, lon, '#faf600', size=40, marker=False)
    #gmap.plot(lat, lon, 'red', edge_with=9.5)
    result = {'source_lat' : src_lat_and_lon[0] , 'source_lon' : src_lat_and_lon[1], 'dest_lat' : des_lat_and_lon[0], 'des_lon' : des_lat_and_lon[1]}
    #gmap.draw("MyMaps\\templates\\display_map.html")
    return jsonify(result)
else:
    return jsonify({'data': "no records"}  


def get_lat_long(location, la_and_lo):
    search_url = "https://www.google.com/search?q="+location+"+logitude+latitude"
    #search_url = "https://www.google.co.in/maps/search/"+src_loc
    #print(search_url)
    req = Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    try:
        web_byte = urlopen(req).read()
    except HTTPError as e:
        return jsonify({'error': e.read()})
    #return web_byte
    webpage = web_byte.decode() #to convert into utf-8
    soup = BeautifulSoup(webpage,"lxml")

    tags = soup.find_all('div', {'class': 'BNeawe iBp4i AP7Wnd'})
    lat_long = tags[0].get_text()
    lat_long_new = lat_long.split(",")

    latitude = lat_long_new[0].split("°")
    longitude = lat_long_new[1].split("°")

    latitude = float(latitude[0])
    longitude = float(longitude[0])
    la_and_lo.append(latitude)
    la_and_lo.append(longitude)
    return


if __name__ == '__main__':
    app.run(debug=True)
'''
from flask import Flask     
app = Flask(__name__)   # Flask constructor 
  
# A decorator used to tells the application 
# which URL is associated function 
@app.route('/')       
def hello(): 
    return 'HELLO'
  
if __name__=='__main__': 
   app.run()     
   '''
