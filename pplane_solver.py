# pplane_solver.py
#
# Interactive phase plane / direction field plotter
# Variables are:
#   s = x-axis variable
#   i = y-axis variable
#
# You can enter your own equations:
#   ds/dt = f(s, i)
#   di/dt = g(s, i)
#
# Example:
#   ds_expr = "i - 0.5*s"
#   di_expr = "sin(s)"
#
# Supports:
#   sin, cos, tan, exp, log, sqrt, pi, etc.

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# ENTER YOUR EQUATIONS HERE
# ============================================================

# R0 < (delta+phi)/delta
gamma = 3
mu = 1
beta = 2
v = 2

# R0 = (delta+phi)/delta
# gamma = 3
# mu = 1
# beta = 12
# v = 2

# R0 > (delta+phi)/delta
# gamma = 3
# mu = 1
# beta = 24
# v = 2

delta = mu/(mu + gamma)
R0 = beta/(mu + gamma)
phi = v/(mu+gamma)
print(R0, (delta+phi)/delta)

eq1 = (delta/(delta+phi), 0)
eq2 = (1/R0, delta - (phi + delta)/R0)
print("equilibrium", eq1, eq2)

ds_expr = f"{delta}*(1-s) - {R0}*s*i -{phi} * s"
di_expr = f"{R0}*s*i - i"

# ============================================================
# SETTINGS
# ============================================================

s_min, s_max = 0, 0.8
i_min, i_max = -1, 1

grid_size = 25
trajectory_time = 20
dt = 0.01

# Initial conditions to trace trajectories
point_spacing = 0.125

s_points = np.arange(s_min, s_max + point_spacing, point_spacing)
i_points = np.arange(i_min, i_max + point_spacing, point_spacing)

initial_points = [
    (s0, i0)
    for s0 in s_points
    for i0 in i_points
]


# ============================================================
# SAFE MATH ENVIRONMENT
# ============================================================

safe_dict = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "exp": np.exp,
    "log": np.log,
    "sqrt": np.sqrt,
    "abs": np.abs,
    "pi": np.pi,
}

# ============================================================
# BUILD VECTOR FIELD
# ============================================================

s = np.linspace(s_min, s_max, grid_size)
i = np.linspace(i_min, i_max, grid_size)

S, I = np.meshgrid(s, i)

# Evaluate equations
DS = eval(ds_expr, {"__builtins__": {}}, {**safe_dict, "s": S, "i": I})
DI = eval(di_expr, {"__builtins__": {}}, {**safe_dict, "s": S, "i": I})

# Normalize arrows
magnitude = np.sqrt(DS**2 + DI**2)
magnitude[magnitude == 0] = 1

DS_norm = DS / magnitude
DI_norm = DI / magnitude

# ============================================================
# PLOT PHASE PLANE
# ============================================================

plt.figure(figsize=(10, 8))

# Direction field
plt.quiver(
    S, I,
    DS_norm, DI_norm,
    magnitude,
    cmap="viridis",
    pivot="mid"
)

# ============================================================
# TRAJECTORY SOLVER (Euler method)
# ============================================================

def f(s, i):
    return eval(ds_expr, {"__builtins__": {}}, {**safe_dict, "s": s, "i": i})

def g(s, i):
    return eval(di_expr, {"__builtins__": {}}, {**safe_dict, "s": s, "i": i})

def simulate(s0, i0, tmax, dt, bound=100):
    n = int(tmax / dt)

    s_vals = [s0]
    i_vals = [i0]

    s = s0
    i = i0

    for _ in range(n - 1):

        ds = f(s, i)
        di = g(s, i)

        s = s + dt * ds
        i = i + dt * di

        # Stop if solution blows up
        if (
            not np.isfinite(s)
            or not np.isfinite(i)
            or abs(s) > bound
            or abs(i) > bound
        ):
            break

        s_vals.append(s)
        i_vals.append(i)

    return np.array(s_vals), np.array(i_vals)

# Plot trajectories
for s0, i0 in initial_points:
    s_path, i_path = simulate(s0, i0, trajectory_time, dt)

    plt.plot(s_path, i_path, linewidth=2)
    # plt.plot(s0, i0, 'ro')

# ============================================================
# LABELS
# ============================================================

# Plot equilibrium points
plt.plot(eq1[0], eq1[1], 'ro', markersize=8)
plt.plot(eq2[0], eq2[1], 'bo', markersize=8)

plt.title("Phase Plane Plot")
plt.xlabel("s")
plt.ylabel("i")

plt.xlim(s_min, s_max)
plt.ylim(i_min, i_max)

plt.grid(True)
# plt.colorbar(label="Vector magnitude")

plt.show()