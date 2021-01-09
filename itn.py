# This is where OOP for analysing data will be developed.

# Import packages here
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
from shapely.geometry import Point
import networkx as nx
from rtree import index

# ITN ANALYSIS CLASS

def nearest_node(point, json_nodes):
    json_nodes = json_nodes['roadnodes']
    fid = list(json_nodes)

    # Create index
    node_index = index.Index()
    for n, node in enumerate(json_nodes):
        node_index.insert(n, json_nodes[node]['coords'])
    # Identify nodes nearest to user and highest point
    loc = (point.x, point.y)
    loc_node = list(node_index.nearest(loc))
    loc_fid = fid[loc_node[0]]
    loc_coords = []
    for i in node_index.nearest(loc, num_results=1, objects=True):
        loc_coords.append(i.bounds[0])
        loc_coords.append(i.bounds[2])
    start_to_end = [loc_fid, loc_coords]
    return start_to_end


def shortest_path(start, end, json):
    g = nx.Graph()
    for link in json:
        start = json[link]['start']
        end = json[link]['end']
        fid = link
        weight = json[link]['length']
        g.add_edge(start, end, fid=fid, weight=weight)

    path = nx.dijkstra_path(g, source=start, target=end, weight='weight')

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


def naismiths_path(json, elevation, start_node, end_node):
    heights = elevation.read(1)
    spd = float(5000 / 60)
    road_links = json
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

    path = nx.dijkstra_path(Graph, start_node, end_node, weight="weight")

    links = []
    geom = []
    first_node = path[0]
    for node in path[1:]:
        link_fid = Graph.edges[first_node, node]['fid']
        links.append(link_fid)
        geom.append(LineString(json[link_fid]['coords']))
        first_node = node
    shortest_path_gpd = gpd.GeoDataFrame({'fid': links, 'geometry': geom})

    return shortest_path_gpd