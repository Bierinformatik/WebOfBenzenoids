import lib.importer
import lib.benzenoids
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


##main to test program
    
#def main():
#    hex = "4343"
#    outhex = render_hexagon(hex)
#    print(outhex)

    
#if  __name__ =='__main__':
#    main()
