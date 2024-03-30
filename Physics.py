import phylib;
import sqlite3;
import os;
import math;
import json;
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE      = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON;
DRAG          = phylib.PHYLIB_DRAG;
MAX_TIME      = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL    = 0.01;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";
# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    # generates an SVG representation of a still ball object, including its position and color
    def svg(self):
        colour = BALL_COLOURS[self.obj.still_ball.number % len(BALL_COLOURS)];
        svgStr = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
            self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, colour);
        return svgStr;



class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class
    """
    def __init__(self, number, pos, vel, acc):
        phylib.phylib_object.__init__(self, 
                                      phylib.PHYLIB_ROLLING_BALL,
                                      number, 
                                      pos, vel, acc, 0.0, 0.0);
        self.__class__ = RollingBall;
    
    #generates an SVG representation of a rolling ball object, including its position and color
    def svg(self):
        colour = BALL_COLOURS[self.obj.rolling_ball.number % len(BALL_COLOURS)];
        svgStr = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
            self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, colour);
        return svgStr;

class Hole(phylib.phylib_object):
    def __init__(self, pos):
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HOLE,
                                      0,
                                      pos, None, None, 0.0, 0.0);
        self.__class__ = Hole;
    
    #generates an SVG representation of a hole object, including its position
    def svg(self):
        svgStr = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (
            self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS);
        return svgStr;

class HCushion(phylib.phylib_object):
    def __init__(self,y):
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      0, None, None, None, 0.0, y);
        self.__class__ = HCushion;
    
    #generates an SVG representation of a rectangular object (Hcushion), 
    #with its position based on certain conditions regarding the y-coordinate
    def svg(self):
        #if it's on the left, set to -25
        if self.obj.hcushion.y == 0:
            y = -25;
        else:
            #else set to 2700 (it's on the right)
            y = 2700;
        svgStr = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % y;
        return svgStr;

class VCushion(phylib.phylib_object):
    def __init__(self,x):
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      0, None, None, None, x, 0.0);
        self.__class__ = VCushion;
    
    #generates an SVG representation of a rectangular object (Vcushion), 
    #with its position based on certain conditions regarding the x-coordinate
    def svg(self):
        #if its on the left, set to -25
        if self.obj.vcushion.x == 0:
            x = -25;
        else:
            #else its on the right, set to 1350
            x = 1350;
        svgStr = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % x;
        return svgStr;

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    #generates the SVG representation of the objects in the Physics class instance and returns it as a string
    def svg(self):
        svgStr = HEADER;
        for object in self:
            if object is not None:
                svgStr += object.svg();
        svgStr += FOOTER;
        return svgStr;

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                    Coordinate(0,0),
                    Coordinate(0,0),
                    Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                    Coordinate( ball.obj.still_ball.pos.x,
                    ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    #Searches through a collection of balls to find the cue ball
    def cueBall(self):
        for objt in self:
            #Looks for a ball that's still and has a number 0, if it finds ball, returns it
            if isinstance(objt, StillBall) and objt.obj.still_ball.number == 0:
                return objt
        #No ball found returns None
        return None
    
class Database:
    #Initializes a SQL Database connection
    def __init__( self, reset=False ):
        #If reset true, deletes an existing db file before creating a new one
        if reset == True:
            if os.path.exists('phylib.db'):
                os.remove('phylib.db');
        #sets up cursor for executing SQL commands and calls a method to create necessary db tables
        self.conn = sqlite3.connect('phylib.db')
        self.cur = self.conn.cursor()
        self.createDB()
    
    def createDB(self):
        #Creating tables Ball, TTable, BallTable, Shot, TableShot, Game, Player
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Ball(
                            BALLID      INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
                            BALLNO      INTEGER  NOT NULL,
                            XPOS        FLOAT    NOT NULL,
                            YPOS        FLOAT    NOT NULL,
                            XVEL        FLOAT,
                            YVEL        FLOAT);""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS TTable(
                            TABLEID     INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
                            TIME        FLOAT    NOT NULL);""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS BallTable(
                            BALLID      INTEGER  NOT NULL,
                            TABLEID     INTEGER  NOT NULL,
                            FOREIGN KEY (BALLID) REFERENCES BALL,
                            FOREIGN KEY (TABLEID) REFERENCES TTable);""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Shot(
                            SHOTID      INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
                            PLAYERID    INTEGER  NOT NULL,
                            GAMEID      INTEGER  NOT NULL,
                            FOREIGN KEY (PLAYERID) REFERENCES Player,
                            FOREIGN KEY (GAMEID) REFERENCES Game);""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS TableShot(
                            TABLEID     INTEGER  NOT NULL,
                            SHOTID      INTEGER  NOT NULL,
                            FOREIGN KEY (TABLEID) REFERENCES TTable,
                            FOREIGN KEY (SHOTID) REFERENCES Shot);""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Game(
                            GAMEID      INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMENAME    VARCHAR(64)  NOT NULL);""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Player(
                            PLAYERID    INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMEID      INTEGER  NOT NULL,
                            PLAYERNAME  VARCHAR(64)  NOT NULL,
                            FOREIGN KEY (GAMEID) REFERENCES Game);""")
        self.conn.commit()
        self.cur.close()
        

    def readTable(self, tableID):
        self.conn = sqlite3.connect('phylib.db')
        self.cur = self.conn.cursor()

        #Retrieving ball data from db based on table ID
        self.cur.execute("""SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                        FROM BallTable
                        JOIN Ball ON BallTable.BALLID = Ball.BALLID
                        WHERE BallTable.TABLEID = ?;""", (tableID + 1,))
        ballsData = self.cur.fetchall()
        if len(ballsData) == 0:
            self.cur.close()
            return None
        
        table = Table()
        #Creates ball objects w/ relevant properties, and populates table object
        for balls in ballsData:
            ballID, ballNO, xPos, yPos, xVel, yVel = balls
            pos = Coordinate(xPos, yPos)
            vel = None
            acc = Coordinate(0,0)
            if xVel is not None and yVel is not None:
                vel = Coordinate(xVel, yVel)
                speed = math.sqrt(xVel ** 2 + yVel ** 2)
                if speed > VEL_EPSILON:
                    acc.x = ((xVel * -1.0) /speed) * DRAG
                    acc.y = ((yVel * -1.0) /speed) * DRAG
                else:
                    acc.x = 0;
                    acc.y = 0;
            if vel is None:
                table += StillBall(ballNO, pos)
            else:
                table += RollingBall(ballNO, pos, vel, acc)
        
        #Retrieves time and assigns time info to the table before returning it
        self.cur.execute("SELECT TIME FROM TTable WHERE TABLEID = ?;", (tableID + 1,))
        time = self.cur.fetchone()[0]
        table.time = time
        self.conn.commit()
        self.cur.close()
        return table
    
    def writeTable(self,table):
        self.conn = sqlite3.connect('phylib.db')
        self.cur = self.conn.cursor()

        #Writes data from table object into db
        #Inserts the table's time into the TTable and retrieves the tableID
        self.cur.execute("INSERT INTO TTable (TIME) VALUES (?);", (table.time,))
        tableID = self.cur.lastrowid

        """For each object(StillBall/RollingBall) in the table, it inserts data into the Ball table, associating 
        it w/ the tableID in the BallTable table"""
        for objt in table:
            if isinstance(objt, StillBall):
                self.cur.execute("""INSERT INTO Ball (BALLNO, XPOS, YPOS)
                                    VALUES (?, ?, ?);""", (objt.obj.still_ball.number, objt.obj.still_ball.pos.x,
                                                            objt.obj.still_ball.pos.y))
                ballID = self.cur.lastrowid
                self.cur.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                                    VALUES (?, ?);""",(ballID, tableID))
            elif isinstance(objt, RollingBall):
                self.cur.execute("""INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                    VALUES (?, ?, ?, ?, ?);""", (objt.obj.rolling_ball.number, objt.obj.rolling_ball.pos.x,
                                                                 objt.obj.rolling_ball.pos.y, objt.obj.rolling_ball.vel.x, objt.obj.rolling_ball.vel.y))
                ballID = self.cur.lastrowid
                self.cur.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                                    VALUES (?, ?);""",(ballID, tableID))
        self.conn.commit()
        self.cur.close()
        return tableID - 1
        
    def close(self):
        #Commits the connection + closes it
        self.conn.commit()
        self.conn.close()

    def getGame(self,gameID):
        self.cur = self.conn.cursor()
        #Retrieves game info based on a given gameID from db
        #Fetches the game name, p1 name, and p2 name from Game + Player tables
        self.cur.execute("""SELECT g.GAMENAME, p1.PLAYERNAME AS PLAYER1NAME, p2.PLAYERNAME AS PLAYER2NAME
                         FROM Game AS g
                         JOIN Player AS p1 ON g.GAMEID = p1.GAMEID AND p1.PLAYERID < 
                            (SELECT PLAYERID FROM Player
                            WHERE GAMEID = g.GAMEID AND PLAYERNAME = p1.PLAYERNAME ORDER BY PLAYERID LIMIT 1)
                         JOIN Player AS p2 ON g.GAMEID = p2.GAMEID AND p2.PLAYERID >
                            (SELECT PLAYERID FROM Player
                            WHERE GAMEID = g.GAMEID AND PLAYERNAME = p2.PLAYERNAME ORDER BY PLAYERID LIMIT 1)
                         WHERE g.GAMEID = ?;""", (gameID + 1))
        gData = self.cur.fetchone()
        #Commits the transaction and closes the cursor before returning the retrieved data or none if no data is found
        if gData:
            gameName, player1Name, player2Name = gData
            self.conn.commit()
            self.cur.close()
            return gameName, player1Name, player2Name
        else:
            self.conn.commit()
            self.cur.close()
            return None
        
    def setGame(self, gameName, player1Name, player2Name):
        self.cur = self.conn.cursor()
        #Inserts game info into db
        #Adds a new entry into the Game table w/ provided game name and retrieves gameID
        self.cur.execute("INSERT INTO Game (GAMENAME) VALUES (?);", (gameName,))
        gameID = self.cur.lastrowid
        #Adds entries into the Player table for p1 and p2, associating them w/ same gameID
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?);", (gameID, player1Name))
        player1ID = self.cur.lastrowid
        self.cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?);", (gameID, player2Name))
        player2ID = self.cur.lastrowid
        self.conn.commit()
        self.cur.close()
        return gameID
    
    #Records a new shot made by a player in a game in db
    def newShot(self, playerName, gameID):
        self.cur = self.conn.cursor()
        """
        Checks if the provided gameID is valid by counting number of occurences 
        of the gameID in the Game table
        """
        self.cur.execute("SELECT COUNT(*) FROM Game WHERE GAMEID = ?;", (gameID,))
        #If count = 0, raises ValueError indicating invalid gameID
        if self.cur.fetchone()[0] == 0:
            raise ValueError(f"Invalid gameID: {gameID}")
        #Retrieves the playerID associated w/ the provided player name and gameID from the Player table
        self.cur.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ? AND GAMEID = ?;", (playerName, gameID))
        playerRow = self.cur.fetchone()
        #No player found w/ the provided name in the specified game, raise ValueError
        if playerRow is None:
            raise ValueError(f"Player '{playerName}' doesn't exist in game w/ ID {gameID}")
        """
        After ensuring the validity of the player + gameID, inserts a new entry into the Shot table
        associating it with the player and gameIDs
        """
        playerID = playerRow[0]
        self.cur.execute("""INSERT INTO Shot (PLAYERID, GAMEID) 
                            VALUES (?,?);""", (playerID, gameID))
        shotID = self.cur.lastrowid
        self.conn.commit()
        self.cur.close()
        return shotID
    
class Game:
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        #Create db object for db interaction
        self.db = Database()
        #If only gameID provided, retrieves game details from db + any other combo of arguements raise ValueError
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            self.gameID = gameID + 1
            gameName, player1Name, player2Name = self.db.getGame(gameID)
            if gameName is not None:
                self.gameName = gameName
                self.player1Name = player1Name
                self.player2Name = player2Name
            else:
                raise ValueError("Invalid gameID provided")
        #If gamename, p1name, and p2name are provided, it sets up a new game in the db + any other combo of arguements raise TypeError
        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            self.gameID = None
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.gameID = self.db.setGame(gameName, player1Name, player2Name)
        else:
            raise TypeError("Invalid combination of arguements provided to the constructor")
        
    def shoot(self, gameName, playerName, table, xvel, yvel):
        # self.db.cur = self.db.conn.cursor()

        # #Initializes a new shot in the db for the given player + game
        # gameID = self.gameID
        # shotID = self.db.newShot(playerName, gameID)
        
        #Retrieves the cueBall's position and sets its type to a rolling ball w/ provided vel
        cue_ball = table.cueBall()   
        
        xpos = cue_ball.obj.still_ball.pos.x
        ypos = cue_ball.obj.still_ball.pos.y
            
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL
        cue_ball.obj.rolling_ball.number = 0
        cue_ball.obj.rolling_ball.pos.x = xpos
        cue_ball.obj.rolling_ball.pos.y = ypos
        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel
        
        #Calculates acc of the cueball based on the vel
        if xvel is not None and yvel is not None:
            speed = math.sqrt(xvel ** 2 + yvel ** 2)
            if speed > VEL_EPSILON:
                cue_ball.obj.rolling_ball.acc.x = ((xvel * -1.0) / speed) * DRAG
                cue_ball.obj.rolling_ball.acc.y = ((yvel * -1.0) / speed) * DRAG
            else:
                cue_ball.obj.rolling_ball.acc.x = 0
                cue_ball.obj.rolling_ball.acc.y = 0
            
        segmentT = table.segment()
        #Iterates through segmets of the table's motion
        while segmentT is not None:
            #For each segment
            segmentL = segmentT.time - table.time
            frameNums = math.floor(segmentL / FRAME_INTERVAL)
            for i in range(frameNums):
                #calculates the table's state at diff frames
                tPassed = i * FRAME_INTERVAL
                newT = table.roll(tPassed)
                newT.time = table.time + tPassed

                #+ updates time 
                table = segmentT
                segmentT = table.segment()
                self.table = table

            if segmentT is None:
                    cue_ball = table.cueBall();
                    if cue_ball is None:
                        pos = Coordinate(675, 2025)
                        cue_ball = StillBall(0,pos)
                        table += cue_ball
                        svg = table.svg()
                        svg = f'<g id = "frame -{frame_id}">(svg)</g>'
                        entire_svg.append(svg)
                        frame_id += 1
            return json.dumps({
                'svg_frames': entire_svg,
                'framesC': frame_id,
            });

    def get_most_recent_table(self):
        return self.table
        


    

        