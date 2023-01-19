import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge
import math
import random

#plt.gcf().set_size_inches(8,4) # largeur , hauteur 

#rect((-2, -2),12, 4)
#disk((0,0), 2, color="black")
#line((0,0), (8, 0), color="red")
#dot((4,0), color="blue")

def resize(w,h):
    plt.gcf().set_size_inches(w,h) # largeur , hauteur
    
def disk(center, r, **kwargs):
    circ=plt.Circle(center, r, lw=0, **kwargs)
    plt.gca().add_patch(circ)

def line(A, B, **kwargs):
    plt.plot([A[0], B[0]],[A[1], B[1]], **kwargs)

def dot(A, **kwargs):
    plt.plot(*A, marker='+',**kwargs)

def rect(xy, w, h, **kwargs):
    my_rect = Rectangle(xy, w, h,**kwargs)
    plt.gca().add_patch(my_rect)

def colors():
    colors = ["orangered","sienna","brown","sienna","orangered","orangered","orangered","ivdarkkhaki","darkseagreen","royalblue","navy","royalblue"] 
    bgcolors = ["tomato","salmon","coral","lightcoral","linen","bisque","blanchedalmond","ivory","honeydew","seashell","peachpuff","lightsteelblue"]
    i = random.randint(0,len(colors)-1)
    return colors[i], bgcolors[i]

def pizzas(n,d):# n = numerateur , d = denominateur
    theta = 360//d
    loop = 1 + n//d
    resize(4*loop,4)
    i=0
    color , bgcolor = colors()
    while i < n :
        l=i//d
        x , y =math.radians(i*theta), math.radians(i*theta)
        wedge = Wedge( (5*l ,0) , 2 , i*theta , (i+1)*theta , color=bgcolor)
        plt.gca().add_patch(wedge)
        B=(5*l + 2*math.cos(x), 2*math.sin(y))
        line((5*l,0), B , color=color)
        i+=1
    x , y =math.radians(i*theta), math.radians(i*theta)
    B=(5*l + 2*math.cos( x ), 2*math.sin( y )) 
    line((5*l,0), B , color=color)

def chocolate(n,d):
    
    loop = 1 + n//d
    mini = min(4*loop,8)
    resize(mini,4)
    i,k=0,0
    color , bgcolor = colors()
        
    while i < n :
        y = i//d
        j = i%d
        rect( (2*j, y) , 2 , 1 , bgcolor)
        i+=1
    while k < n :
        y = k//d
        j = k%d
        line((2*j,y), (2*(j+1),y) , color=color)
        line((2*j,y+1), (2*(j+1),y+1) , color=color)
        line((2*j,y), (2*j,y+1) , color=color)
        line((2*j+2,y), (2*j+2,y+1) , color=color)
        k+=1

def pythagore(): # 0 à plat , 1 à l'envers , 2 Oblique  , 3 Oblique
    color , bgcolor = colors()
    p = random.randint(0,4)
    if p == 0 :
        line((-5,0), (5,0) , color=color)
        line((-5,0), (-3,4) , color=color)
        line((5,0), (-3,4) , color=color)
        line((-3.22,3.56), (-2.77,3.34) , color=color)
        line((-2.55,3.78), (-2.77,3.34) , color=color)
    elif p == 1 :
        line((7,0), (0,0) , color=color)
        line((0,0), (0,4) , color=color)
        line((7,0), (0,4) , color=color)
        line((0,0.4), (0.4,0.4) , color=color)
        line((0.4,0), (0.4,0.4) , color=color)
    elif p == 2 :
        line((3,-1.5), (0,0) , color=color)
        line((0,0), (1,2) , color=color)
        line((3,-1.5), (1,2) , color=color)
        line((0.14,-0.07), (0.21,0.07) , color=color)
        line((0.07,0.14), (0.21,0.07) , color=color)
    elif p == 3 :
        line((1,5), (8,5) , color=color)
        line((1,5), (8,1) , color=color)
        line((8,5), (8,1) , color=color)
        line((7.6,4.6), (7.6,5) , color=color)
        line((7.6,4.6), (8,4.6) , color=color)
    else :
        line((1,3), (2,1) , color=color)
        line((1,3), (6,3) , color=color)
        line((2,1), (6,3) , color=color)
        line((2.14,1.07), (2.07,1.22) , color=color)
        line((1.93,1.14),  (2.07,1.22) , color=color)