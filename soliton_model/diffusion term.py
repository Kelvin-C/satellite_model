import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as an
import matplotlib
import math
  
def initialwave(alpha, x0):
    """
    Creates a soliton wave with the equation equal to the solution of KdeV equation.
    """
    return 12*alpha**2*(1/np.cosh(alpha*(x-x0)))**2
    
def initiatecos(width, x0, amplitude=1):
    """
    Generates a cosine wave with only the central peak and (all values below 0) = 0.
    Width defines the width between the 0 points of the cosine wave.
    """
    x0 = x0[0]
    y = amplitude * np.cos((x-x0)*np.pi/width)
    for i in range(xsize):
        if x[i] < (x0-width/2.) or x[i] > (x0+width/2.):
            y[i] = 0
    return y

def initiategaussian(sd, x0, height=1):
    """
    Generates a gaussian, where sd = standard deviation and x0 = (x value at peak).
    """
    y = height*np.exp(-x**2/(2*sd**2))
    return y
    
plotmass = 'y'
plotamplitude = 'y'
plotvelocity = 'n'
animation_speed = 10
h = 0.5
dt = 0.01
xmin = -10
xmax = 50
tmax = 2.5
x = np.arange(xmin,xmax, h)
t = np.arange(0,tmax, dt)
xsize = len(x)
tsize = len(t)
u = np.zeros((tsize, xsize))
u0 = np.zeros(xsize)

x0 = [0]
width = 20
#u0 = initiatecos(width, x0, 1)  #Width here is the distance between the roots of the cosine wave.
#u0 = initiategaussian(width,x0) #Width here is SD. Breaking works with SD = 5. NOTE:

alpha = [4.2]
for i in range(len(alpha)): #Can generate multiple solitons
    u0 += initialwave(alpha[i], x0[i])

u[0] = u0

def integrate(u, j, h):
    """
    Numerical integration with Trapezium method.
    """
    y = u[j]
    return (h/2.)*((y[0]+y[-1]) + 2*sum(y[1:-1]))
    
def makevelocity(velocity, jstore, ignore = [0]):    
    """
    An algorithm to calculate velocity of the largest peak over time.
    This algorithm ignores the boundary because passing through the boundary will give a negative velocity.
    The small number of time steps per calculation of velocity was used (explained in the report).
    """
    for j in range(1, tsize-jstore):
        if j not in ignore:
            temp = (peak_position[jstore+j]-peak_position[jstore])/(t[jstore+j]-t[jstore])
            if temp != 0:
                if temp < 0:
                    if len(velocity) == 0:
                        ignore += [j]
                        return velocity, jstore, ignore
                    else:
                        velocity = np.append(velocity, velocity[-1])
                        jstore = jstore + j
                        return velocity, jstore, [0]
                else:
                    velocity = np.append(velocity, temp)
                    jstore = jstore + j
                    return velocity, jstore, [0]
    return velocity, tsize, [0]
            
def init():
    """
    Needed for animation. Resets all plots.
    """
    uanim.set_data([],[])
    return uanim,

def animate(j):
    """
    Animates the plots.
    """
    uanim.set_data(x, u[j%tsize])
    return uanim,
    
def initmass():
    """
    Needed for animation. Resets all plots.
    """
    uanim.set_data([],[])
    massanim.set_data([],[])
    return uanim, massanim
    
def animatemass(j):
    """
    Animates the plots.
    """
    uanim.set_data(x, u[j%tsize])
    massanim.set_data(t[:j%tsize], mass[:j%tsize])
    return uanim, massanim
    
def initamp():
    """
    Needed for animation. Resets all plots.
    """
    uanim.set_data([],[])
    massanim.set_data([],[])
    ampanim.set_data([],[])
    txt1.set_text(" ")
    return uanim, massanim, ampanim, txt1
    
def animateamp(j):
    """
    Animates the plots.
    """
    uanim.set_data(x, u[j%tsize])
    massanim.set_data(t[:j%tsize], mass[:j%tsize])
    ampanim.set_data(t[:j], amplitudes[:j])
    txt1.set_text("j = %s" %j)
    if j > stop1:
        wave1.set_data(x, u[stop1])
    if j > stop2:
        wave2.set_data(x, u[stop2])
    if j > stop3:
        wave3.set_data(x, u[stop3])
        uanim.set_data(x, u[stop3])
        massanim.set_data(t[:stop3], mass[:stop3])
        ampanim.set_data(t[:stop3], amplitudes[:stop3])
        txt1.set_text("j = %s" %stop3)
        #plt.savefig('pictures')
    return uanim, massanim, ampanim, wave1, wave2, wave3, txt1
    
def initvelocity():
    """
    Needed for animation. Resets all plots.
    """
    uanim.set_data([],[])
    massanim.set_data([],[])
    vanim.set_data([],[])
    ampanim.set_data([],[])
    return uanim, massanim, vanim, ampanim
    
def animatevelocity(j):
    """
    Animates the plots. The animation has 3 stopping points which show the movement of the soliton.
    """
    i = j/v_intervals
    uanim.set_data(x, u[j])
    massanim.set_data(t[:j], mass[:j])
    vanim.set_data(v_times[:i], velocity[:i])
    ampanim.set_data(t[:j], amplitudes[:j])
    return uanim, massanim, vanim, ampanim
    
def RK4(y, j, h, dt, f):
    """
    Runge-Kutta 4 method
    """
    k1 = dt*f(y, j, h,)
    k2 = dt*f(y, j, h, 0.5*k1)
    k3 = dt*f(y, j, h, 0.5*k2)
    k4 = dt*f(y, j, h, k3)
    return (y[j] + (1./6.)*(k1 + 2*k2 + 2*k3 + k4))

    
def func1(y, j, h, add_u = 0):
    """
    Used to calculate k1, k2,.. etc for Runge Kutta 4. All terms from the KdeV are kept.
    """
    y_temp = y[j] + add_u
    N = xsize
    k = np.zeros(xsize)
    for i in range(xsize):
        k[i] = -(1/4.)*(1./h)*(y_temp[(i+1)%N]**2-y_temp[(i-1)%N]**2) - 0.5/(h**3)*(y_temp[(i+2)%N]-2*y_temp[(i+1)%N]+2*y_temp[(i-1)%N]-y_temp[(i-2)%N])
    return k
    
def func2(y, j, h, add_u = 0):
    """
    Used to calculate k1, k2,.. etc for Runge Kutta 4. 3rd term of KdeV equation removed.
    Used to show shock waves.
    """
    y_temp = y[j] + add_u
    N = xsize
    k = np.zeros(xsize)
    for i in range(xsize):
        k[i] = -(1/4.)*(1./h)*(y_temp[(i+1)%N]**2-y_temp[(i-1)%N]**2)
    return k
    
def func3(y, j, h, add_u = 0):
    """
    Used to calculate k1, k2,.. etc for Runge Kutta 4. 3rd term of KdeV equation removed
    and is replaced by diffusion term (damping). Prevents instability.
    """
    y_temp = y[j] + add_u
    N = xsize
    k = np.zeros(xsize)
    for i in range(xsize):
        k[i] = -(1/4.)*(1./h)*(y_temp[(i+1)%N]**2-y_temp[(i-1)%N]**2) + (1/2.)*(1./h**2)*(y_temp[(i+1)%N]-2*y_temp[i%N]+y_temp[(i-1)%N])
    return k

for j in range(tsize-1): #Calculates u at all time steps.
    u[j+1]= RK4(u, j, h, dt, func3)

if plotmass == 'y':
    mass = np.zeros(tsize)
    for j in range(tsize):
        mass[j] = integrate(u, j, h)

#This set of code is used to produce velocity and amplitude plots.
#Amplitude over time is plotted by finding peak value of wave at all times.
#Velocity is found by finding the rate of change of the peak's position over time.
peak_position = np.zeros(tsize)
amplitudes = np.zeros(tsize)
stable = True
for j in range(tsize):
    if math.isnan(max(u[j])) == True:
        stable = False
        peak_position[j] = 0
        amplitudes[j] = 0
    else:
        peak_position[j] = x[np.where(u[j]==max(u[j]))[0][0]]
        amplitudes[j] = max(u[j])
        
if stable == False:
    print "Solution is unstable. The height had grown too large."     
    plotvelocity = 'n'
    
if plotvelocity == 'y':
    velocity = np.array([])
    jstore = 0
    ignore = [0]
    while jstore < tsize:
        velocity, jstore, ignore = makevelocity(velocity, jstore, ignore)
    velocity[0] = velocity[1]
    v_times = np.linspace(0, tmax, len(velocity))
    v_intervals = tsize/len(velocity)

#Plot animation of soliton.
fig = plt.figure(figsize=(20,6))
matplotlib.rcParams.update({'font.size': 14})
subplot1 = fig.add_subplot(1,4,1)
uanim, = plt.plot([],[], 'k-', linewidth=3)
stop1 = 75 #number of frames until stop first time.
stop2 = 20000 #number of frames until stop 2nd time.
stop3 = 200 #number of frames for final stop and freeze.
wave1, = plt.plot([],[], 'g-', linewidth = 3)
wave2, = plt.plot([],[], 'r-', linewidth = 2)
wave3, = plt.plot([],[], 'm-', linewidth = 1)
plt.axis([xmin, xmax, -0.1, 2*12*max(alpha)**2])
#plt.axis([xmin, xmax, -0.1, 5])
plt.plot(x,u[0], 'b-', linewidth=3)
plt.title('Visualisation')
plt.xlabel('x', fontsize = 20)
plt.ylabel('u', fontsize = 25)


#Plot the area underneath the curve of soliton (i.e. mass)
if plotmass == 'y':
    subplot2 = fig.add_subplot(1,4,2)
    plt.plot(t, mass, 'b--')
    massanim, = plt.plot([],[], 'b-')
    plt.title('Area under curve')
    plt.xlabel('t', fontsize = 20)
    plt.ylabel('Area', fontsize = 20)

#Plot the velocity over time.
if plotvelocity == 'y':
    subplot2 = fig.add_subplot(1,4,4)
    plt.plot(v_times, velocity, 'r:')
    vanim, = plt.plot([],[], 'r-')
    #plt.axis([min(t), max(t), 3.7, 4.1])
    plt.title('Velocity of Soliton')
    plt.xlabel('t', fontsize = 20)
    plt.ylabel('Velocity', fontsize = 20)

#Plot the amplitude of largest soliton over time.
if plotamplitude == 'y':
    subplot2 = fig.add_subplot(1,4,3)
    plt.plot(t, amplitudes, 'g:')
    ampanim, = plt.plot([],[], 'g-')
    plt.title('Height of Soliton')
    plt.xlabel('t', fontsize = 20)
    plt.ylabel('Height', fontsize = 20)

plt.tight_layout() #Ensures all plots and animations is as big as possible for clarity
 
#Text is used to find the frame to stop the animation.
text1 = fig.add_subplot(1,3,3)
txt1 = text1.text(0.5,0.5," ")
plt.axis("off")
    
if plotmass == 'y' and plotvelocity != 'y' and plotamplitude != 'y':
    anim=an.FuncAnimation(fig, animatemass, init_func=initmass, frames=tsize, interval=animation_speed, blit=True)
elif plotmass == 'y' and plotvelocity != 'y' and plotamplitude == 'y':
    anim=an.FuncAnimation(fig, animateamp, init_func=initamp, frames=tsize, interval=animation_speed, blit=True)
elif plotmass == 'y' and plotvelocity == 'y' and plotamplitude == 'y':
    anim=an.FuncAnimation(fig, animatevelocity, init_func=initvelocity, frames=tsize, interval=animation_speed, blit=True)
else:
    anim=an.FuncAnimation(fig, animate, init_func=init, frames=tsize, interval=animation_speed, blit=True)

#Can save animation if wanted. Uses ffmpeg for the library of codecs.
#writer = an.writers['ffmpeg'](fps=30)
#dpi=300
#anim.save('wave.mp4',writer=writer,dpi=dpi)

plt.show()