# Translated into Python by M.E.Farmer 2013.
#
# This an adaptation of Robert Penner's easing/tweening algorithms.
# http://www.robertpenner.com/easing/
#
# I couldn't find a good tweening library for a 
# project I was working on so I found the original 
# tweening alogorithms and modified them for Python.
# Because they are stateless I have included
# helper functions that make them easy to use.
# They are implemented as generators so you can 
# just setup and then call their .next() method
# or use them in loops.
#
# Some of these tweens were created by me using the awesome demo at
# http://www.timotheegroleau.com/Flash/experiments/easing_function_generator.htm
# To create your own custom tween play with the demo and use the last line of the formula
# copy the InchWorm tween and replace the return line with the one the formula gives you.
# You can also use the customTween function just pass in the formula as a string
# and it will return a tweening function for you.
# You just need what is between the return and the semicolon.
# 
# Where would you use these?
#    calculate position changes with ease..ing ;)
#    Robotics, game object movements, webpage scrolling, etc.
#    LED or object color morphs are a snap
#    "breathing" LED type effects
#     etc..
# Example:
# >>> from tween import *
# >>> t = tween(easeLinear, 1,255,20,True,False)
# >>> for x in t:
# >>>     print x,
# >>> 1 14 28 41 54 68 81 95 108 121 135 148 161 175 188 202 215 228 242 255
#
# >>> color1 = (123,234,12)
# >>> color2 = (255,12,189)
# >>> color_gen = colorTween(easeInQuad,color1,color2,10,
#                            include_begin=True,endless=False)
# >>> for rgb in color_gen:
# >>>     print rgb
# (123, 234, 12)
# (125, 231, 14)
# (130, 223, 21)
# (138, 209, 32)
# (149, 190, 47)
# (164, 165, 67)
# (182, 135, 91)
# (203, 100, 119)
# (227, 59, 152)
# (255, 12, 189)
# >>> b = cycleTween(easeInQuad,
#                    easeOutQuad,
#                    1,255,10,
#                    endless=False)
# >>> for x in b:
#	print x,
#	
# 1 4 11 24 42 65 92 125 164 207 255 207 164 125 92 65 42 24 11 4 1
import math

def tween(tweenFunc,begin,end,steps,
          include_begin=False,endless=False):
    '''Basic tween wrapper to generate the transition between values using easing.
       Use by itself or use it to create composite easing.
       Example:
            Create a function that takes an RGB tuple and
            tween each color channel using a different easing function.

            Create a function that tweens between X,Y pairs using
            a different easing function on each coordinate to give
            arced type trajectories.
       endless = repeat last value
       Functon yields Integers.
    '''
    change = end-begin
    tick=0.
    if include_begin:
        steps-=1
        yield begin
    while tick < steps:
        tick+=1
        out = int(round(tweenFunc(tick,begin,change,steps)))
        yield out
    while endless:
        yield out
        
def xyTween(tweenFunc,begin_xy,end_xy,steps,
            include_begin=False,endless=False):
    '''Transition between XY tuples or list using easing.
       endless = repeat last value forever once last step is reached 
       Function yields X,Y tuples
    '''
    changex = end_xy[0]-begin_xy[0]
    changey = end_xy[1]-begin_xy[1]
    tick=0.
    if include_begin:
        steps-=1
        yield begin_xy
    while tick < steps:
        tick+=1
        x = int(round(tweenFunc(tick,begin_xy[0],changex,steps)))
        y = int(round(tweenFunc(tick,begin_xy[1],changey,steps)))
        yield (x,y)
    while endless:
        yield (x,y)

def colorTween(tweenFunc,begin_rgb,end_rgb,steps,
               include_begin=False,endless=False):
    '''Transition between RGB tuples or list with easing.
       Because functions that are 'elastic' can bounce above
       or below the min and max ranges (0,255) we cutoff at 255.
       endless = repeat last value forever once last step is reached 
       Function will yield R,G,B tuples
    '''
    changer = end_rgb[0]-begin_rgb[0]
    changeg = end_rgb[1]-begin_rgb[1]
    changeb = end_rgb[2]-begin_rgb[2]
    tick=0.
    if include_begin:
        steps-=1
        r,g,b = begin_rgb
        
        yield ([r,255][r/255],[g,255][g/255],[b,255][b/255])
    while tick < steps:
        tick+=1
        r = int(round(tweenFunc(tick,begin_rgb[0],changer,steps)))
        g = int(round(tweenFunc(tick,begin_rgb[1],changeg,steps)))
        b = int(round(tweenFunc(tick,begin_rgb[2],changeb,steps)))
        yield ([r,255][r/255],[g,255][g/255],[b,255][b/255])
    while endless:
        yield ([r,255][r/255],[g,255][g/255],[b,255][b/255])

def cycleTween(tweenFunc_one,tweenFunc_two,begin,end,steps,endless=False):
    '''Ease forward and backward through begin and end points
       Easing functions can be the same or different to
       give varied effects.
       endless = True is a repeating cycle
       endless = False is a single cycle
       Function yields Integers
    '''
    cycle = True
    # add the first value so it will start right
    yield begin
    while cycle:
        if not endless:
            cycle = False
        forward = tween(tweenFunc_one,
                        begin,end,steps,
                        False,False)
        for step in forward:
            yield step
        backward = tween(tweenFunc_two,
                         end,begin,steps,
                         False,False)
        for step in backward:
            yield step

def floatTween(tweenFunc,begin,end,steps,
          include_begin=False,endless=False):
    '''Basic tween wrapper to generate the transition between
       floating point values using easing.
       Usefull when a range of floats is needed.
       endless = repeat last value forever once last step is reached 
       Functon yields floats.
    '''
    change = float(end-begin)
    tick=0.
    if include_begin:
        steps-=1
        yield begin
    while tick < steps:
        tick+=1
        out = tweenFunc(tick,begin,change,steps)
        yield out
    while endless:
        yield out

def easeLinear(t,b,c,d):
    v = t/d
    return c*v+b    

def easeInQuad(t,b,c,d):
    v = t/d
    return c*v*v+b

def easeOutQuad(t,b,c,d):
    v = t/d
    return -c*v*(v-2)+b
    
def easeInOutQuad(t,b,c,d):
    v = t/(d/2)
    if v < 1:
        return c/2*v*v+b
    else:
        v-=1
        return -c/2*((v)*(v-2)-1)+b
        
def easeInCubic(t,b,c,d):
    v = t/d
    return c*pow(v,3)+b
    
def easeOutCubic(t,b,c,d):
    v = t/d
    return c*(pow(v-1,3)+1)+b
    
def easeInOutCubic(t,b,c,d):
    v = t/(d/2)
    if v < 1:
        return c/2*pow(v,3)+b
    else:
        return c/2*(pow(v-2,3)+2)+b
        
def easeInQuartic(t,b,c,d):
    v = t/d
    return c*pow(v,4)+b
    
def easeOutQuartic(t,b,c,d):
    v = t/d
    return -c*(pow(v-1,4)-1)+b
    
def easeInOutQuartic(t,b,c,d):
    v = t/(d/2)
    if v < 1:
        return c/2*pow(v,4)+b
    else:
        return -c/2*(pow(v-2,4)-2)+b
        
def easeInQuintic(t,b,c,d):
    v = t/d
    return c*pow(v,5)+b
    
def easeOutQuintic(t,b,c,d):
    v = t/d
    return c*(pow(v-1,5)+1)+b
    
def easeInOutQuintic(t,b,c,d):
    v = t/(d/2)
    if v < 1:
        return c/2*pow(v,5)+b
    else:
        return c/2*(pow(v-2,5)+2)+b
        
def easeInSine(t,b,c,d):
    v = t/d
    return c*(1-math.cos(v*(math.pi/2)))+b
    
def easeOutSine(t,b,c,d):
    v = t/d
    return c*math.sin(v*(math.pi/2))+b
    
def easeInOutSine(t,b,c,d):
    v = t/d
    return c/2*(1-math.cos(math.pi*v))+b
    
def easeInExpo(t,b,c,d):
    v = t/d
    return c*pow(2,10*(v-1))+b
    
def easeOutExpo(t,b,c,d):
    v = t/d
    return c*(-pow(2,-10*v)+1)+b
    
def easeInOutExpo(t,b,c,d):
    v = t/(d/2)
    if v < 1:
        return c/2*pow(2,10*(v-1))+b
    else:
        v-=1
        return c/2*(-pow(2,-10*v)+2)+b

def easeInCirc(t,b,c,d):
    v = t/d
    return c*(1-math.sqrt(1-v*v))+b

def easeOutCirc(t,b,c,d):
    v = t/d-1
    return c*math.sqrt(1-(v*v))+b

def easeInOutCirc(t,b,c,d):
    v = t/(d/2)
    if v < 1:
        return c/2*(1-math.sqrt(1-(v*v)))+b
    else:
        v-=2
        return c/2*(math.sqrt(1-v*v)+1)+b

def easeOutElasticBig(t,b,c,d):
    t/=d
    ts=t*t
    tc=ts*t
    return b+c*(56*tc*ts + -175*ts*ts + 200*tc + -100*ts + 20*t)

def easeInElasticBig(t,b,c,d):
    t/=d
    ts=t*t
    tc=ts*t
    return b+c*(56*tc*ts + -105*ts*ts + 60*tc + -10*ts)

def easeOutElasticSmall(t,b,c,d):
    t/=d
    ts=t*t
    tc=ts*t
    return b+c*(33*tc*ts + -106*ts*ts + 126*tc + -67*ts + 15*t)

def easeInElasticSmall(t,b,c,d):
    t/=d
    ts=t*t
    tc=ts*t
    return b+c*(33*tc*ts + -59*ts*ts + 32*tc + -5*ts)

def easeLoop(t,b,c,d):
    t/=d
    ts=t*t
    tc=ts*t
    return b+c*(-11.945*tc*ts + 45.585*ts*ts + -42.685*tc + 5.795*ts + 4.25*t)

def easeInchWorm(t,b,c,d):
    t/=d
    ts=t*t
    tc=ts*t
    return b+c*(44.2925*tc*ts + -114.88*ts*ts + 105.18*tc + -39.99*ts + 6.3975*t)

def customTween(formula_string):
    '''function for creating your own custom tweens.
       Call this function with your formula string and it will return
       a tweening function for you to use.
       Go to this website:
           http://www.timotheegroleau.com/Flash/experiments/easing_function_generator.htm
       and tweak the control points and take
       the formula and pass it in as a string.
       You need everything between the return and the semicolon.
       
       This is a bounce tween for example:
          "b+c*(26.65*tc*ts + -91.5925*ts*ts + 115.285*tc + -62.89*ts + 13.5475*t"
    '''
    def custom(t,b,c,d):
	t/=d
        ts=t*t
        tc=ts*t
        return eval(formula_string)
    return custom
