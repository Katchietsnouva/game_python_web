#include "phylib.h"

//Part 1

//creates and initializes a new physics library object representing a still ball with a specified number and position,
//allocating memory for the object and setting its attributes accordingly.
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos){
    phylib_object *newStillBall;
    newStillBall = (phylib_object*) malloc(sizeof(phylib_object));
    if(newStillBall == NULL){
        return NULL;
    }
    
    newStillBall -> type = PHYLIB_STILL_BALL;
    newStillBall-> obj.still_ball.number = number;
    newStillBall -> obj.still_ball.pos.x = pos -> x;
    newStillBall -> obj.still_ball.pos.y = pos -> y;
    
    return newStillBall;
}

//Allocates memory for a new physics library rolling ball object and initializes its attributes based on input parameters, 
//returning a pointer to the created object.
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos,
phylib_coord *vel, phylib_coord *acc){
    phylib_object *newRollBall = (phylib_object*) malloc(sizeof(phylib_object));
    if(newRollBall == NULL){
        return NULL;
    }
    
    newRollBall -> type = PHYLIB_ROLLING_BALL;
    newRollBall -> obj.rolling_ball.number = number;

    newRollBall -> obj.rolling_ball.pos.x = pos -> x;
    newRollBall -> obj.rolling_ball.vel.x = vel -> x;
    newRollBall -> obj.rolling_ball.acc.x = acc -> x;
    newRollBall -> obj.rolling_ball.pos.y = pos -> y;
    newRollBall -> obj.rolling_ball.vel.y = vel -> y;
    newRollBall -> obj.rolling_ball.acc.y = acc -> y;
   
    return newRollBall;
}

//creates and initializes a new physics library object representing a hole at the specified coordinates,
//returning a pointer to the object or NULL if memory allocation fails.
phylib_object *phylib_new_hole(phylib_coord *pos){
    phylib_object *newHole = (phylib_object*) malloc(sizeof(phylib_object));
    if(newHole == NULL){
        return NULL;
    }
    
    newHole -> type = PHYLIB_HOLE;
        
    newHole -> obj.hole.pos.x = pos -> x;
    newHole -> obj.hole.pos.y = pos -> y;
    
    return newHole;
}

//creates a new phylib_object representing a cushion in a physics library,
//initializes its type and y-coordinate, and returns a pointer to the newly created object.
phylib_object *phylib_new_hcushion(double y){
    phylib_object *newHCushion = (phylib_object*) malloc(sizeof(phylib_object));
    if(newHCushion == NULL){
        return NULL;
    }
   
    newHCushion -> type = PHYLIB_HCUSHION;
    newHCushion -> obj.hcushion.y = y;
    
    return newHCushion;

}
//creates a new phylib_object representing a cushion in a physics library, 
//initializes its type and x-coordinate, and returns a pointer to the newly created object.
phylib_object *phylib_new_vcushion(double x){
    phylib_object *newVCushion = (phylib_object*) malloc(sizeof(phylib_object));
    if(newVCushion == NULL){
        return NULL;
    }
    
    newVCushion -> type = PHYLIB_VCUSHION;
    newVCushion -> obj.vcushion.x = x;
    
    return newVCushion;
}

//creates and initializes a new table structure with various components, 
//including cushions and holes, and returns a pointer to the newly created table.
phylib_table *phylib_new_table(void){
    phylib_table *newTable = (phylib_table*) malloc(sizeof(phylib_table));
    if(newTable == NULL){
        return NULL;
    }
    
    newTable -> time = 0.0;
    newTable -> object[0] = phylib_new_hcushion(0.0);
    newTable -> object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable -> object[2] = phylib_new_vcushion(0.0);
    newTable -> object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    phylib_coord tLeftHole = {0.0,0.0};
    phylib_coord mLeftHole = {0.0, PHYLIB_TABLE_WIDTH};
    phylib_coord bLeftHole = {0.0,PHYLIB_TABLE_LENGTH};
    phylib_coord tRightHole = {PHYLIB_TABLE_WIDTH, 0.0};
    phylib_coord mRightHole = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH};
    phylib_coord bRightHole = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH};

    newTable -> object[4] = phylib_new_hole(&tLeftHole);
    newTable -> object[5] = phylib_new_hole(&mLeftHole);
    newTable -> object[6] = phylib_new_hole(&bLeftHole);
    newTable -> object[7] = phylib_new_hole(&tRightHole);
    newTable -> object[8] = phylib_new_hole(&mRightHole);
    newTable -> object[9] = phylib_new_hole(&bRightHole);

    for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++){
        newTable -> object[i] = NULL;
    }
    return newTable;
}
    


//PART 2

//copies a phylib_object from the source pointer to the destination pointer, 
//handling memory allocation and checking for null pointers.
void phylib_copy_object( phylib_object **dest, phylib_object **src){
    if(src == NULL || *src == NULL){
        *dest = NULL;
        return;
    }
    *dest = (phylib_object*)malloc(sizeof(phylib_object));
    if(*dest == NULL){
        *dest = NULL;
        return;
    }
    if(*dest != NULL){
        memcpy(*dest, *src, sizeof(phylib_object));
    }
    
}

//Copies a given phylib table, allocating memory for a new table, 
//and duplicates its contents, including associated objects.
phylib_table *phylib_copy_table( phylib_table *table){
    if(table == NULL){
        return NULL;
    }
    phylib_table *copiedTable = (phylib_table*)malloc(sizeof(phylib_table));

    if(copiedTable == NULL){
        return NULL;
    }

    copiedTable -> time = table -> time;
    
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table -> object[i] != NULL){
            phylib_copy_object(&(copiedTable->object[i]), &(table -> object[i]));  
        }else{
            copiedTable -> object[i] = NULL;
        }
        
    }
 
    return copiedTable;
}

//Adds a phylib object to a phylib table, 
//inserting it into the first available slot.
void phylib_add_object(phylib_table *table, phylib_object *object){
    if(table == NULL || object == NULL){
        return;
    }
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table -> object[i] == NULL){
            table -> object[i] = object;
            break;
        }
    }
}

//Frees memory allocated for objects in a phylib_table and the table itself, 
//setting object pointers to NULL to avoid dangling references, if i dont do this
//it may cause unitialized errors.
void phylib_free_table(phylib_table *table){
    if(table == NULL){
        return;
    }
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table -> object[i] != NULL){
            free(table->object[i]);
            table -> object[i] = NULL;
        }
    }
    free(table);
    
}

//Computes the subtraction of two phylib_coord structures, 
//returning a new phylib_coord with the resulting coordinates.
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2){
    phylib_coord resultS;
    
    resultS.x = c1.x - c2.x;
    resultS.y = c1.y - c2.y;
    return resultS;
}

//Calculates and returns the Euclidean length of a 2D vector,
//represented by the input coordinates.
double phylib_length(phylib_coord c ){
    double sqSum = c.x * c.x + c.y * c.y;
    double resultL = sqrt(sqSum);
    return resultL;
}

//Computes and returns the dot product of two 2D vectors,
//represented by the input coordinates.
double phylib_dot_product(phylib_coord a, phylib_coord b){
    double resultD = (a.x * b.x) + (a.y * b.y);
    return resultD;
}

//calculates the distance between two physical objects, 
//represented by phylib_object pointers, considering different object types.
double phylib_distance(phylib_object *obj1, phylib_object *obj2){
    //If either object is NULL or the first object is not a rolling ball, the function returns -1.0. 
    if(obj1 == NULL || obj2 == NULL){
        return -1.0;
    }
    if(obj1 -> type != PHYLIB_ROLLING_BALL){
        return -1.0;
    }

    phylib_rolling_ball ball1 = obj1 -> obj.rolling_ball;
    phylib_coord ball1Center = ball1.pos;
    phylib_coord ball2Center;
    double distance;
    
    //For rolling balls and still balls, it computes the distance based on ball centers; 
    if(obj2 -> type == PHYLIB_ROLLING_BALL || obj2 -> type == PHYLIB_STILL_BALL){ //move PHYLIB_STILL_BALL here
        ball2Center = obj2 -> obj.rolling_ball.pos;
        distance = phylib_length(phylib_sub(ball1Center,ball2Center))- PHYLIB_BALL_DIAMETER;
        return distance;
    //for holes, horizontal and vertical cushions, it adjusts the distance based on specific object characteristics
    } else if (obj2 -> type == PHYLIB_HOLE){
        phylib_coord holeCenter = obj2 -> obj.hole.pos;
        distance = phylib_length((phylib_coord){ball1Center.x - holeCenter.x, ball1Center.y - holeCenter.y});
        return distance - PHYLIB_HOLE_RADIUS;
    } else if (obj2 -> type == PHYLIB_HCUSHION){
        double cushionY = obj2 -> obj.hcushion.y;
        distance = fabs(ball1Center.y - cushionY);
        return distance - PHYLIB_BALL_RADIUS;
    } else if (obj2 -> type == PHYLIB_VCUSHION){
        double cushionX = obj2 -> obj.vcushion.x;
        distance = fabs(ball1Center.x - cushionX);
        return distance - PHYLIB_BALL_RADIUS;
    //if the second object is none of the recognized types, it returns -1.0
    } else{
        return -1.0;
    }
    //distance = phylib_length((phylib_coord){ball1Center.x - ball2Center.x, ball1Center.y - ball2Center.y});
    return distance - PHYLIB_BALL_DIAMETER;

}

//PART 3

//updates the position and velocity of a rolling ball object over time based on its acceleration,
//given the new and old states, using physics calculations.
void phylib_roll(phylib_object *new, phylib_object *old, double time){
    if(new == NULL || old == NULL || new -> type != PHYLIB_ROLLING_BALL || old -> type != PHYLIB_ROLLING_BALL){
        return;
    }
    double timeSq = time * time;

    new -> obj.rolling_ball.pos.x = old -> obj.rolling_ball.pos.x + old -> obj.rolling_ball.vel.x * time + 0.5 * old -> obj.rolling_ball.acc.x * timeSq;
    new -> obj.rolling_ball.pos.y = old -> obj.rolling_ball.pos.y + old -> obj.rolling_ball.vel.y * time + 0.5 * old -> obj.rolling_ball.acc.y * timeSq;

    new -> obj.rolling_ball.vel.x = old -> obj.rolling_ball.vel.x + old -> obj.rolling_ball.acc.x * time;
    new -> obj.rolling_ball.vel.y = old -> obj.rolling_ball.vel.y + old -> obj.rolling_ball.acc.y * time;
    
    //if statements to handle cases where the velocity changes direction, 
    //setting velocity and acceleration components to zero accordingly.
    if((old -> obj.rolling_ball.vel.x * new -> obj.rolling_ball.vel.x) < 0){
        new -> obj.rolling_ball.vel.x = 0.0;
        new -> obj.rolling_ball.acc.x = 0.0;
    }

    if((old -> obj.rolling_ball.vel.y * new -> obj.rolling_ball.vel.y) < 0){
        new -> obj.rolling_ball.vel.y = 0.0;
        new -> obj.rolling_ball.acc.y = 0.0;
    }

    //(if both velocities change sign,
    //then both velocities and both accelerations must be set to zero
    if(((new -> obj.rolling_ball.vel.x) == 0) && ((new -> obj.rolling_ball.vel.y) == 0)){
        new -> obj.rolling_ball.acc.x = 0.0;
        new -> obj.rolling_ball.acc.y = 0.0;
        
    }
}

//takes a pointer to a phylib_object and checks if it represents a rolling ball;
//if not, or if the pointer is NULL, it returns 0
unsigned char phylib_stopped(phylib_object *object ){
    if(object == NULL || object -> type != PHYLIB_ROLLING_BALL){
        return 0;
    }
    phylib_rolling_ball *rollBall = &object -> obj.rolling_ball;
    //calculate length of vel (speed)
    double speed = phylib_length(rollBall -> vel);
    //Checks if ball stopped
    if(speed < PHYLIB_VEL_EPSILON){
        //If the rolling ball's speed is below a certain threshold (PHYLIB_VEL_EPSILON), 
        //it updates the object to a still ball, copies relevant attributes(number + pos),
        //and returns 1; otherwise, it returns 0.
        object -> type = PHYLIB_STILL_BALL;
        object -> obj.still_ball.number = object -> obj.rolling_ball.number;
        object -> obj.still_ball.pos = object -> obj.rolling_ball.pos;
        
        return 1;
    }
    return 0;
}

//takes two pointers to phylib_object objects and performs collision-related operations based on their types, 
//particularly handling bouncing behavior for a rolling ball object colliding with various other object types.
void phylib_bounce(phylib_object **a, phylib_object **b){
    if(a == NULL || b == NULL || *a == NULL || *b == NULL){
        return;
    }
    phylib_object *objA = *a;
    phylib_object *objB = *b;

    if(objA -> type != PHYLIB_ROLLING_BALL){
        return;
    }

    switch(objB -> type){
        case PHYLIB_HCUSHION:
            //Reflects the rolling ball's velocity and acceleration along the y-axis.
            objA -> obj.rolling_ball.vel.y = -objA -> obj.rolling_ball.vel.y;
            objA -> obj.rolling_ball.acc.y = -objA -> obj.rolling_ball.acc.y;
            break;
        case PHYLIB_VCUSHION:
            //Reflects the rolling ball's velocity and acceleration along the x-axis.
            objA -> obj.rolling_ball.vel.x = -objA -> obj.rolling_ball.vel.x;
            objA -> obj.rolling_ball.acc.x = -objA -> obj.rolling_ball.acc.x;
            break;
        case PHYLIB_HOLE:
            //Frees memory for object A and sets it to NULL.
            free(*a);
            *a = NULL;
            break;
        case PHYLIB_STILL_BALL: {
            // Converts object B to a rolling ball, copying relevant properties(number + pos + vel + acc)
            objB -> type = PHYLIB_ROLLING_BALL;
            objB -> obj.rolling_ball.number = objB -> obj.still_ball.number;
            objB -> obj.rolling_ball.pos = objB -> obj.still_ball.pos;
            objB -> obj.rolling_ball.vel = (phylib_coord){.x = 0, .y = 0};
            objB -> obj.rolling_ball.acc = (phylib_coord){.x = 0,.y = 0};
        }
        case PHYLIB_ROLLING_BALL:
            {
                //Computes and updates velocities and accelerations for two colliding rolling balls, 
                //considering their relative velocities and directions. Additionally, applies drag forces based on their speeds.

                //Calculates relative position r_ab and relative velocity v_rel, by using the phylib_sub function.
                phylib_coord r_ab = phylib_sub(objA -> obj.rolling_ball.pos, objB -> obj.rolling_ball.pos);
                phylib_coord v_rel = phylib_sub(objA -> obj.rolling_ball.vel, objB -> obj.rolling_ball.vel);

                //Finds collision normal vector n.
                phylib_coord n = {r_ab.x / phylib_length(r_ab), r_ab.y/ phylib_length(r_ab)};
                double v_rel_n = phylib_dot_product(v_rel, n);

                //Reflects velocities across n to simulate bounce.
                objA -> obj.rolling_ball.vel.x -= v_rel_n * n.x;
                objA -> obj.rolling_ball.vel.y -= v_rel_n * n.y;
                objB -> obj.rolling_ball.vel.x += v_rel_n * n.x;
                objB -> obj.rolling_ball.vel.y += v_rel_n * n.y;

                //Applies drag forces based on velocities for energy loss
                double speedA = phylib_length(objA -> obj.rolling_ball.vel);
                double speedB = phylib_length(objB -> obj.rolling_ball.vel);

                //Updates accelerations with drag forces if speeds exceed PHYLIB_VEL_EPSILON
                if(speedA > PHYLIB_VEL_EPSILON){
                    objA -> obj.rolling_ball.acc.x = (-objA -> obj.rolling_ball.vel.x / speedA) * PHYLIB_DRAG; //multiply by -1
                    objA -> obj.rolling_ball.acc.y = (-objA -> obj.rolling_ball.vel.y / speedA) * PHYLIB_DRAG;
                }
                if (speedB > PHYLIB_VEL_EPSILON){
                    objB -> obj.rolling_ball.acc.x = (-objB -> obj.rolling_ball.vel.x / speedB) *PHYLIB_DRAG;
                    objB -> obj.rolling_ball.acc.y = (-objB -> obj.rolling_ball.vel.y / speedB) * PHYLIB_DRAG;
                }
            }
            break;
        default:
            break;
    }
}

//counts the number of objects in a given phylib_table that are of type PHYLIB_ROLLING_BALL and returns the count,
//or 0 if the input table is NULL
unsigned char phylib_rolling(phylib_table *t){
    if (t == NULL){
        return 0;
    }
    unsigned char rollCount = 0;
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(t -> object[i] != NULL && t -> object[i] -> type == PHYLIB_ROLLING_BALL){
            rollCount++;
        }
    }
    return rollCount;
}

//return a segment of a pool shot
phylib_table *phylib_segment(phylib_table *table){
    if (table == NULL){
        return NULL;
    }

    int rBallE = 0;
    //The first loop iterates through each object in the input table,
    //setting a flag rBallE if a rolling ball object is found.
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL && table->object[i]->type == PHYLIB_ROLLING_BALL) {
            rBallE = 1;
        }
    }
    if (rBallE == 0) {
        return NULL;
    }
    
    phylib_table *resultT = phylib_copy_table(table);

    double time = PHYLIB_SIM_RATE;
    //The second loop, running a physics simulation, iterates through each rolling ball object in a copy of the input table (resultT),
    //updating their positions based on rolling motion and handling collisions with other objects
    while(time <= PHYLIB_MAX_TIME){
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if(resultT -> object[i] != NULL && resultT -> object[i] -> type == PHYLIB_ROLLING_BALL){
                phylib_roll(resultT -> object[i], table -> object[i], time);
            }
        }

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if(resultT -> object[i] != NULL && resultT -> object[i] -> type == PHYLIB_ROLLING_BALL){
                //nested loop checks for collisions between the current rolling ball object and other objects. If a collision occurs, 
                //it updates the resultT table and returns it; otherwise, 
                //it checks if the rolling ball object has stopped, in which case it returns the resultT table.
                for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
                    if(i != j && resultT -> object[j] != NULL){ 
                        if(phylib_distance(resultT -> object[i], resultT -> object[j]) < 0.0){
                            phylib_bounce(&resultT -> object[i], &resultT -> object[j]);
                            resultT -> time = table -> time + time;
                            return resultT;
                            
                        }
                    }
                }
                if(phylib_stopped(resultT -> object[i])){
                    resultT -> time = table -> time + time;
                    return resultT;
                }
                
            }
            
        }
        time += PHYLIB_SIM_RATE;
    }
    return resultT;
}

char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x );
            break;
        }
    return string;
}
