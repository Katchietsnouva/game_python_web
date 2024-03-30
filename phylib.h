#ifndef _phylib_h
#define _phylib_h
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>   

#define PHYLIB_BALL_RADIUS      (28.5) // mm
#define PHYLIB_BALL_DIAMETER    (2*PHYLIB_BALL_RADIUS)
#define PHYLIB_HOLE_RADIUS      (2*PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH     (2700.0) // mm
#define PHYLIB_TABLE_WIDTH      (PHYLIB_TABLE_LENGTH/2.0) // mm
#define PHYLIB_SIM_RATE         (0.0001) // s
#define PHYLIB_VEL_EPSILON      (0.01) // mm/s
#define PHYLIB_DRAG             (150.0) // mm/s^2
#define PHYLIB_MAX_TIME         (600) // s
#define PHYLIB_MAX_OBJECTS      (26)

//grouped constants
typedef enum {
    PHYLIB_STILL_BALL = 0,
    PHYLIB_ROLLING_BALL = 1,
    PHYLIB_HOLE = 2,
    PHYLIB_HCUSHION = 3,
    PHYLIB_VCUSHION = 4,
} phylib_obj;

//class representing a vector in 2 dimension
typedef struct {
    double x;
    double y;
} phylib_coord;

//child classes representing objects on the table
//ball not in motion
typedef struct {
    unsigned char number;
    phylib_coord pos;
} phylib_still_ball;

//balls in motion
typedef struct {
    unsigned char number;
    phylib_coord pos;
    phylib_coord vel;
    phylib_coord acc;
} phylib_rolling_ball;

//one of the 6 holes on the table
typedef struct {
    phylib_coord pos;
} phylib_hole;

//horizontal cushion; either of the 2 short sides of the table
typedef struct {
    double y;
} phylib_hcushion;

//vertical cushion; either of the 2 long sides of the table
typedef struct {
    double x;
} phylib_vcushion;

//Parent class of objects on the table
//union that can store any of the above classes/structure in the same place
typedef union {
    phylib_still_ball still_ball;
    phylib_rolling_ball rolling_ball;
    phylib_hole hole;
    phylib_hcushion hcushion;
    phylib_vcushion vcushion;
} phylib_untyped;

//identifies what the class of the object is
typedef struct {
    phylib_obj type;
    phylib_untyped obj;
} phylib_object;

//the table
typedef struct {
    double time;
    phylib_object *object[PHYLIB_MAX_OBJECTS];
} phylib_table;

//function prototypes
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos);
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos,
phylib_coord *vel, phylib_coord *acc);
phylib_object *phylib_new_hole(phylib_coord *pos);
phylib_object *phylib_new_hcushion(double y);
phylib_object *phylib_new_vcushion(double x);
phylib_table *phylib_new_table(void);

void phylib_copy_object(phylib_object **dest, phylib_object **src);
phylib_table *phylib_copy_table(phylib_table *table);
void phylib_add_object(phylib_table *table, phylib_object *object);
void phylib_free_table(phylib_table *table);
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2);
double phylib_length(phylib_coord c);
double phylib_dot_product(phylib_coord a, phylib_coord b);
double phylib_distance(phylib_object *obj1, phylib_object *obj2);

void phylib_roll(phylib_object *new, phylib_object *old, double time);
unsigned char phylib_stopped(phylib_object *object );
void phylib_bounce(phylib_object **a, phylib_object **b);
unsigned char phylib_rolling(phylib_table *t );
phylib_table *phylib_segment(phylib_table *table);

//New function
char *phylib_object_string( phylib_object *object);

#endif
