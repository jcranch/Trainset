import os2wgs84
import globalmaptiles
import Image, ImageDraw
import sqlite3
from flask import Flask, send_file, render_template
import StringIO
from flask.ext.cache import Cache
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

g = globalmaptiles.GlobalMercator()

def railtoWGS84(E,N):
    return os2wgs84.OSGB36toWGS84((E - 10000) * 100,  (N - 60000) * 100)

def railto900913meters(E, N):
    return g.LatLonToMeters(*railtoWGS84(E,N))

def railto900913pixels(E, N, zoom):
    mx, my = railto900913meters(E, N)
    return g.MetersToPixels(mx, my, zoom)

class TileLayer:
    def __init__(self):
        self.circles = []
    def addCircle(self, E, N, colour, size):
        """E, N are longitudes and latitudes in WGS84"""
        self.circles.append(Circle(E, N, colour, size))
    def renderTile(self, x, y, zoom):
        t = Image.new("RGBA", (256, 256), (0,0,0,0))
        draw = ImageDraw.Draw(t)
        ty = 256 * 2 ** zoom
        for c in self.circles:
            px, py = g.MetersToPixels(c.mx, c.my, zoom)
            py = ty - py - y * 256
            px = px - x * 256
            draw.ellipse((px - c.size * 2, py - c.size * 2, px + c.size * 2, py + c.size * 2), fill = "red")
            draw.ellipse((px - c.size, py - c.size, px + c.size, py + c.size), fill = c.colour)
        del draw #Make sure tile is drawn
        return t

class Circle:
    def __init__(self, E, N, colour, size):
        """E, N are longitudes and latitudes in WGS84"""
        self.mx, self.my = g.LatLonToMeters(E, N)
        self.colour = colour
        self.size = size

#http://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser
def serve_pil_image(pil_img):
    img_io = StringIO.StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg') 

@app.route('/tiles/<int:x>/<int:y>/<int:zoom>.png')
def tile_render(x, y, zoom):
    tl = makeTileLayer()
    return serve_pil_image(tl.renderTile(x, y, zoom))

@app.route('/')
def osm():
    return render_template('map.html')

@cache.cached(timeout=500, key_prefix='tilelayer')
def makeTileLayer():
    tl = TileLayer()
    E, N = railtoWGS84(14358, 63870) # Sheffield
    conn = sqlite3.connect('../data.sqlite')
    c = conn.cursor()
    for Erail, Nrail, ChangeTime in c.execute("select easting, northing, change_time from stations"):
        E, N = railtoWGS84(Erail, Nrail)
        tl.addCircle(E, N, "blue", ChangeTime)
    c.close()
    return tl

if __name__ == '__main__':
    app.run(debug=False)