import lib.importer
import lib.benzenoids

def render_hexagon(input_str):
    hex_list = lib.importer.bec_to_hex_list(input_str)
    b = lib.benzenoids.Benzenoid(hex_list)
    return str(hex_list) + '; deficit: ' + str(b.convex_deficit())
