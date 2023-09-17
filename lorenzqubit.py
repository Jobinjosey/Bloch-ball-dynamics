
import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

#N_trajectories = 25
import tkinter as tk
from tkinter import simpledialog

def get_user_input(parameter_name, default_value):
    user_input = simpledialog.askstring("Input", f"Enter {parameter_name} (leave blank for default {default_value}): ")
    if user_input:
        return float(user_input)
    else:
        return default_value

def show_letter_by_letter(label, text, speed):
    for i in range(len(text)):
        label.config(text=label.cget("text") + text[i])
        label.update_idletasks()
        label.after(speed)

def get_input_parameters():
    global sigma, beta, rho, g, N_trajectories

    sigma = get_user_input("sigma", 10.0)
    beta = get_user_input("beta", 8./3)
    rho = get_user_input("rho", 28.0)
    g = get_user_input("g", 0.7)

    N_trajectories = int(simpledialog.askstring("Input", "Enter the number of trajectories:") or 1)

root = tk.Tk()
root.title("Lorenz Attractor Interactive Game")

# Set the dimensions of the window
root.geometry("800x600")

# Explanations
explanation_label = tk.Label(root, text="", wraplength=750, justify="left", font=("Arial", 16, "bold"))
explanation_label.pack()

explanations = [
    "Welcome to the Lorenz Butterfly Qubit Interactive Game!",
    "The classical nonlinear systems exhibit rich dynamical behavior, including bifurcations, strange attractors, etc. Here is an interactive demonstration showcasing a nonlinear qubit model and extending the famous Lorenz model into the quantum regime to investigate quantum information processing",
    "Let's start! Below, you can find the equations for Lorenz's 1963 model. Take a look at the variable parameters for the gameplay!",
    "dx/dt= σ (y − x),dy/dt=ρx − y − gxz,dz/dt= − βz + gxy",
    "Sigma (σ) controls the rate at which the variables change",
    "Beta (β) determines the nature of the flow.",
    "Rho (ρ) influences the size of the lorenz butterfly quit",
    "The parameter 'g' is a customizable factor you can utilize. Try manipulating 'g' to position the butterfly qubit inside the Bloch sphere",
    "Take a look at the pop-out where you can position the Lorenz attractor inside the Bloch sphere. Give it a try!",
    "IF YOU CHOOSE RIGHT PARAMETER, YOU'LL OBSERVE POINTS IN THE LORENZ QUBIT SIMULATION REPRESENTING RANDOM INITIAL CONDITIONS. THE TRAJECTORIES SWIFTLY CONVERGE TOWARDS ONE OF THE TWO DISC-SHAPED SETS, OSCILLATING UNPREDICTABLY BETWEEN THEM. THIS BEHAVIOR MIRRORS THE APERIODIC REVERSALS OF THE MALKUS WATERWHEEL, AS DEPICTED IN ITS FOURIER REPRESENTATION.",
    "Repeat the game to find optimal parameters.!"
]

explanation_index = 0

def next_explanation():
    global explanation_index

    if explanation_index < len(explanations):
        show_letter_by_letter(explanation_label, explanations[explanation_index], 50)

        # Change color for specific portions
        if explanation_index == 3:
            explanation_label.config(fg='blue')  # Change color for equations
        else:
            explanation_label.config(fg='black')  # Reset color for other explanations

        explanation_index += 1

        # Add a space between explanations
        explanation_label.config(text=explanation_label.cget("text") + "\n\n")

    else:
        get_input_parameters()

next_explanation_button = tk.Button(root, text="Next", command=next_explanation)
next_explanation_button.pack()

root.mainloop()
def lorentz_deriv(coords, t0, sigma=10., beta=8./3, rho=28.0):
    x, y, z = coords
    return [sigma * (y - x), x * rho - y - g * x * z, g * x * y - beta * z]

np.random.seed(1)
x0 = -20 + 40 * np.random.random((N_trajectories, 3))

t = np.linspace(0, 10, 1000)
x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t) for x0i in x0])

 #Create the sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_sphere = 100 * np.outer(np.cos(u), np.sin(v))
y_sphere = 100 * np.outer(np.sin(u), np.sin(v))
z_sphere = 100 * np.outer(np.ones(np.size(u)), np.cos(v))

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# Plot the sphere
sphere = ax.plot_surface(x_sphere, y_sphere, z_sphere, color=(0, 0, 0, 0.05), rstride=10, cstride=10, linewidth=0, antialiased=True)

# Add lines along the sphere
ax.plot_wireframe(x_sphere, y_sphere, z_sphere, color="white", rcount=10, ccount=10)

# Plot the x-axis
#ax.plot([-60, 60], [0, 0], [0, 0], color='red', linewidth=8)
#ax.text(70, 0, 0, 'X', color='red', fontsize=20)

# Plot the y-axis
#ax.plot([0, 0], [-60, 60], [0, 0], color='green', linewidth=8)
#ax.text(0, 70, 0, 'Y', color='green', fontsize=20)

# Plot the z-axis
#ax.plot([0, 0], [0, 0], [5, 55], color='blue', linewidth=2)
#ax.text(0, 0, 60, 'Z', color='blue', fontsize=12)

positions = {
    '|0⟩': (0, 0, -80),
    '|1⟩': (0, 0, 80),
    '|-i⟩': (0, -100, 0),
    '|+i⟩': (0, 100, 0),
    '|-⟩': (-100, 0, 0),
    '|+⟩': (100, 0, 0)
}

# Add the states
for state, pos in positions.items():
    ax.text(pos[0], pos[1], pos[2], state, color='black', fontsize=20, ha='center')



# Add legend
#ax.legend()
# Choose a different color for each trajectory
colors = plt.cm.plasma(np.linspace(0, 1, N_trajectories))

# Set up lines and points with labels
lines = sum([ax.plot([], [], [], '-', c=c, label=f'Trajectory {i}') for i, c in enumerate(colors)], [])
pts = sum([ax.plot([], [], [], 'o', c=c, label=f'Point {i}') for i, c in enumerate(colors)], [])


ax.set_xlim((-60, 60))
ax.set_ylim((-60, 60))
ax.set_zlim((5, 55))

ax.view_init(30, 0)

# Initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts + [sphere]

# Animation function. This will be called sequentially with the frame number
def animate(i):
    # We'll step two time-steps per frame. This leads to nice results.
    i = (2 * i) % x_t.shape[1]

    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])

    ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return lines + pts + [sphere]

# Instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=500, interval=30, blit=True)

fig.set_size_inches(9, 9)  # You can adjust the dimensions as needed

# Adjust layout before saving
#plt.tight_layout()

# Save the animation
# Save the animation
anim.save('animation3.gif', writer='pillow', fps=30)


plt.show()


