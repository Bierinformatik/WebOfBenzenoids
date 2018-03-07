__author__ = 'Nino Bašić <nino.basic@fmf.uni-lj.si>'
__version__ = '0.1'


import functools
import fractions

import networkx  # Library for graphs and networks (version >= 1.8.1)
import numpy  # Library for numeric computation (version >= 1.8.1)
import sympy  # Library for symbolic computation (version >= 0.7.5)

import algorithms


def centre_of_mass(coords):
    sx, sy = 0, 0
    for x, y in coords:
        sx += x
        sy += y
    return sx / len(coords), sy / len(coords)


class Face(object):

    def __init__(self, face_label, benzenoid):
        """
        Construct a face inside the given benzenoid.
        """
        self.label = face_label
        self.benzenoid = benzenoid
        self.benzenoid.face_dict[self.label] = self

        # Add vertices (and create any missing).
        self.__vertex_list = []
        for nu in range(6):
            vertex_label = Vertex.canonical_label(face_label + (nu,))
            if vertex_label not in self.benzenoid.vertex_dict:
                vertex = Vertex(vertex_label, benzenoid)
            else:
                vertex = self.benzenoid.vertex_dict[vertex_label]
            self.__vertex_list.append(vertex)

        # Add edges (and create any missing).
        self.__edge_list = []
        for nu in range(6):
            edge_label = Edge.canonical_label(face_label + (nu,))
            if edge_label not in self.benzenoid.edge_dict:
                edge = Edge(edge_label, benzenoid)
            else:
                edge = self.benzenoid.edge_dict[edge_label]
            self.__edge_list.append(edge)

        # Update information on neighbours.
        self.__face_list = []
        self.update_face_list()

        # Force incident edges to refresh their adjacency/incidence lists.
        for edge in self.__edge_list:
            edge.update_every_list()

        # Force incident vertices to refresh their adjacency/incidence lists.
        for vertex in self.__vertex_list:
            vertex.update_every_list()

        # Force adjacent faces to refresh their adjacent faces lists.
        for face in self.__face_list:
            face.update_face_list()

        edge_layer = set()
        vertex_layer = set()
        for vertex in self.__vertex_list:
            edge_layer |= set(vertex.incident_edges())
            vertex_layer |= set(vertex.adjacent_vertices())
        edge_layer -= set(self.__edge_list)
        vertex_layer -= set(self.__vertex_list)
        for edge in edge_layer:
            edge.update_edge_list()
        for vertex in vertex_layer:
            vertex.update_vertex_list()

    def update_face_list(self):
        """
        Rebuild the list of adjacent faces.
        """
        xi, eta = self.label
        neigh = [(xi + d_xi, eta + d_eta) for d_xi, d_eta in [(-1, 1), (0, 1), (-1, 0), (1, 0), (0, -1), (1, -1)]]
        self.__face_list = [self.benzenoid.face_dict[label] for label in neigh
                            if label in self.benzenoid.face_dict]

    def update_edge_list(self):
        """
        Rebuild the list of incident edges.

        Note: This function is never needed, but might become handy in the future
        (when the removal of hexagons will be implemented).
        """
        incident = [Edge.canonical_label(self.label + (nu,)) for nu in range(6)]
        self.__face_list = [self.benzenoid.face_dict[label] for label in incident
                            if label in self.benzenoid.face_dict]

    def update_vertex_list(self):
        """
        Rebuild the list of incident vertices.

        Note: This function is never needed, but might become handy in the future
        (when the removal of hexagons will be implemented).
        """
        incident = [Vertex.canonical_label(self.label + (nu,)) for nu in range(6)]
        self.__vertex_list = [self.benzenoid.vertex_dict[label] for label in incident
                              if label in self.benzenoid.vertex_dict]

    def update_every_list(self):
        """
        Rebuild all incidence/adjacency lists.
        """
        self.update_vertex_list()
        self.update_edge_list()
        self.update_face_list()

    def incident_vertices(self):
        """
        Make a generator object that will yield incident vertices.
        """
        for v in self.__vertex_list:
            yield v

    def incident_edges(self):
        """
        Make a generator object that will yield incident edges.
        """
        for e in self.__edge_list:
            yield e

    def adjacent_faces(self):
        """
        Make a generator object that will yield adjacent faces.
        """
        for f in self.__face_list:
            yield f

    def get_incident_edge(self, nu):
        """
        Return the adjacent edge at position nu (0 <= nu <= 5).
        """
        return self.benzenoid.edge_dict[Edge.canonical_label(self.label + (nu,))]


class Edge(object):

    @staticmethod
    def canonical_label(label):
        """
        Convert an edge label to its corresponding canonical label.
        """
        xi, eta, nu = label
        if 0 <= nu <= 2:
            return xi, eta, nu
        if nu == 3:
            return xi + 1, eta - 1, 0
        if nu == 4:
            return xi, eta - 1, 1
        if nu == 5:
            return xi - 1, eta, 2
        raise ValueError('nu is out of range')

    def __init__(self, edge_label, benzenoid):
        """
        Construct an edge inside the given benzenoid.

        Note: Updating of adjacency/incidence lists is performed by the Face constructor.
        """
        self.label = Edge.canonical_label(edge_label)
        self.benzenoid = benzenoid
        self.benzenoid.edge_dict[self.label] = self

        self.__vertex_list = []
        self.__edge_list = []
        self.__face_list = []

    def update_vertex_list(self):
        """
        Rebuild the list of incident vertices.
        """
        xi, eta, nu = self.label
        if nu == 0:
            incident = [(xi - 1, eta, 1), (xi, eta, 0)]
        elif nu == 1:
            incident = [(xi, eta, 0), (xi, eta, 1)]
        else:  # nu == 2
            incident = [(xi, eta, 1), (xi + 1, eta - 1, 0)]
        self.__vertex_list = [self.benzenoid.vertex_dict[label] for label in incident
                              if label in self.benzenoid.vertex_dict]

    def update_edge_list(self):
        """
        Rebuild the list of adjacent edges.
        """
        xi, eta, nu = self.label
        if nu == 0:
            neigh = [(xi - 1, eta + 1, 2), (xi - 1, eta, 1), (xi, eta, 1), (xi - 1, eta, 2)]
        elif nu == 1:
            neigh = [(xi - 1, eta + 1, 2), (xi, eta, 0), (xi + 1, eta, 0), (xi, eta, 2)]
        else:  # nu == 2
            neigh = [(xi, eta, 1), (xi + 1, eta, 0), (xi + 1, eta - 1, 0), (xi + 1, eta - 1, 1)]
        self.__edge_list = [self.benzenoid.edge_dict[label] for label in neigh
                            if label in self.benzenoid.edge_dict]

    def update_face_list(self):
        """
        Rebuild the list of incident faces.
        """
        xi, eta, nu = self.label
        if nu == 0:
            incident = [(xi - 1, eta + 1), (xi, eta)]
        elif nu == 1:
            incident = [(xi, eta + 1), (xi, eta)]
        else:  # nu == 2
            incident = [(xi, eta), (xi + 1, eta)]
        self.__face_list = [self.benzenoid.face_dict[label] for label in incident
                            if label in self.benzenoid.face_dict]

    def incident_faces_candidates(self):
        """
        Return the list of coordinates of incident faces candidates.
        """
        xi, eta, nu = self.label
        if nu == 0:
            return [(xi - 1, eta + 1), (xi, eta)]
        elif nu == 1:
            return [(xi, eta + 1), (xi, eta)]
        else:  # nu == 2
            return [(xi, eta), (xi + 1, eta)]

    def update_every_list(self):
        """
        Rebuild all incidence/adjacency lists.
        """
        self.update_vertex_list()
        self.update_edge_list()
        self.update_face_list()

    def incident_vertices(self):
        """
        Make a generator object that will yield incident vertices.
        """
        for v in self.__vertex_list:
            yield v

    def adjacent_edges(self):
        """
        Make a generator object that will yield adjacent edges.
        """
        for e in self.__edge_list:
            yield e

    def incident_faces(self):
        """
        Make a generator object that will yield incident faces.
        """
        for f in self.__face_list:
            yield f

    def is_boundary(self):
        """
        Return True if and only if this edge belongs to the boundary.

        Note: The boundary is the union of perimeter and holes.
        """
        return len(self.__face_list) == 1

    def belongs_to_perimeter(self):
        """
        Return True if and only if this edges belongs to the perimeter.
        """
        if 'perimeter_set' not in self.benzenoid.memo:
            self.benzenoid.perimeter()
        return self.label in self.benzenoid.memo['perimeter_set']

    def belongs_to_hole(self):
        """
        Return True if and only if this edges belongs to one of the holes.
        """
        return self.is_boundary() and not self.belongs_to_perimeter()


class Vertex(object):

    @staticmethod
    def canonical_label(label):
        """
        Convert a vertex label to its corresponding canonical label.
        """
        xi, eta, nu = label
        if 0 <= nu <= 1:
            return xi, eta, nu
        if nu == 2:
            return xi + 1, eta - 1, 0
        if 3 <= nu <= 4:
            return xi, eta - 1, 4 - nu
        if nu == 5:
            return xi - 1, eta, 1
        raise ValueError('nu is out of range')

    def __init__(self, vertex_label, benzenoid):
        """
        Construct a vertex inside the given benzenoid.

        Note: Updating of adjacency/incidence lists is performed by the Face constructor.
        """
        self.label = Vertex.canonical_label(vertex_label)
        self.benzenoid = benzenoid
        self.benzenoid.vertex_dict[self.label] = self

        self.__vertex_list = []
        self.__edge_list = []
        self.__face_list = []

    def update_vertex_list(self):
        """
        Rebuild the list of adjacent vertices.

        BUG!
        """
        xi, eta, nu = self.label
        if nu == 0:
            neigh = [(xi - 1, eta + 1, 1), (xi - 1, eta, 1), (xi, eta, 1)]
            incident_edges = [(xi - 1, eta + 1, 2), (xi, eta, 0), (xi, eta, 1)]
        else:  # nu == 1
            neigh = [(xi, eta, 0), (xi + 1, eta, 0), (xi + 1, eta - 1, 0)]
            incident_edges = [(xi, eta, 1), (xi + 1, eta, 0), (xi, eta, 2)]
        self.__vertex_list = [self.benzenoid.vertex_dict[label] for label, e_label in zip(neigh, incident_edges)
                              if label in self.benzenoid.vertex_dict and e_label in self.benzenoid.edge_dict]

    def update_edge_list(self):
        """
        Rebuild the list of incident edges.
        """
        xi, eta, nu = self.label
        if nu == 0:
            incident = [(xi - 1, eta + 1, 2), (xi, eta, 0), (xi, eta, 1)]
        else:  # nu == 1
            incident = [(xi, eta, 1), (xi + 1, eta, 0), (xi, eta, 2)]
        self.__edge_list = [self.benzenoid.edge_dict[label] for label in incident
                            if label in self.benzenoid.edge_dict]

    def update_face_list(self):
        """
        Rebuild the list of incident faces.
        """
        xi, eta, nu = self.label
        if nu == 0:
            incident = [(xi - 1, eta + 1), (xi, eta + 1), (xi, eta)]
        else:  # nu == 1
            incident = [(xi, eta + 1), (xi, eta), (xi + 1, eta)]
        self.__face_list = [self.benzenoid.face_dict[label] for label in incident
                            if label in self.benzenoid.face_dict]

    def update_every_list(self):
        """
        Rebuild all incidence/adjacency lists.
        """
        self.update_vertex_list()
        self.update_edge_list()
        self.update_face_list()

    def adjacent_vertices(self):
        """
        Make a generator object that will yield adjacent vertices.
        """
        for v in self.__vertex_list:
            yield v

    def incident_edges(self):
        """
        Make a generator object that will yield incident edges.
        """
        for e in self.__edge_list:
            yield e

    def incident_faces(self):
        """
        Make a generator object that will yield incident faces.
        """
        for f in self.__face_list:
            yield f

    def get_coordinates(self, edge_length=1.4):
        """
        Return the cartesian coordinates (in the infinite hexagonal grid) of the vertex.
        """
        xi, eta, nu = self.label
        altitude = 3**0.5 * edge_length / 2
        x = eta * altitude + 2 * xi * altitude
        y = 3 / 2 * eta * edge_length
        if nu == 0:
            y += edge_length
        else:  # nu == 1
            x += altitude
            y += edge_length / 2
        return x, y

    def is_male(self):
        """
        Return True if and only if this is a male vertex (as defined by Gordon and Davison).
        """
        xi, eta, nu = self.label
        return nu == 0

    def is_female(self):
        """
        Return True if and only if this is a female vertex (as defined by Gordon and Davison).
        """
        xi, eta, nu = self.label
        return nu == 1

    def is_peak(self):
        """
        Return True if and only if this vertex is a peak.
        """
        _, y = self.get_coordinates()
        return (self.is_male() and len(self.__face_list) == 1 and
                all(y > v.get_coordinates()[1] for v in self.__vertex_list))

    def is_valley(self):
        """
        Return True if and only if this vertex is a valley.
        """
        _, y = self.get_coordinates()
        return (self.is_female() and len(self.__face_list) == 1 and
                all(y < v.get_coordinates()[1] for v in self.__vertex_list))

    def get_degree(self):
        return len(self.__vertex_list)

    def __str__(self):
        return str(self.label)


class Benzenoid(object):

    properties_erased_by_add = [
        'perimeter',
        'perimeter_vertices',
        'perimeter_set',
        'list_of_holes',
        'list_of_holes_vertices',
    ]
    properties_updated_by_add = [
        'bottom_left_hexagon',
    ]

    def __init__(self, hexagon_list=()):
        """
        Construct a benzenoid from a list of hexagons (faces) given by canonical labels.
        """
        self.vertex_dict = dict()
        self.edge_dict = dict()
        self.face_dict = dict()

        # This dictionary keeps certain properties that are hard to compute
        # (therefore they are reasonable to memoize).
        self.memo = dict()

        # prev_vertex = set()
        # prev_edge = set()
        # prev_face = set()
        for h in hexagon_list:
            self.add_hexagon(h)  # Add hexagons one by one.
            # DEBUG
            # print('new stuff:')
            # print(set(self.vertex_dict.keys()) - prev_vertex)
            # prev_vertex = set(self.vertex_dict.keys())
            # print(set(self.edge_dict.keys()) - prev_edge)
            # prev_edge = set(self.edge_dict.keys())
            # print(set(self.face_dict.keys()) - prev_face)
            # prev_face = set(self.face_dict.keys())
            # print('########################################3')
            # DEBUG

    def get_h(self):
        """
        Return the number of hexagons (faces).
        """
        return len(self.face_dict)

    def get_n(self):
        """
        Return the number of vertices.
        """
        return len(self.vertex_dict)

    def get_m(self):
        """
        Return the number of edges.
        """
        return len(self.edge_dict)

    def _update_bottom_left_hexagon(self, h):
        """
        Update the info on bottom-most left-most hexagon.

        Note: This method is called exclusively by the add_hexagon method.
        """
        xi, eta = h
        if 'bottom_left_hexagon' not in self.memo:
            self.memo['bottom_left_hexagon'] = h
        else:
            xi_curr, eta_curr = self.memo['bottom_left_hexagon']
            if eta < eta_curr or (eta == eta_curr and xi < xi_curr):
                self.memo['bottom_left_hexagon'] = h

    def get_bottom_left_hexagon(self):
        if 'bottom_left_hexagon' not in self.memo:
            raise IndexError('the benzenoid is empty')
        return self.face_dict[self.memo['bottom_left_hexagon']]

    def add_hexagon(self, h):
        """
        Add a hexagon (given by its canonical label) to the benzenoid system.
        """
        if h not in self.face_dict:
            Face(h, self)
            # Update the info on bottom-most left-most hexagon.
            self._update_bottom_left_hexagon(h)
        # Erase stored properties that might change by adding a new hexagon.
        for property_name in self.properties_erased_by_add:
            if property_name in self.memo:
                del self.memo[property_name]

    def list_of_holes(self):
        """
        Return the list of holes. Each hole is represented as list of boundary edges.
        """
        if 'list_of_holes' in self.memo:
            return self.memo['list_of_holes']
        ret = []
        # Build the graph of boundary edges that do not belong to the perimeter.
        boundary_graph = {e: [w for w in e.adjacent_edges() if w.belongs_to_hole()]
                          for e in self.edge_dict.values() if e.belongs_to_hole()}
        discovered = set()
        for e in boundary_graph:
            if e.label in discovered:
                continue
            hole = algorithms.dfs(e, neighbors=lambda w: boundary_graph[w])
            ret.append(hole)
            discovered.update(w.label for w in hole)
        self.memo['list_of_holes'] = ret
        return self.memo['list_of_holes']

    def list_of_holes_vertices(self):
        """
        Return the list of holes. Each hole is prepresented as list of boundary vertices.
        """
        if 'list_of_holes_vertices' in self.memo:
            return self.memo['list_of_holes_vertices']
        ret = []
        hole_list = self.list_of_holes()
        for hole in hole_list:
            n = len(hole)  # Length of the boundary of that hole.
            v_list = []
            for i, e in enumerate(hole):
                u, v = e.incident_vertices()
                v_list.append(u if u in hole[(i+1) % n].incident_vertices() else v)
            ret.append(v_list)
        self.memo['list_of_holes_vertices'] = ret
        return self.memo['list_of_holes_vertices']

    def perimeter(self):
        """
        Return the perimeter (the cycle formed of external edges).

        Note: Some authors call it boundary. (For us the boundary is the union of perimeter and holes.)
        """
        if 'perimeter' in self.memo:
            return self.memo['perimeter']
        e = self.get_bottom_left_hexagon().get_incident_edge(4)
        self.memo['perimeter'] = algorithms.dfs(e, neighbors=lambda w: (d for d in w.adjacent_edges()
                                                                        if d.is_boundary()))
        # Store the labels of vertices on the perimeter in a set data-structure.
        self.memo['perimeter_set'] = {e.label for e in self.memo['perimeter']}
        return self.memo['perimeter']

    def perimeter_vertices(self):
        """
        Return the list of vertices on the perimeter.
        """
        if 'perimeter_vertices' in self.memo:
            return self.memo['perimeter_vertices']
        ret = []
        p = self.perimeter()
        n = len(p)  # Length of the perimeter.
        for i, e in enumerate(p):
            u, v = e.incident_vertices()
            ret.append(u if u in p[(i+1) % n].incident_vertices() else v)
        self.memo['perimeter_vertices'] = ret
        return self.memo['perimeter_vertices']

    def is_connected(self):
        """
        Return True if the benzenoid is connected.
        """
        print(self.face_dict)
        some_face = next(iter(self.face_dict.values()))
        component = algorithms.bfs(some_face, neighbors=lambda w: w.adjacent_faces())
        return len(component) == len(self.face_dict)

    def is_simply_connected(self):
        """
        Return True if and only if this benzenoid system is simply connected.
        """
        return len(self.list_of_holes()) == 0

    def tikz_picture_faces(self, colors=dict(), default_color='VertexColor'):
        """
        TODO: clean up! Remove HACKs.
        """
        output = []
        label_mapping = dict()
        self.perimeter_vertices()
        peri_vert = [v.label for v in self.memo['perimeter_vertices']]
        output_buffer = []
        for node in self.vertex_dict.values():
            x, y = node.get_coordinates()
            tikz_label = '_'.join(str(t) for t in node.label)
            label_mapping[node.label] = tikz_label
            node_color = colors.get(node.label, default_color)
            output.append(r'\coordinate ({0}) at ({1:.6f}, {2:.6f});'.format(
                tikz_label, x, y, node_color))
            output_buffer.append(r'\node[fill={3}] at ({0}) {{}};'.format(
                tikz_label, x, y, node_color))
        peri = {e.label for e in self.memo['perimeter']}
        centres = []
        for face in self.face_dict.values():
            coords = [v.get_coordinates() for v in face.incident_vertices()]
            centres.append(centre_of_mass(coords))
            face_code = r'\draw[fill=FaceColor] {0} -- cycle;'.format(' -- '.join('({0:.5f}, {1:.5f})'.format(x, y) for x, y in coords))
            output.append(face_code)
        bottom_left = min(centres, key=lambda p: (p[1], p[0]))
        bottom_right = min(centres, key=lambda p: (p[1], -p[0]))
        top_left = max(centres, key=lambda p: (p[1], -p[0]))
        top_right = max(centres, key=lambda p: (p[1], p[0]))
        #
        output_buffer.append('% bottom left: {0}'.format(bottom_left))
        output_buffer.append('% bottom right: {0}'.format(bottom_right))
        output_buffer.append('% top left: {0}'.format(top_left))
        output_buffer.append('% top right: {0}'.format(top_right))
        #
        for edge in self.edge_dict.values():
            uv = [label_mapping[w.label] for w in edge.incident_vertices()]
            # HACK
            tralala = 'edge'
            # print(edge.label)
            if edge.label in peri:
                tralala = 'periedge'
            # print(tralala)
            # \draw[periedge] (1_-2_0) -- node [draw=none, black, pos=0.5, sloped, above] {1/2} (1_-2_1);
            # \begin{tikzpicture}[scale=1.2]
            output.append(r'\draw[{2}] ({0}) -- ({1});'.format(uv[0], uv[1], tralala))
            # HACK
            # output.append(r'\draw[edge] ({0}) -- ({1});'.format(*uv))
        return r'''\begin{tikzpicture}[scale=1]
\tikzstyle{every node} = [inner sep=2.5, draw, circle]
\tikzstyle{edge} = [draw, line width=1.0]
\tikzstyle{aedge} = [draw, line width=1.0]
\tikzstyle{periedge} = [draw, line width=1.0]''', output + output_buffer, r'\end{tikzpicture}'
#         return (r'''\begin{tikzpicture}[scale=1]
# \tikzstyle{every node} = [inner sep=3.5, draw, circle]
# \tikzstyle{edge} = [draw, line width=1.0]
# \tikzstyle{periedge} = [draw, line width=1.0]''' +
#                 '\n' + '\n'.join(output + output_buffer) + '\n' + r'\end{tikzpicture}')

    def tikz_picture_simple(self, colors=dict(), default_color='AliceBlue'):
        """
        TODO: clean up! Remove HACKs.
        """
        output = []
        label_mapping = dict()
        self.perimeter_vertices()
        peri_vert = [v.label for v in self.memo['perimeter_vertices']]
        for node in self.vertex_dict.values():
            x, y = node.get_coordinates()
            tikz_label = '_'.join(str(t) for t in node.label)
            label_mapping[node.label] = tikz_label
            node_color = colors.get(node.label, default_color)
            output.append(r'\node[] ({0}) at ({1:.6f}, {2:.6f}) {{}};'.format(
                tikz_label, x, y, node_color))
        peri = {e.label for e in self.memo['perimeter']}
        # print(peri)
        for edge in self.edge_dict.values():
            uv = [label_mapping[w.label] for w in edge.incident_vertices()]
            # HACK
            tralala = 'edge'
            # print(edge.label)
            if edge.label in peri:
                tralala = 'periedge'
            # print(tralala)
            # \draw[periedge] (1_-2_0) -- node [draw=none, black, pos=0.5, sloped, above] {1/2} (1_-2_1);
            # \begin{tikzpicture}[scale=1.2]
            output.append(r'\draw[{2}] ({0}) -- ({1});'.format(uv[0], uv[1], tralala))
            # HACK
            # output.append(r'\draw[edge] ({0}) -- ({1});'.format(*uv))
        return (r'''\begin{tikzpicture}[scale=1]
\tikzstyle{every node} = [inner sep=3.5, draw, circle]
\tikzstyle{edge} = [draw, line width=1.0]
\tikzstyle{periedge} = [draw, line width=1.0]''' +
                '\n' + '\n'.join(output) + '\n' + r'\end{tikzpicture}')

    def tikz_picture(self):
        """
        TODO clean up! Remove HACKs.
        """
        output = []  # TODO: clean up (and generalize) this code!!!
        label_mapping = dict()
        self.perimeter_vertices()
        peri_vert = [v.label for v in self.memo['perimeter_vertices']]
        print(peri_vert)
        hole_dict = {}

        def reduced_fraction(p, q):
            d = fractions.gcd(p, q)
            return p, q
            return p // d, q // d

        pbo = {k: '%d/%d' % reduced_fraction(p, q) for k, (p, q) in self.pauling_bond_orders().items()}
        for i, h in enumerate(self.list_of_holes()):
            for j, e in enumerate(h):
                hole_dict[e.label] = '%d.%d' % (i, j)
        for node in self.vertex_dict.values():
            x, y = node.get_coordinates()
            tikz_label = '_'.join(str(t) for t in node.label)
            label_mapping[node.label] = tikz_label
            node_type = 'male' if node.is_peak() else ('female' if node.is_valley() else '')
            xx = peri_vert.index(node.label) if node.label in peri_vert else ''
            xx = ''
            output.append(r'\node[{3}] ({0}) at ({1:.6f}, {2:.6f}) {{{4}}};'.format(tikz_label, x, y, node_type, xx))
        peri = {e.label for e in self.memo['perimeter']}
        print(peri)
        for edge in self.edge_dict.values():
            uv = [label_mapping[w.label] for w in edge.incident_vertices()]
            # HACK
            tralala = 'edge'
            print(edge.label)
            if edge.label in peri:
                tralala = 'periedge'
            # print(tralala)
            # \draw[periedge] (1_-2_0) -- node [draw=none, black, pos=0.5, sloped, above] {1/2} (1_-2_1);
            # \begin{tikzpicture}[scale=1.2]
            if True:  # HACK: tralala == 'periedge':
                orient = edge.label[-1]
                position = 'below right' if orient == 0 else ('above right' if orient == 1 else 'right')
                output.append(r'\draw[periedge] ({0}) -- node [{3}] {{\footnotesize{{{2}}}}} ({1});'.format(
                    uv[0], uv[1], pbo[edge.label], 'draw=none, black, pos=0.5, {0}'.format(position)
                ))
            else:
                output.append(r'\draw[{2}] ({0}) -- ({1});'.format(uv[0], uv[1], tralala))
            # HACK
            # output.append(r'\draw[edge] ({0}) -- ({1});'.format(*uv))
        #return (r'''\begin{tikzpicture}[scale=0.8]
#\tikzstyle{every node} = [inner sep=2.0, draw, circle]
#\tikzstyle{male} = [fill=blue!50]
#\tikzstyle{female} = [fill=red!50]
#\tikzstyle{edge} = [draw, line width=1.0]
#\tikzstyle{periedge} = [draw, line width=1.0, color=red]''' +
#                '\n' + '\n'.join(output) + '\n' + r'\end{tikzpicture}')
        return (r'''\begin{tikzpicture}[scale=0.8]
\tikzstyle{every node} = [inner sep=2.0, draw, circle]
\tikzstyle{male} = [fill=blue!50]
\tikzstyle{female} = [fill=red!50]
\tikzstyle{edge} = [draw, line width=1.0]
\tikzstyle{periedge} = [draw, line width=1.0, color=red]''',
                output, r'\end{tikzpicture}')

    def atom_bond_lists(self):
        """
        Needed on September 20, 2015.
        """
        atoms = []
        bonds = []
        for node in self.vertex_dict.values():
            x, y = node.get_coordinates()
            atoms.append((x, y))
        for edge in self.edge_dict.values():
            u, v = edge.incident_vertices()
            bonds.append((u.get_coordinates(), v.get_coordinates()))
        return atoms, bonds

    def boundary_edges_code(self):
        """
        Return the (canonical) boundary-edges code of the benzenoid (as a string).

        Note: For more info on boundary-edges code see the paper P. Hansen et al., The boundary-edges code for
        polyhexes, J. Mol. Struct. (Theochem) 363 (1996), no. 2, 237--247.
        """
        vert_degrees = ''.join(str(v.get_degree()) for v in self.perimeter_vertices())

        def add_spaces(s):
            new_s = ''
            while len(s) > 0:
                new_s += s[:3] + ' '
                s = s[3:]
            return new_s.rstrip()

        # print(add_spaces(vert_degrees))
        if '3' not in vert_degrees:
            return '6'  # This must be benzene.
        pos = 0
        while vert_degrees[pos] != '3':
            pos += 1
        code = ''.join(str(len(seg) + 1) for seg in (vert_degrees[pos+1:] + vert_degrees[:pos]).split('3'))
        all_forms = [code[i:] + code[:i] for i in range(len(code))]
        code = code[::-1]  # Perform reverse operation on code.
        all_forms += [code[i:] + code[:i] for i in range(len(code))]
        all_forms.sort()
        return all_forms[-1]  # Return lexicographically largest BEC.

    def myrvold_format(self, edge_length=1.4):
        """
        Return the string that represent this benzenoid in Wendy Myrvold's format.

        Detailed description:
         - The first line contain a single integer n that represents the number of vertices.
           (Vertices are labeled by integers from 0 to n-1.)

         - Each of the next n lines, for i = 0 ... n-1, provides description of i-th vertex in
           the format 'x_i y_i deg_i neighbors_of_i' where x_i and y_i are coordinates of the
           i-th vertex (real numbers), deg_i is the degree of the vertex (an integer), and
           neighbors_of_i is a list of its neighbors.
        """
        n = len(self.vertex_dict)
        wendy_label = {label: i for i, label in enumerate(self.vertex_dict)}
        vertex_data = []
        for k, v in self.vertex_dict.items():
            vertex_data.append([wendy_label[k], v.get_coordinates(edge_length=edge_length),
                                [wendy_label[w.label] for w in v.adjacent_vertices()]])
        vertex_data.sort()  # Sort by canonical labels (0 ... n-1).
        ret = '{0}\n'.format(n) + \
              '\n'.join('{0} {1} {2} {3}'.format(x, y, len(neigh), ' '.join(str(w) for w in neigh))
                        for label, (x, y), neigh in vertex_data)
        return ret

    def nx_graph(self):
        """
        Create the NetworkX's Graph object (using benzenoid's edges and vertices).
        """
        g = networkx.Graph()
        g.add_nodes_from(self.vertex_dict)
        g.add_edges_from([v.label for v in edge.incident_vertices()] for edge in self.edge_dict.values())
        return g

    def adjacency_matrix(self):
        """
        Return the adjacency matrix of the graph (using plain Python).
        """
        g = self.nx_graph()
        canonical_label = {node: label for label, node in enumerate(g.nodes_iter())}
        print(canonical_label)
        ret = [[0 for _ in range(g.order())] for _ in range(g.order())]
        for u, neigh in g.adjacency_iter():
            for v in neigh:
                ret[canonical_label[u]][canonical_label[v]] = 1
        return ret

    def numpy_adjacency_matrix(self):
        """
        Return the adjacency matrix of the graph as a NumPy matrix.
        """
        return networkx.to_numpy_matrix(self.nx_graph())

    def perfect_matchings(self):
        """
        Return the number of perfect matchings.

        Note: Result by Gutman and Polansky.
        """
        # print(self.spectrum())
        eigvals = sorted([float(x) for x in self.spectrum()], key=lambda x: -x)
        n = len(eigvals)
        k = round(functools.reduce(lambda x, y: x*y, [eigvals[i] for i in range(n // 2)]))
        return k

    def pauling_bond_orders(self):
        """
        Return the Pauling bond orders for each bond (as fractions). The function returns
        a dictionary that maps from canonical labels to bond orders.
        """
        g = self.nx_graph()
        canonical_labels = {node: label for label, node in enumerate(g.nodes_iter())}
        adj_inv = numpy.linalg.inv(networkx.to_numpy_matrix(g))
        # print(adj_inv)
        k = self.perfect_matchings()
        ret = dict()
        for label, edge in self.edge_dict.items():
            u, v = [canonical_labels[v.label] for v in edge.incident_vertices()]
            # TODO: hack
            # ret[label] = fractions.Fraction(round(float(k * adj_inv[u, v])), k)
            ret[label] = (round(float(k * adj_inv[u, v])), k)
        return ret

    def sympy_adjacency_matrix(self):
        """
        Return the adjacency matrix of the graph as a SymPy matrix.
        """
        return sympy.Matrix(self.adjacency_matrix())

    def spectrum(self):
        """
        Return the spectrum (as a list of eigenvalues sorted in non-decreasing order) of the
        graphs using numeric computation (i.e. NumPy package).

        Note: The adjacency matrix of a graph is a real symmetric matrix, therefore its eigenvalues
        are all real numbers. According to the NumPy documentation, the eigenvalues are computed using
        LAPACK routines _ssyevd and _heevd.
        """
        return numpy.linalg.eigvalsh(self.numpy_adjacency_matrix())

    def symbolic_spectrum(self):
        """
        Return the spectrum (as a dictionary of eigenvalues) of the graphs that is obtained
        by using symbolic computation (i.e. Sympy library).

        Note: Many eigenvalues may be missing.
        """
        return self.sympy_adjacency_matrix().eigenvals()

    def face_coordinates(self):
        """
        Return the generator that yields coordinates of faces (hexagons) of this benzenoid.
        """
        return self.face_dict.keys()

    def copy(self):
        """
        Create an exact copy of this benzenoid.
        """
        return Benzenoid(self.face_coordinates())

    def empty_face_slots(self):
        """
        Return the set of face coordinates, that are not part of the benzenoid but are adjacent to it.
        """
        ret = set()
        for e in self.perimeter():
            ret.update(f for f in e.incident_faces_candidates() if f not in self.face_dict)
        return ret

    def is_convex(self):
        """
        Return True if and only if the benzenoid is convex.
        """
        return '1' not in self.boundary_edges_code()
