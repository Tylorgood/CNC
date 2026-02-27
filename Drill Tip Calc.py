import math
import tkinter as tk
from tkinter import ttk, messagebox

def drill_tip_length(diameter, point_angle_deg=118.0):
    half_angle_rad = math.radians(point_angle_deg / 2.0)
    return diameter / (2.0 * math.tan(half_angle_rad))

def tip_diameter_at_depth(depth, point_angle_deg=118.0):
    half_angle_rad = math.radians(point_angle_deg / 2.0)
    return 2.0 * depth * math.tan(half_angle_rad)

def to_float(entry: tk.Entry, name: str) -> float:
    raw = entry.get().strip()
    if raw == "":
        raise ValueError(f"{name} is blank.")
    return float(raw)

def calculate():
    try:
        units = units_var.get()

        dia = to_float(diameter_entry, "Diameter")
        angle = float(angle_entry.get().strip() or "118")

        tip_len = drill_tip_length(dia, angle)

        flat_depth_raw = flat_depth_entry.get().strip()
        drill_to = None
        if flat_depth_raw != "":
            flat_depth = float(flat_depth_raw)
            drill_to = flat_depth + tip_len

        # Optional: diameter at depth from tip
        depth_raw = depth_from_tip_entry.get().strip()
        d_at_depth = None
        if depth_raw != "":
            depth = float(depth_raw)
            d_at_depth = tip_diameter_at_depth(depth, angle)

        # Output
        tip_len_var.set(f"{tip_len:.6f} {units}")

        if drill_to is None:
            drill_to_var.set("—")
        else:
            drill_to_var.set(f"{drill_to:.6f} {units}")

        if d_at_depth is None:
            d_at_depth_var.set("—")
        else:
            d_at_depth_var.set(f"{d_at_depth:.6f} {units}")

    except Exception as e:
        messagebox.showerror("Input Error", str(e))

def clear_all():
    diameter_entry.delete(0, tk.END)
    angle_entry.delete(0, tk.END)
    flat_depth_entry.delete(0, tk.END)
    depth_from_tip_entry.delete(0, tk.END)
    angle_entry.insert(0, "118")
    tip_len_var.set("—")
    drill_to_var.set("—")
    d_at_depth_var.set("—")

# --- UI ---
root = tk.Tk()
root.title("Drill Tip Length Calculator (118°/Any Angle)")
root.geometry("520x360")
root.resizable(False, False)

main = ttk.Frame(root, padding=16)
main.pack(fill="both", expand=True)

title = ttk.Label(main, text="Drill Tip Length Calculator", font=("Segoe UI", 16, "bold"))
title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

units_var = tk.StringVar(value="in")

ttk.Label(main, text="Units:").grid(row=1, column=0, sticky="w")
units_combo = ttk.Combobox(main, textvariable=units_var, values=["in", "mm"], width=8, state="readonly")
units_combo.grid(row=1, column=1, sticky="w")

ttk.Label(main, text="Drill Diameter:").grid(row=2, column=0, sticky="w", pady=(10, 0))
diameter_entry = ttk.Entry(main, width=18)
diameter_entry.grid(row=2, column=1, sticky="w", pady=(10, 0))
ttk.Label(main, text="(example: 0.34)").grid(row=2, column=2, sticky="w", pady=(10, 0))

ttk.Label(main, text="Point Angle (deg):").grid(row=3, column=0, sticky="w", pady=(10, 0))
angle_entry = ttk.Entry(main, width=18)
angle_entry.grid(row=3, column=1, sticky="w", pady=(10, 0))
angle_entry.insert(0, "118")
ttk.Label(main, text="(118, 135, etc.)").grid(row=3, column=2, sticky="w", pady=(10, 0))

ttk.Separator(main).grid(row=4, column=0, columnspan=3, sticky="ew", pady=12)

ttk.Label(main, text="Optional Flat Depth (for drill-to):").grid(row=5, column=0, sticky="w")
flat_depth_entry = ttk.Entry(main, width=18)
flat_depth_entry.grid(row=5, column=1, sticky="w")
ttk.Label(main, text="(leave blank if not needed)").grid(row=5, column=2, sticky="w")

ttk.Label(main, text="Optional Depth From Tip (for dia@depth):").grid(row=6, column=0, sticky="w", pady=(10, 0))
depth_from_tip_entry = ttk.Entry(main, width=18)
depth_from_tip_entry.grid(row=6, column=1, sticky="w", pady=(10, 0))
ttk.Label(main, text="(depth measured from the point)").grid(row=6, column=2, sticky="w", pady=(10, 0))

ttk.Separator(main).grid(row=7, column=0, columnspan=3, sticky="ew", pady=12)

# Results
tip_len_var = tk.StringVar(value="—")
drill_to_var = tk.StringVar(value="—")
d_at_depth_var = tk.StringVar(value="—")

ttk.Label(main, text="Tip Length:").grid(row=8, column=0, sticky="w")
ttk.Label(main, textvariable=tip_len_var, font=("Consolas", 12, "bold")).grid(row=8, column=1, sticky="w")

ttk.Label(main, text="Drill To (Flat Depth + Tip):").grid(row=9, column=0, sticky="w", pady=(8, 0))
ttk.Label(main, textvariable=drill_to_var, font=("Consolas", 12, "bold")).grid(row=9, column=1, sticky="w", pady=(8, 0))

ttk.Label(main, text="Diameter at Depth From Tip:").grid(row=10, column=0, sticky="w", pady=(8, 0))
ttk.Label(main, textvariable=d_at_depth_var, font=("Consolas", 12, "bold")).grid(row=10, column=1, sticky="w", pady=(8, 0))

# Buttons
btns = ttk.Frame(main)
btns.grid(row=11, column=0, columnspan=3, sticky="w", pady=16)

ttk.Button(btns, text="Calculate", command=calculate).grid(row=0, column=0, padx=(0, 10))
ttk.Button(btns, text="Clear", command=clear_all).grid(row=0, column=1)

# Nice default focus
diameter_entry.focus()
root.mainloop()
