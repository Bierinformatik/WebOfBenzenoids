# mob.py --- 
# 
# Filename: mob.py
# Description: Serving the Math of Benzenoids
# Authors: Convexitators
# Maintainer: You
# Created: Mon Mar  5 16:05:41 2018 (+0100)
# Version: 0.1
# Package-Requires: (flask, py3.7)
# Last-Updated: Mon Mar  5 18:21:37 2018 (+0100)
#           By: Joerg Fallmann
#     Update #: 18
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.
# 
# 

# Code:

from flask import * 
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def hello():
	return 'Hello'
@app.route("/mob")
def calc():
    return render_template('mob.html')

@app.route("/debug")
def deb():
    return render_template('index.html')

#@app.route("/input")
#def read():
#    return render_template('input.html')

# 
# mob.py ends here
