import lib.importer
import lib.benzenoids as bz
from subprocess import call

#boundary code to coordinates and convexity deficit
def render_hexagon(input_str):
    try:
        hex_list = lib.importer.bec_to_hex_list(input_str)
        b = bz.Benzenoid(hex_list)
        realbc = b.boundary_edges_code()
        hex2pdf(b)
        return 'bc:' + str(realbc) + '; coordinates:' + str(hex_list) + '; deficit: ' + str(b.convex_deficit())
    except:
        e= "Error: not a valid boundary code!"
#        e = traceback.print_exc()
#        e = sys.exc_info()[0]
        return e


#parse string to coordinates list (probably not a very safe method)
def str2coord(input_str):
    #input_str has to be converted to a list of coordinates
    coordlist = []
    if(input_str[0] == '['):
        newstr1 = input_str.replace("[","")
    else:
        newstr1 = input_str
    if(newstr1[-1] == ']'):
        newstr11 = newstr1.replace("]","")
    else:
        newstr11= newstr1
    newstr = newstr11.replace(" ","")
    ls = len(newstr)
    if(ls == 0):
        raise Exception("Error! Empty coordinates list!")
    
    spstr = newstr.split(',') #now every first entry is (num and every second is num)
    cura = 0
    curb = 0
    for s in spstr:
        if(s[0] =='('):
            cura = int(s[1:])
        elif(s[-1] == ')'):
            curb = int(s[:-1])
            p = (cura,curb)
            coordlist.append(p)
        else:
            raise Exception("Error! Weird format!")
    return coordlist
            

#coordinate string to boundary code and convexity deficit
def str2benzenoid(input_str):
    try:
        coord = str2coord(input_str)
        benz = bz.Benzenoid(coord)
        bec = benz.boundary_edges_code()
        cd = benz.convex_deficit()
        hex2pdf(benz)
        return 'bc:' + str(bec) + '; deficit: ' + str(cd)
    except Exception as error:
        print(error)


#benzenoid object to tex to pdf
def hex2pdf(benz):
    bec = benz.boundary_edges_code()
    outfile = "static/outfiles/"+str(bec)+".tex"
    pdffile = "static/outfiles/"+str(bec)+".pdf"
    pngfile = "static/outfiles/"+str(bec)+".png"
    template = "./templates/picture.tex"
    bec2tikz = benz.tikz_picture_simple()
    text = "";
    file = open(template,"r")
    f = open(outfile,"w")
    for line in file:
        if(line.startswith("<!PICTURE_HERE")):
            f.write(bec2tikz)
        else:
            f.write(line)
    file.close()
    f.close()
    call(["pdflatex", "-output-directory=static/outfiles/", outfile])
    call(["convert", pdffile, pngfile])


##main to test program
    
def main():
    #boundary code to coordinates and convexity deficit
    hex = "55"
    outhex = render_hexagon(hex)
    print(outhex)
    #coordinate string to boundary code and convexity deficit
    becstr = "[(0, 0), (-2, 1), (-1, 0), (-1, 1)]"
    outbenz = str2benzenoid(becstr)
    print(outbenz)
    #benzenoid object to tex to pdf
#    coord = [(0, 0), (-2, 1), (-1, 0), (-1, 1)]
#    benz = bz.Benzenoid(coord)
#    hex2pdf(benz)

    
if  __name__ =='__main__':
    main()
