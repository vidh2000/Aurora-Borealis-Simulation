# Import the dependencies
from vpython import *
#from scattering import scatter
from generate_curve import generate_curve
from vector import *
from random import uniform
from particle import Particle
from noise import pnoise1
import matplotlib.pyplot as plt
import time
import povexport
from noise import pnoise2

total_time = 0
time_making_sheet = 0
time_propagating = 0
time_export = 0
total_time = clock() - total_time

# Make sure that 1 is turned into 0001 to put the frames in order
def format_frame(frame):
    return "0" * (4 - len(str(frame))) + str(frame)

# Clear the screen after a frame of animation
def clear_screen():
    for obj in scene.objects:
        obj.visible = False
        del obj

# Record? True / False
record = False
for i in range(2):
    # Set the fps
    fps = 30

    # Define the magnetic field. CHANGE WITH DATA
    B = lambda h: Vector(0, 0, 0) - Khat

    # Create a variable to keep track of the frame number
    frame = 16

    # Create the seeds for the perlin noise
    seedx = 577.3 #uniform(0, 1000)
    seedy = 476.19072 + 16 / 175 + i* 100
    seed1 = 887.34
    seed2 = 163.44  + 16 * 0.02 + i* 100 #uniform(0, 1000)

    # Choose the starting and end points of the aurora
    Pi = Vector(-400, -200 + i * 400)#
    Pf = Vector(2000, -200 + i* 400)#

    # Choose the number of points to simulate per period
    n = 2000

    # Choose the number of internal layers
    b = 1

    # Choose the initial angle for the first wave
    phi_i = 0

    # Choose the initial angle for the final wave
    phi_f = 3 * PI / 180                             #0.35 PI

    # Choose the width of the aurora
    w = 1 #random.uniform(9,10)          #width  1- 10

    # Choose the wavelength of the wave
    wl = 800#random.uniform(20,22 ) * 2 * w      #wavelength  5.2 - 31.4 * 2 * w


    N_particles = n * 800 / wl
    print(f"{N_particles * 360 * b / 10**6: .2f} million particles created.")

    # Initial height variations
    ds = 5 / n

    # Calculate the value of P
    P = np.array([])
    heights = np.array([])

    print("Let's begin")
    time_making_sheet = clock() - time_making_sheet

    for i in range(1, b + 1):
        print(f"Creating layer {i}...")
        P_layer_i = generate_curve(Pi, Pf, n, b, i, phi_i, phi_f, w, wl, B, seedx, seedy)
        for j in range(len(P_layer_i)):
            #Changes initial height
            height = (240 + 20* pnoise2(seed1 + j * ds, seed2)) - (240 + 20* pnoise2(seed1 + j * ds, seed2) - 100) * (0.5* np.sin(1e3*j/n) + 0.5)
            #if height > 285:
                #print(height)
            P = np.append(P, Vector(P_layer_i[j, 0], P_layer_i[j, 1], height))  #300
            heights = np.append(heights, height)

    time_making_sheet = clock() - time_making_sheet
    print("Done creating initial positions.")
    # DEBUGGING ONLY
    # plt.plot(P_layer_i[:, 0], P_layer_i[:, 1])
    # plt.xlim([0, 5])
    # plt.ylim([-2.5, 2.5])
    # plt.show()

    ###################################### SIMULATION OF THE SCENE ########################################

    scene.lights = []
    scene.ambient = vector(1, 1, 1)
    scene.visible = False

    #Set view
    #scene.center = vector(50,100,0)        #doesn't work for some reason correctly?
    scene.camera.axis = vector(5,2, 0)
    scene.camera.pos = vector(-300, 10, 0)

    # # #DEBUGGING ONLY
    # scene.camera.axis = vector(0,-1, 0)
    # scene.camera.pos = vector(0, 800, 0)

    print("Begin making objects...")
    # Make Particle objects
    particles = np.array([])
    #for pos in P:
    #    particles = np.append(particles, Particle(pos, 200))#height - 100))

    for pos, height in zip(P,heights):
        particles = np.append(particles, Particle(pos, height - 100))#height - 100))

    print("Done making objects.")
    # Main loop
    run = True
    start = time.time()

    # Only draw when necessary
    n_frames = 0
    print("Begin propagation...")
    while run:
        # Set the fps
        rate(fps)
        time_propagating = clock() - time_propagating
        # Simulate the scattering of electrons
        for particle in particles:
            # Choose the length of the electron paths
            particle.scatter(B)

        print(f'Progress {particles[0].t * 100: .1f} %.')
        time_propagating = clock() - time_propagating

        # Check if one frame of simulation is complete
        finished = True
        for particle in particles:
            if not particle.is_done():
                finished = False
                break

        # # Print mouse position
        # if screen_size:
        #     print(pyautogui.position())

        # Record frame when it is ready
        if finished:
            # Allow the scene to draw again

            print("Propagation has ended.")
            #Earth
            box(pos = vector(0,0,0), length=10000, height = 0.0001, width= 10000, color = color.gray(0.2))

            # #Cartesian coordinates
            # xaxis = arrow(pos=vector(0,0,0), axis=vector(500,0,0), color = color.red)
            # yaxis = arrow(pos=vector(0,0,0), axis=vector(0,500,0), color = color.green)
            # zaxis = arrow(pos=vector(0,0,0), axis=vector(0,0,500), color = color.blue)

            if frame == n_frames + 16:
                break                  #if: break then only n frame. Otherwise it runs more frames.

            # Add one to the frame number
            frame += 1
            
            seed2 += 0.02    #for initial height variations
            seedy += 1 / 175   #for P variations

            # Calculate the value of P
            P = np.array([])
            heights = np.array([])
            #print(f"Creating layer {i}...")

            #time_making_sheet = clock() - time_making_sheet

            for i in range(1, b + 1):
                print(f"Creating layer {i}...")
                P_layer_i = generate_curve(Pi, Pf, n, b, i, phi_i, phi_f, w, wl, B, seedx, seedy)
                for j in range(len(P_layer_i)):
                    #Changes initial height
                    height = (290 + 20* pnoise2(seed1 + j * ds, seed2)) - (290 + 20* pnoise2(seed1 + j * ds, seed2) - 140) * (0.5* np.sin(8e2*j/n) + 0.5)
                    P = np.append(P, Vector(P_layer_i[j, 0], P_layer_i[j, 1], height - 100))#
                    heights = np.append(heights, height)

            #print("Done creating initial positions.")
            #time_making_sheet = clock() - time_making_sheet

            # Make Particle objects
            #print("Begin making objects...")
            particles = np.array([])
            for pos, height in zip(P,heights):
                particles = np.append(particles, Particle(pos, height - 100))#height - 100))

            #print("Done making objects.")



            # Clear screen
            clear_screen()

#Export the scene as .pov file
print("Begin exporting...")
time_export = clock() - time_export
#scene.pause('Adjust the camera, then click to export to POV-ray.')           #if ON, you can adjust the picture manually as well, before exporting picture
povexport.export(canvas=scene, filename= f'frame{format_frame(frame)}.pov', include_list= None, shadowless = True)
time_export = clock() - time_export
print("POV-ray file has been exported.")


total_time = clock() - total_time
print("This program took", f'{total_time: .1f}',"seconds.")
if n_frames == 0:
    print("Creating initial sheet took", f'{time_making_sheet / total_time * 100: .1f}',"%.")
    print("Propagation of electrons took", f'{time_propagating / total_time * 100: .1f}',"%.")
    print("Exporting took", f'{time_export / total_time * 100: .1f}', "%.")

print(f"{N_particles * 360 * b / 10**6: .2f} million particles created.")
print("Simulation complete")