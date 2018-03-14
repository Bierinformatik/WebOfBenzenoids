# mob.py --- 
# 
# Filename: mob.py
# Description: Serving the Math of Benzenoids
# Authors: Convexitators
# Maintainer: You
# Created: Mon Mar	5 16:05:41 2018 (+0100)
# Version: 0.1
# Package-Requires: (flask, py3.7)
# Last-Updated: Tue Mar 13 18:58:10 2018 (+0100)
#			By: Joerg Fallmann
#	  Update #: 27
# URL: https://www.bierinformatik.de/MoB
# Doc URL: 
# Keywords: 
# 
# 

# Commentary: 
# 
# 
# 
# 

# Change Log:
# 
# 
# 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.	 If not, see <http://www.gnu.org/licenses/>.
# 
# 

# Code:

from flask import * 
import os
import analyser

###Paths
UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

###App
app = Flask(__name__, static_url_path='/static')

###Configs
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True ### debug mode on

###Routes
@app.route("/mob",methods=['GET', 'POST'])
def hello():
	if request.method == 'POST':
		if 'text' in request.form:
			text = request.form['text']
			processed_text = text.upper()
			#TODO send text as input
			outp = analyser.render_hexagon(processed_text)
			image = getBCI(outp)
			return render_template('results.html', input=(text), output=outp, comment = image) #boundarycode is needed to find the image
		elif 'coord' in request.form:
			text = request.form['coord']
			processed_text = text.upper()
			outp = analyser.str2benzenoid(processed_text)
			image = getBCI(outp)
			return render_template('results.html', input=text, output=outp, comment = image)
		# check if the post request has the file part
		else:
			return redirect(request.url)
		if 'file' not in request.files:
			#			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file and allowed_file(file.filename) and file.filename != '':
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file',filename=filename))
	else:
		return render_template('welcomepage.html')
	
@app.route("/mob/draw",methods=['GET'])
def calc():
	return render_template('mob.html')

@app.route("/mob/results",methods=['GET', 'POST'])
def res():	
	if request.method == 'POST':
		jn = request.get_json()			
		coords = jn.get('coords').upper()
		return jsonify(dict(redirect='/mob/results?coords='+coords))
	else:
		if request.args.get('coords'):
			textc = request.args.get('coords')
			processed = textc.upper()  
			return render_template('results.html', input=textc, output=analyser.str2benzenoid(processed))
	
@app.route("/mob/help")
def help():
	return render_template('help.html')

@app.route("/mob/about")
def about():
	return render_template('about.html')

@app.route("/mob/contact")
def contact():
	return render_template('contact.html')

@app.route("/debug")
def deb():
	return render_template('index.html')

###Subs
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getBCI(istring):
        istring2 = istring.replace(" ","")
        infos = istring2.split(';')
        for i in infos:
                if(i.startswith("bc")):
                   elems = i.split(':')
                   imagename = "static/outfiles/" + elems[1]+".png" 
                   return imagename #this is the outfolder + boundary code + .png = image name
        return "NA" #error case

###Run as main
if __name__ == "__main__":
	
	app.run()

###Laters
#@app.route("/input")
#def read():
#	 return render_template('input.html')
#@app.route('/mob', methods=['POST'])
#def my_form_post():
#	 text = request.form['text']
#	 processed_text = text.upper()
#	 return processed_text

# 
# mob.py ends here
