# File for developing OOP for network analysis

# Import packages here
import geopandas as gpd
import rasterio
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
from shapely.geometry import Point
import networkx as nx
from rtree import index


class Networker:
    """ Networker Class """

    def __init__(self, start, end, json):
        self.start = start
        self.end = end
        self.json = json

    def nearest_nodes(self):
        """ Extract nodes nearest to start and end Points """

        start_p = self.start
        end_p = self.end
        json_nodes = self.json
        fid = list(json_nodes)

        # Create index
        node_index = index.Index()
        for n, node in enumerate(json_nodes):
            node_index.insert(n, json_nodes[node]['coords'])

        # Identify node nearest to start
        loc1 = (start_p.x, start_p.y)
        loc1_node = list(node_index.nearest(loc1))
        loc1_fid = fid[loc1_node[0]]
        loc1_coords = []
        for i in node_index.nearest(loc1, num_results=1, objects=True):
            loc1_coords.append(i.bounds[0])
            loc1_coords.append(i.bounds[2])

        # Identify node nearest to end
        loc2 = (end_p.x, end_p.y)
        loc2_node = list(node_index.nearest(loc2))
        loc2_fid = fid[loc2_node[0]]
        loc2_coords = []
        for i in node_index.nearest(loc2, num_results=1, objects=True):
            loc2_coords.append(i.bounds[0])
            loc2_coords.append(i.bounds[2])

        start_node = [loc1_fid, loc1_coords]
        end_node = [loc2_fid, loc2_coords]
        return start_node, end_node

    def dijkstra_path(self, start_node, end_node):
        """ Extracts shortest path between start and end nodes """

        json = self.json

        # Create Graph
        g = nx.Graph()
        for link in json:
            start = json[link]['start']
            end = json[link]['end']
            fid = link
            weight = json[link]['length']
            g.add_edge(start, end, fid=fid, weight=weight)

        # Extract path
        path = nx.dijkstra_path(g, source=start_node, target=end_node, weight='weight')

        # Parse path to a GeoDataFrame
        links = []
        geom = []
        first_node = path[0]
        for node in path[1:]:
            link_fid = g.edges[first_node, node]['fid']
            links.append(link_fid)
            geom.append(LineString(json[link_fid]['coords']))
            first_node = node
        shortest_path_gpd = gpd.GeoDataFrame({'fid': links, 'geometry': geom})

        return shortest_path_gpd

    def naismiths_path(self, elevation, start_node, end_node):
        """ Extracts naismiths path between start and end nodes """
        ### Needs more comments #####

        heights = elevation.read(1)
        spd = float(5000 / 60)
        road_links = self.json

        # Create Graph
        Graph = nx.Graph()
        for l in road_links:
            elevation_time = 0
            full_coords = road_links[l]['coords']

            # Forward
            point_start = Point(tuple(road_links[l]['coords'][0]))
            for p in full_coords:
                point_end = Point(tuple(p))
                start_r, start_l = elevation.index(point_start.x, point_start.y)
                end_r, end_l = elevation.index(point_end.x, point_end.y)
                d_ele = heights[int(end_r), int(end_l)] - heights[int(start_r), int(start_l)]
                if d_ele > 0:
                    elevation_time = float(d_ele / 10) + elevation_time
                point_start = point_end
            time = elevation_time + road_links[l]['length'] / spd
            Graph.add_edge(road_links[l]['start'], road_links[l]['end'], fid=l, weight=time)

            # Reversed
            point_start_reversed = Point(tuple(road_links[l]['coords'][-1]))
            for p in reversed(full_coords):
                point_end = Point(tuple(p))
                start_r, start_l = elevation.index(point_start_reversed.x, point_start_reversed.y)
                end_r, end_l = elevation.index(point_end.x, point_end.y)
                d_ele = heights[int(end_r), int(end_l)] - heights[int(start_r), int(start_l)]
                if d_ele > 0:
                    elevation_time = float(d_ele / 10) + elevation_time
                point_start_reversed = point_end
            time = elevation_time + road_links[l]['length'] / spd
            Graph.add_edge(road_links[l]['start'], road_links[l]['end'], fid=l, weight=time)

        # Extract path
        path = nx.dijkstra_path(Graph, start_node, end_node, weight="weight")

        # Parse path to a GeoDataFrame
        links = []
        geom = []
        first_node = path[0]
        for node in path[1:]:
            link_fid = Graph.edges[first_node, node]['fid']
            links.append(link_fid)
            geom.append(LineString(road_links[link_fid]['coords']))
            first_node = node
        shortest_path_gpd = gpd.GeoDataFrame({'fid': links, 'geometry': geom})

        return shortest_path_gpd
