import lib.importer
import lib.benzenoids as bz
#import sys
#import traceback

def render_hexagon(input_str):
    try:
        hex_list = lib.importer.bec_to_hex_list(input_str)
        b = lib.benzenoids.Benzenoid(hex_list)
        return str(hex_list) + '; deficit: ' + str(b.convex_deficit())
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
            

def str2benzenoid(input_str):
    try:
        coord = str2coord(input_str)
        benz = bz.Benzenoid(coord)
        bec = benz.boundary_edges_code()
        cd = benz.convex_deficit()
        return str(bec) + '; deficit: ' + str(cd)
    except Exception as error:
        print(error)

        
##main to test program
    
def main():
    hex = "4343"
    outhex = render_hexagon(hex)
    print(outhex)
    #bec = [(0, 0), (-2, 1), (-1, 0), (-1, 1)]
    becstr = "[(0, 0), (-2, 1), (-1, 0), (-1, 1)]"
    outbenz = str2benzenoid(becstr)
    print(outbenz)
#    bec2tikz = benz.tikz_picture()
#    print(bec2tikz)

    
if  __name__ =='__main__':
    main()
