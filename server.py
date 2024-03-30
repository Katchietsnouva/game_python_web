import os;
import Physics;
import math;
import sys;
import json;
from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;

game = None;
tableId = None;
table = Physics.Table();
db = Physics.Database(reset=True);
db.createDB();

BALL_GAP = 2.0;
RACK_POSITION_X = Physics.TABLE_WIDTH / 2
RACK_POSITION_Y = Physics.TABLE_LENGTH / 4  # You can adjust this if needed

# Cue ball position
CUE_BALL_X = Physics.TABLE_WIDTH / 2
CUE_BALL_Y = Physics.TABLE_LENGTH * 3 / 4  # Or some other position that suits your table layout

# Calculate the direction vector from the apex ball to the cue ball
direction_x = CUE_BALL_X - RACK_POSITION_X
direction_y = CUE_BALL_Y - RACK_POSITION_Y

# Normalize the direction vector (to have a length of 1)
magnitude = math.sqrt(direction_x**2 + direction_y**2)
direction_x /= magnitude
direction_y /= magnitude

# Adjust positions of the balls in the triangle according to the direction vector
# We will move backwards from the rack position to the top of the triangle
balls_positions = []
for row in range(5):
    for col in range(row + 1):
        # Determine the center of the row
        row_center_x = RACK_POSITION_X - direction_x * (row * (Physics.BALL_RADIUS * 2 + BALL_GAP) * (math.sqrt(3) / 2))
        row_center_y = RACK_POSITION_Y - direction_y * (row * (Physics.BALL_RADIUS * 2 + BALL_GAP) * (math.sqrt(3) / 2))
        
        # Offset each ball in the row from the center
        offset_x = (col - row / 2.0) * (Physics.BALL_RADIUS * 2 + BALL_GAP)
        offset_y = offset_x * math.sqrt(3) / 2  # 30 degrees to either side for equilateral triangle spacing
        ball_x = row_center_x + offset_x * direction_y  # Swap X/Y for perpendicular
        ball_y = row_center_y - offset_x * direction_x  # Swap X/Y for perpendicular
        
        balls_positions.append((ball_x, ball_y))

# Now add the balls to the table using the positions calculated
# The 8-ball (black ball) should be at the middle of the triangle, which is ball number 5 in our enumeration
ball_numbers = [1, 2, 3, 4, 8, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]


for index, (x, y) in enumerate(balls_positions):
    ball_number = ball_numbers[index]
    ball = Physics.StillBall(ball_number, Physics.Coordinate(x, y))
    table += ball

# Add the cue ball
cue_ball = Physics.StillBall(0, Physics.Coordinate(CUE_BALL_X, CUE_BALL_Y))
table += cue_ball

tableId = db.writeTable(table);
frames = []

def generate_svg_content():
    # ... your existing code to generate the SVG content
    svg_content = table.svg()  # This is just a placeholder for however you get the SVG content

    # Add the cue ball to the SVG content
    # The cx and cy attributes should be the center coordinates of the cue ball on the table
    cue_ball_svg = f'<circle id="cueBall" cx="{CUE_BALL_X}" cy="{CUE_BALL_Y}" r="28" fill="white" />'
    
    # Insert the cue ball SVG before the closing tag of the SVG content
    svg_content_with_cue_ball = svg_content.replace('</svg>', cue_ball_svg + '</svg>')

    return svg_content_with_cue_ball

class MyHandler( BaseHTTPRequestHandler ):

    
    def do_GET(self):
        global table
        parsed = urlparse(self.path)
        #check if web-pages match the list
        if parsed.path == "/index.html":
            try:
                fp = open('index.html')
                page = fp.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(page))
                self.end_headers();
                self.wfile.write(bytes(page, "UTF-8"))
            except FileNotFoundError:
                #if file not found, response 404 (Not found)
                self.send_response(404);
                self.end_headers();
                #Write a corresponding error message to the response body
                self.wfile.write(b'404 Not Found!');
        elif parsed.path == "/shoot.html":
            try:
                svg_content = generate_svg_content()
                with open('shoot.html') as fp:
                    page_template = fp.read()
                
                page = page_template.replace('{svg_content}', svg_content);
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(page))
                self.end_headers();
                self.wfile.write(bytes(page, "UTF-8"))
            except FileNotFoundError:
                #if file not found, response 404 (Not found)
                self.send_response(404);
                self.end_headers();
                #Write a corresponding error message to the response body
                self.wfile.write(b'404 Not Found');
        #checks if the requested path starts w/ '/table-' and ends w/ '.svg'
        elif parsed.path == "/styles.css":
            try:
                fp = open('styles.css')
                page = fp.read()
                self.send_response(200);
                self.send_header( "Content-type", "text/css" );
                self.send_header("Content-length", len(page))
                self.end_headers();
                self.wfile.write(bytes(page, "UTF-8"))
            except FileNotFoundError:
                #if file not found, response 404 (Not found)
                self.send_response(404);
                self.end_headers();
                #Write a corresponding error message to the response body
                self.wfile.write(b'404 Not Found');
        elif parsed.path == "/main.js":
            try:
                fp = open('main.js')
                page = fp.read()
                self.send_response(200);
                self.send_header( "Content-type", "text/javascript" );
                self.send_header("Content-length", len(page))
                self.end_headers();
                self.wfile.write(bytes(page, "UTF-8"))
            except FileNotFoundError:
                #if file not found, response 404 (Not found)
                self.send_response(404);
                self.end_headers();
                #Write a corresponding error message to the response body
                self.wfile.write(b'404 Not Found');
        elif parsed.path == "/display.html":
            table = db.readTable(tableId);
            svg = table.svg

            self.send_response(200);
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(svg));
            self.send_header( "Access-Control-Allow-Origin", "*" );
            self.end_headers();
            self.wfile.write(bytes(svg, "utf-8"));
        else:
            #Unsuccessful = 404
            self.send_response(404);
            self.end_headers();
            self.wfile.write(b'404 Not Found');
    def do_POST(self):
        global game
        global table
        global frames
        #Parsing URL path of the incoming POST request
        parsed = urlparse(self.path);
        #Check if requested path is '/display.html'
        if parsed.path == '/display.html':
            #Getting the content length of the POST request body
            contentLength = int(self.headers.get('Content-length'));
            #Reading the POST data from the request body
            data = self.rfile.read(contentLength);
            #parse the POST data into a dictionary
            postData = dict(parse_qsl(data.decode()));
            
            game = Physics.Game(None, "Game", postData["player1Name"], postData["player2Name"]);
            
            #Send the HTTP response w/ 200 (OK)
            self.send_response(303);
            self.send_header('Location', '/shoot.html')
            self.end_headers();
            
        elif parsed.path == '/shoot.html':
            try:
                content_length = int(self.headers.get('Content-Length'))
                post_data = self.rfile.read(content_length).decode('utf-8')
                post_data = json.loads(post_data)  # Parse JSON data

                # Logging to check what data is being received
                print("Received POST data:", post_data)

                # Check if all necessary keys are present
                if 'playerName' not in post_data or 'vel_x' not in post_data or 'vel_y' not in post_data:
                    raise KeyError("Required data keys are missing.")

                # Your existing game logic
                result = game.shoot("Game", post_data['playerName'], table, float(post_data['vel_x']), float(post_data['vel_y']))
        
                shotData = json.loads(result)
                frames = shotData('svg_frames')
                frameC = shotData('frame_count')

                db.writeTable(shotData);
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Shot processed'}).encode());
            except KeyError as e:
                print("Key Error:", e)
                self.send_error(400, "Bad Request: Missing data in POST request")
            except json.JSONDecodeError:
                print("Invalid JSON")
                self.send_error(400, "Bad Request: Invalid JSON format")
            except Exception as e:
                print("An error occurred:", e)
                self.send_error(500, "Internal Server Error")
        else:
            #Unsuccessful Path = 404
            self.send_response(404);
            self.end_headers();
            self.wfile.write(b'404 Not Found');
if __name__ == '__main__':
    #Create an instance of the HTTPServer class, specifying the server address & request handler class
    httpd = HTTPServer (('localhost', int(sys.argv[1])), MyHandler);
    print(f'Server listening on port: ', int(sys.argv[1]));
    #Start server request indefinetly
    httpd.serve_forever();
