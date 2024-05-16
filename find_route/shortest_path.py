import pandas as pd
from openrouteservice import client
from openrouteservice import distance_matrix, directions
from ortools.constraint_solver import pywrapcp
import json
import time


# def make_distance_matrix(location):
#   request = {'locations': location,
#            'profile': 'foot-hiking',
#            'metrics': ["distance","duration"]}

#   matrix = ors.distance_matrix(**request)
#   print("Calculated {}x{} routes.".format(len(matrix["distances"]), len(matrix["distances"][0])))
#   return matrix


# def get_optimal_coords(places_coords, matrix):
#   tsp_size = len(places_coords)
#   num_routes = 1
#   start = 0  # arbitrary start location

#   optimal_coords = []
  
#   if tsp_size > 0:
#     manager = pywrapcp.RoutingIndexManager(tsp_size, num_routes, start)
#     routing = pywrapcp.RoutingModel(manager)

#     def distance_callback(from_index, to_index):
#           """Returns the distance between the two nodes."""
#           # Convert from routing variable Index to distance matrix NodeIndex.
#           from_node = manager.IndexToNode(from_index)
#           to_node = manager.IndexToNode(to_index)
#           return int(matrix['durations'][from_node][to_node])

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)

#     # Solve, returns a solution if any.
#     assignment = routing.Solve()
#     if assignment:
#           # Total cost of the 'optimal' solution.
#           #print("Total dist: " + str(round(assignment.ObjectiveValue(), 3) / 60) + " km\n")
#           index = routing.Start(start)  # Index of the variable for the starting node.
#           # while not routing.IsEnd(index):
#           for node in range(routing.nodes()):
#               # IndexToNode has been moved from the RoutingModel to the RoutingIndexManager
#               optimal_coords.append(places_coords[manager.IndexToNode(index)])
#               index = assignment.Value(routing.NextVar(index))
#           optimal_coords.append(places_coords[manager.IndexToNode(index)])
#           optimal_coords.pop(0)
#   return optimal_coords


def get_optimal_route(places_coords, profile):#, matrix):
  # optimal_coords = get_optimal_coords(places_coords, matrix)

  request = {'coordinates': places_coords,
          'profile': profile,
          'geometry': 'true',
          'format_out': 'geojson',
          'units':"km",
          'radiuses':[100000]
          #            'instructions': 'false'
          }
  optimal_route = ors.directions(**request)
  return optimal_route

  


df_coords = pd.read_csv('WayPoint_coords.csv')

api_key = '5b3ce3597851110001cf62485a12ee99ab524a439d70f849aeeb567a'
ors = client.Client(key=api_key)

optimal_routes = {}

places_coords=[]
unique_names = df_coords["Наименование маршрута"].unique()

for i in range(round(len(unique_names))):
  # получаем точки маршрута по имени
  way_name_df = df_coords[df_coords["Наименование маршрута"] == unique_names[i]]
  way_name_df.reset_index(drop= True , inplace= True )

  # if way_name_df.shape[0]>=70:
  #   for j in range(way_name_df.shape[0]/2):
  #     places_coords.append([way_name_df['lon'][j], way_name_df['lat'][j]])
  #     try:
  #       optimal_route = get_optimal_route(places_coords)
  #       name = unique_names[i]
  #       optimal_routes[name]=optimal_route
  #     except Exception as e:
  #       print("The error is:", e)
  #   places_coords=[]
  #   for j in range(way_name_df.shape[0]/2, way_name_df.shape[0]):
  #     places_coords.append([way_name_df['lon'][j], way_name_df['lat'][j]])
  
  for j in range(way_name_df.shape[0]):
      places_coords.append([way_name_df['lon'][j], way_name_df['lat'][j]])

  try:
      # расчитываем матрицу расстояний по координатам
      # matrix = make_distance_matrix(places_coords)

      # получаем оптимальный маршрут
      optimal_route = get_optimal_route(places_coords,'foot-hiking')
      name = unique_names[i]
      optimal_routes[name]=optimal_route

      duration = optimal_route['features'][0]['properties']['summary']['duration']
      distance = optimal_route['features'][0]['properties']['summary']['distance']
      print(duration, distance)
  except Exception as e:
      print("The error is:", e)
      try:
        optimal_route = get_optimal_route(places_coords,'driving-car')
        name = unique_names[i]
        optimal_routes[name]=optimal_route
        duration = optimal_route['features'][0]['properties']['summary']['duration']
        distance = optimal_route['features'][0]['properties']['summary']['distance']
        print(duration, distance)
      except Exception as e:
         print("Error 2 is:", e)
  places_coords=[]
  time.sleep(5)

print(optimal_routes.keys())
with open('Optimal_routes.geojson', 'w', encoding='utf-8') as f: 
      json.dump(optimal_routes, f)
