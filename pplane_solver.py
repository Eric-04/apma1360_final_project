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
a = 1
b = 0.5

ds_expr = f"{a}*(1-s) - {b}*s*i"
di_expr = f"{b}*s*i - i"

# ============================================================
# SETTINGS
# ============================================================

s_min, s_max = -5, 5
i_min, i_max = -5, 5

grid_size = 25
trajectory_time = 20
dt = 0.01

# Initial conditions to trace trajectories
initial_points = [
    (4, 2),
    (-4, 3),
    (-3, -2),
    (3, -4),
    (1, -2),
    (-1, 4),
    (2, 1),
    (-2, -3),
    (0.5, 3.5),
    (-4.5, 0.5),
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

def simulate(s0, i0, tmax, dt):
    n = int(tmax / dt)

    s_vals = np.zeros(n)
    i_vals = np.zeros(n)

    s_vals[0] = s0
    i_vals[0] = i0

    for k in range(n - 1):
        ds = f(s_vals[k], i_vals[k])
        di = g(s_vals[k], i_vals[k])

        s_vals[k + 1] = s_vals[k] + dt * ds
        i_vals[k + 1] = i_vals[k] + dt * di

    return s_vals, i_vals

# Plot trajectories
for s0, i0 in initial_points:
    s_path, i_path = simulate(s0, i0, trajectory_time, dt)

    plt.plot(s_path, i_path, linewidth=2)
    # plt.plot(s0, i0, 'ro')

# ============================================================
# LABELS
# ============================================================

plt.title("Phase Plane Plot")
plt.xlabel("s")
plt.ylabel("i")

plt.xlim(s_min, s_max)
plt.ylim(i_min, i_max)

plt.grid(True)
# plt.colorbar(label="Vector magnitude")

plt.show()