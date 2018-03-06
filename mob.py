# mob.py --- 
# 
# Filename: mob.py
# Description: Serving the Math of Benzenoids
# Authors: Convexitators
# Maintainer: You
# Created: Mon Mar	5 16:05:41 2018 (+0100)
# Version: 0.1
# Package-Requires: (flask, py3.7)
# Last-Updated: Tue Mar  6 10:41:10 2018 (+0100)
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

###Paths
UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

###App
app = Flask(__name__, static_url_path='/static')

###Configs
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###Routes
@app.route("/mob",methods=['GET', 'POST'])
def hello():
	if request.method == 'POST':
		text = request.form['text']
		processed_text = text.upper()
		return processed_text	
	else:
		return render_template('welcomepage.html')
	
@app.route('/mob/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file',
									filename=filename))
	return ''
		
@app.route("/mob/draw")
def calc():
	return render_template('mob.html')

@app.route("/debug")
def deb():
	return render_template('index.html')

###Subs
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
