import pandas as pd
import folium
from weighted_graph import WeightedGraph
from vertex import Vertex


class WarsawNavigator:
    def __init__(self, nodes_file, connections_file):
        self.graph = WeightedGraph()
        self.node_data = {}
        self.letter_to_index = {}
        self._load_nodes(nodes_file)
        self._load_connections(connections_file)

    def _load_nodes(self, filename):
        df = pd.read_csv(filename)
        for idx, row in df.iterrows():
            vertex = Vertex(row['Node'])
            self.graph.addVertex(vertex)
            self.letter_to_index[row['Node']] = idx
            self.node_data[row['Node']] = {
                'name': row['Location'],
                'lat': row['Latitude'],
                'lon': row['Longitude']
            }

    def _load_connections(self, filename):
        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            from_idx = self.letter_to_index[row['Node_From']]
            to_idx = self.letter_to_index[row['Node_To']]
            time = row['Travel_Time_Minutes']
            self.graph.addEdge(from_idx, to_idx, time)

    def find_route(self, start_letter, end_letter):
        start_idx = self.letter_to_index[start_letter]
        end_idx = self.letter_to_index[end_letter]
        return self.graph.shortestPath(start_idx, end_idx)

    def create_map(self):
        warsaw_center = [52.2297, 21.0122]
        m = folium.Map(location=warsaw_center, zoom_start=12)
        
        for letter, data in self.node_data.items():
            folium.Marker(
                location=[data['lat'], data['lon']],
                popup=f"{letter}: {data['name']}",
                tooltip=f"{letter}: {data['name']}",
                icon=folium.Icon(color='green', icon='info-sign')
            ).add_to(m)
        
        added_edges = set()
        for i in range(self.graph.nVertices()):
            for j in self.graph.adjacentVertices(i):
                if (i, j) not in added_edges and (j, i) not in added_edges:
                    from_letter = self.graph.getVertex(i).name
                    to_letter = self.graph.getVertex(j).name
                    from_data = self.node_data[from_letter]
                    to_data = self.node_data[to_letter]
                    
                    folium.PolyLine(
                        locations=[[from_data['lat'], from_data['lon']], 
                                   [to_data['lat'], to_data['lon']]],
                        color='black',
                        weight=2,
                        opacity=0.6
                    ).add_to(m)
                    added_edges.add((i, j))
        
        return m

    def create_path_map(self, path):
        warsaw_center = [52.2297, 21.0122]
        m = folium.Map(location=warsaw_center, zoom_start=12)
        
        path_letters = self.graph.letters_instead_of_indexes(path)
        
        for letter, data in self.node_data.items():
            if letter in path_letters:
                color = 'green'
            else:
                color = 'orange'
            
            folium.Marker(
                location=[data['lat'], data['lon']],
                popup=f"{letter}: {data['name']}",
                tooltip=f"{letter}: {data['name']}",
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(m)
        
        for i in range(len(path) - 1):
            from_idx = path[i]
            to_idx = path[i + 1]
            from_letter = self.graph.getVertex(from_idx).name
            to_letter = self.graph.getVertex(to_idx).name
            from_data = self.node_data[from_letter]
            to_data = self.node_data[to_letter]
            
            folium.PolyLine(
                locations=[[from_data['lat'], from_data['lon']], 
                           [to_data['lat'], to_data['lon']]],
                color='red',
                weight=5,
                opacity=0.8
            ).add_to(m)
        
        return m

    def print_route_details(self, start_letter, end_letter):
        path = self.find_route(start_letter, end_letter)
        letters = self.graph.letters_instead_of_indexes(path)
        total_time = self.graph.total_time(path)
        
        print(f"\n{'='*60}")
        print(f"Route from {start_letter} to {end_letter}")
        print(f"{'='*60}")
        
        print("\nPath (Letters):")
        print(" → ".join(letters))
        
        print("\nPath (Locations):")
        for letter in letters:
            print(f"  {letter}: {self.node_data[letter]['name']}")
        
        print(f"\nTotal Travel Time: {total_time} minutes")
        print(f"{'='*60}\n")
