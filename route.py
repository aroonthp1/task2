import re

def get_positive_integer(prompt, max_routes): ##function created for taking positive number 
    while True:    ## using while loop for condion check only for value greater than zero, if other value it generate message .
        try:
            #converting user input to integer
            value = int(input(prompt))
            if value < 0:  #if value is less opr negtive it raise an error message
                raise ValueError("Invalid value. Please enter a non-negative integer")
            if value > max_routes: #condition to check if value is greater than maximum value
                raise ValueError("Please enter a number less than or equal to total number of routes")
            return value
        except ValueError as e:
            # print("Please enter a positive integer.")
            print(e)

def read_route_data(file_name): #function to read  the file 
    route_data = []
    route_numbers = set()
    
    try:
        with open(file_name, 'r') as file:
            for line in file:
                parts = line.split(',')
                
                if len(parts) != 3:
                    raise ValueError("Error reading data.\nPlease ensure each line of routes.txt contains a route number, followed by a comma, followed by the number of happy customers, followed by a comma, followed by the number of unhappy customers and that no route is repeated throughout the file")
                
                route_number = parts[0]
                n_happy = parts[1]
                n_unhappy = parts[2]
                
                # if not n_happy.isdigit() or not route_number.isdigit() or not n_unhappy.isdigit():
                if bool(re.search(r' ', n_happy)) or bool(re.search(r' ', n_unhappy)) or bool(re.search(r' ', route_number)):
                # if bool(re.search(r'\s', n_happy)) or bool(re.search(r'\s', route_number)):
                    raise ValueError("Invalid values: " + line)
                
                n_happy = int(n_happy)
                n_unhappy = int(n_unhappy)
                
                if route_number in route_numbers:
                    raise ValueError("Duplicate route number: " + route_number)
                
                route_numbers.add(route_number)
                # calculating the happy ratio (avoid divison by zero)
                if n_unhappy == 0:
                    happy_ratio = 0
                else:
                    happy_ratio = n_happy / n_unhappy
                
                route_data.append({
                    'route_number': route_number,
                    'n_happy': n_happy,
                    'n_unhappy': n_unhappy,
                    'happy_ratio': happy_ratio
                })
        
        return route_data
    
    except FileNotFoundError:
        raise FileNotFoundError("File not found: " + file_name)
    except ValueError as e:
        raise ValueError(str(e))

def sort_route_data(route_data):
    # Sort the route data based on happy_ratio, handling routes with ratio 0
    sorted_routes = sorted(route_data, key=lambda route: (route['happy_ratio'] if route['happy_ratio'] > 0 else float('inf')))
    return sorted_routes

def main():
    file_name = 'routes.txt'
    
    try:
        route_data = read_route_data(file_name)
        route_data = sort_route_data(route_data)
        total_buses = get_positive_integer("How many routes can have an extra bus?",len(route_data))
        print("You should add busses for the following routers:")
        for number in range(total_buses):
            print(route_data[number].get('route_number'))
        # print(total_buses)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
