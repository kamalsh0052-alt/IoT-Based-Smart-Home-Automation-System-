import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime


class SmartHomeDashboard:
    def __init__(self, root):
        self.root = root

        # Window
        self.root.title("IoT Smart Home Automation System")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#0f1720")

        # ---------------- COLORS ----------------
        self.bg = "#0f1720"
        self.sidebar = "#151f2b"
        self.card = "#1b2734"
        self.card2 = "#263849"

        self.text = "#f4f7fa"
        self.muted = "#9aa8b6"

        self.green = "#35d07f"
        self.red = "#ff5f61"
        self.blue = "#4da3ff"
        self.cyan = "#39d5ff"
        self.yellow = "#f4c95d"

        # ---------------- DEVICE STATES ----------------
        self.light = False
        self.fan = False
        self.ac = False
        self.door_locked = True
        self.auto_mode = False

        # ---------------- SENSOR VALUES ----------------
        self.temperature = 26.5
        self.humidity = 58.0
        self.energy = 0.05
        self.motion = False

        # Graph data
        self.temp_history = []

        # Build UI
        self.build_header()
        self.build_sidebar()

        self.main = tk.Frame(
            self.root,
            bg=self.bg
        )
        self.main.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.show_dashboard()

        # Start updates
        self.update_sensors()
        self.update_clock()

    # ==================================================
    # BUTTON
    # ==================================================

    def make_button(
        self,
        parent,
        text,
        command,
        bg=None,
        fg=None,
        **kwargs
    ):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg if bg else self.card2,
            fg=fg if fg else self.text,
            activebackground=bg if bg else self.card2,
            activeforeground=fg if fg else self.text,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            **kwargs
        )

    # ==================================================
    # HEADER
    # ==================================================

    def build_header(self):

        header = tk.Frame(
            self.root,
            bg=self.card,
            height=72
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(
            header,
            bg=self.card
        )

        left.pack(
            side="left",
            padx=24
        )

        tk.Label(
            left,
            text="SMART HOME",
            bg=self.card,
            fg=self.text,
            font=("Segoe UI", 20, "bold")
        ).pack(side="left")

        tk.Label(
            left,
            text="  |  IoT Automation Dashboard",
            bg=self.card,
            fg=self.muted,
            font=("Segoe UI", 10)
        ).pack(
            side="left",
            pady=5
        )

        tk.Label(
            header,
            text="● ONLINE",
            bg=self.card,
            fg=self.green,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="right",
            padx=18
        )

        self.clock = tk.Label(
            header,
            text="",
            bg=self.card,
            fg=self.muted,
            font=("Segoe UI", 10)
        )

        self.clock.pack(
            side="right",
            padx=10
        )

    # ==================================================
    # SIDEBAR
    # ==================================================

    def build_sidebar(self):

        side = tk.Frame(
            self.root,
            bg=self.sidebar,
            width=190
        )

        side.pack(
            side="left",
            fill="y"
        )

        side.pack_propagate(False)

        tk.Label(
            side,
            text="CONTROL",
            bg=self.sidebar,
            fg=self.muted,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(25, 12)
        )

        menu = [
            ("Dashboard", self.show_dashboard),
            ("Devices", self.show_devices),
            ("Energy", self.show_energy),
            ("Security", self.show_security)
        ]

        for name, command in menu:

            self.make_button(
                side,
                name,
                command,
                bg=self.card,
                fg=self.text,
                anchor="w",
                padx=18,
                pady=10
            ).pack(
                fill="x",
                padx=10,
                pady=3
            )

        tk.Label(
            side,
            text="SYSTEM MODE",
            bg=self.sidebar,
            fg=self.muted,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(25, 10)
        )

        self.auto_btn = self.make_button(
            side,
            "AUTO MODE: OFF",
            self.toggle_auto,
            bg=self.card,
            fg=self.yellow,
            padx=10,
            pady=10
        )

        self.auto_btn.pack(
            fill="x",
            padx=10,
            pady=3
        )

        tk.Label(
            side,
            text="Python + Tkinter\nIoT Smart Home Project",
            bg=self.sidebar,
            fg=self.muted,
            font=("Segoe UI", 9),
            justify="left"
        ).pack(
            side="bottom",
            anchor="w",
            padx=20,
            pady=22
        )

    # ==================================================
    # CLEAR MAIN
    # ==================================================

    def clear_main(self):

        for widget in self.main.winfo_children():
            widget.destroy()

    # ==================================================
    # CARD
    # ==================================================

    def make_card(
        self,
        parent,
        title,
        value,
        accent
    ):

        frame = tk.Frame(
            parent,
            bg=self.card,
            height=105
        )

        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            bg=self.card,
            fg=self.muted,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 2)
        )

        value_label = tk.Label(
            frame,
            text=value,
            bg=self.card,
            fg=accent,
            font=("Segoe UI", 20, "bold")
        )

        value_label.pack(
            anchor="w",
            padx=16
        )

        frame.value_label = value_label

        return frame

    # ==================================================
    # DASHBOARD
    # ==================================================

    def show_dashboard(self):

        self.clear_main()

        tk.Label(
            self.main,
            text="Dashboard",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 23, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 2)
        )

        tk.Label(
            self.main,
            text="Real-time monitoring and appliance control",
            bg=self.bg,
            fg=self.muted,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=30
        )

        # ---------------- SENSOR CARDS ----------------

        sensors = tk.Frame(
            self.main,
            bg=self.bg
        )

        sensors.pack(
            fill="x",
            padx=25,
            pady=22
        )

        self.temp_card = self.make_card(
            sensors,
            "Temperature",
            f"{self.temperature:.1f} °C",
            self.cyan
        )

        self.temp_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.humidity_card = self.make_card(
            sensors,
            "Humidity",
            f"{self.humidity:.0f} %",
            self.blue
        )

        self.humidity_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.energy_card = self.make_card(
            sensors,
            "Energy Usage",
            f"{self.energy:.2f} kWh",
            self.yellow
        )

        self.energy_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        security_text = (
            "SECURE"
            if self.door_locked
            else "UNLOCKED"
        )

        self.security_card = self.make_card(
            sensors,
            "Security",
            security_text,
            self.green if self.door_locked else self.red
        )

        self.security_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        # ---------------- DEVICE CONTROL ----------------

        tk.Label(
            self.main,
            text="Device Control",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 8)
        )

        controls = tk.Frame(
            self.main,
            bg=self.bg
        )

        controls.pack(
            fill="x",
            padx=25
        )

        devices = [
            ("LIGHT", self.light, self.toggle_light),
            ("FAN", self.fan, self.toggle_fan),
            ("AIR CONDITIONER", self.ac, self.toggle_ac),
            ("DOOR LOCK", self.door_locked, self.toggle_door)
        ]

        for i, (name, state, command) in enumerate(devices):

            box = tk.Frame(
                controls,
                bg=self.card,
                height=92
            )

            box.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=5
            )

            box.grid_propagate(False)

            tk.Label(
                box,
                text=name,
                bg=self.card,
                fg=self.text,
                font=("Segoe UI", 9, "bold")
            ).pack(
                pady=(11, 5)
            )

            if name == "DOOR LOCK":

                status = (
                    "LOCKED"
                    if state
                    else "UNLOCKED"
                )

            else:

                status = (
                    "ON"
                    if state
                    else "OFF"
                )

            button_color = (
                self.green
                if state
                else self.red
            )

            self.make_button(
                box,
                status,
                command,
                bg=button_color,
                fg="#101820",
                width=14,
                pady=4
            ).pack()

        for i in range(4):

            controls.columnconfigure(
                i,
                weight=1
            )

        # ---------------- GRAPH ----------------

        graph_box = tk.Frame(
            self.main,
            bg=self.card
        )

        graph_box.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=18
        )

        tk.Label(
            graph_box,
            text="Live Temperature Graph",
            bg=self.card,
            fg=self.text,
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 3)
        )

        self.graph = tk.Canvas(
            graph_box,
            bg=self.card,
            highlightthickness=0
        )

        self.graph.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=5
        )

        self.draw_graph()

    # ==================================================
    # DEVICES
    # ==================================================

    def show_devices(self):

        self.clear_main()

        tk.Label(
            self.main,
            text="Devices",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 23, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        tk.Label(
            self.main,
            text="Current appliance status",
            bg=self.bg,
            fg=self.muted,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        devices = [
            (
                "Living Room Light",
                self.light,
                self.toggle_light
            ),
            (
                "Ceiling Fan",
                self.fan,
                self.toggle_fan
            ),
            (
                "Air Conditioner",
                self.ac,
                self.toggle_ac
            ),
            (
                "Main Door Lock",
                self.door_locked,
                self.toggle_door
            )
        ]

        for name, state, command in devices:

            row = tk.Frame(
                self.main,
                bg=self.card,
                height=65
            )

            row.pack(
                fill="x",
                padx=30,
                pady=5
            )

            row.pack_propagate(False)

            tk.Label(
                row,
                text=name,
                bg=self.card,
                fg=self.text,
                font=("Segoe UI", 11)
            ).pack(
                side="left",
                padx=20
            )

            if name == "Main Door Lock":

                status = (
                    "LOCKED"
                    if state
                    else "UNLOCKED"
                )

            else:

                status = (
                    "ON"
                    if state
                    else "OFF"
                )

            button_color = (
                self.green
                if state
                else self.red
            )

            self.make_button(
                row,
                status,
                command,
                bg=button_color,
                fg="#101820",
                width=12
            ).pack(
                side="right",
                padx=20,
                pady=13
            )

    # ==================================================
    # ENERGY
    # ==================================================

    def show_energy(self):

        self.clear_main()

        tk.Label(
            self.main,
            text="Energy Monitoring",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 23, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 15)
        )

        box = tk.Frame(
            self.main,
            bg=self.card
        )

        box.pack(
            fill="x",
            padx=30,
            pady=5
        )

        tk.Label(
            box,
            text="Current Consumption",
            bg=self.card,
            fg=self.muted,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 3)
        )

        tk.Label(
            box,
            text=f"{self.energy:.2f} kWh",
            bg=self.card,
            fg=self.yellow,
            font=("Segoe UI", 28, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        explanation = (
            "Energy usage is estimated from the active appliances. "
            "Light, fan and AC states demonstrate an IoT-based "
            "energy monitoring concept."
        )

        tk.Label(
            self.main,
            text=explanation,
            bg=self.bg,
            fg=self.muted,
            font=("Segoe UI", 11),
            wraplength=800,
            justify="left"
        ).pack(
            anchor="w",
            padx=30,
            pady=20
        )

    # ==================================================
    # SECURITY
    # ==================================================

    def show_security(self):

        self.clear_main()

        tk.Label(
            self.main,
            text="Security",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 23, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 15)
        )

        locked = self.door_locked

        status = (
            "HOME SECURE"
            if locked
            else "DOOR UNLOCKED"
        )

        color = (
            self.green
            if locked
            else self.red
        )

        box = tk.Frame(
            self.main,
            bg=self.card
        )

        box.pack(
            fill="x",
            padx=30,
            pady=5
        )

        tk.Label(
            box,
            text=status,
            bg=self.card,
            fg=color,
            font=("Segoe UI", 25, "bold")
        ).pack(
            pady=(30, 5)
        )

        tk.Label(
            box,
            text="Main Door",
            bg=self.card,
            fg=self.muted,
            font=("Segoe UI", 11)
        ).pack(
            pady=(0, 25)
        )

        self.make_button(
            box,
            "UNLOCK DOOR" if locked else "LOCK DOOR",
            self.toggle_door,
            bg=self.card2,
            fg=self.text,
            width=18,
            pady=8
        ).pack(
            pady=(0, 25)
        )

        tk.Label(
            self.main,
            text=(
                "Motion Sensor: "
                + (
                    "DETECTED"
                    if self.motion
                    else "NO MOTION"
                )
            ),
            bg=self.bg,
            fg=self.red if self.motion else self.green,
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=20
        )

    # ==================================================
    # DEVICE ACTIONS
    # ==================================================

    def toggle_light(self):

        self.light = not self.light
        self.show_dashboard()

    def toggle_fan(self):

        self.fan = not self.fan
        self.show_dashboard()

    def toggle_ac(self):

        self.ac = not self.ac
        self.show_dashboard()

    def toggle_door(self):

        self.door_locked = not self.door_locked

        if self.door_locked:

            messagebox.showinfo(
                "Security",
                "Door locked successfully."
            )

        else:

            messagebox.showwarning(
                "Security",
                "Warning: Door is now unlocked!"
            )

        self.show_dashboard()

    # ==================================================
    # AUTO MODE
    # ==================================================

    def toggle_auto(self):

        self.auto_mode = not self.auto_mode

        if self.auto_mode:

            self.auto_btn.config(
                text="AUTO MODE: ON",
                fg=self.green
            )

            messagebox.showinfo(
                "Auto Mode",
                "Automatic appliance control enabled."
            )

        else:

            self.auto_btn.config(
                text="AUTO MODE: OFF",
                fg=self.yellow
            )

    # ==================================================
    # SENSOR UPDATE
    # ==================================================

    def update_sensors(self):

        # Temperature
        self.temperature += random.uniform(
            -0.15,
            0.15
        )

        self.temperature = max(
            20,
            min(
                35,
                self.temperature
            )
        )

        # Humidity
        self.humidity += random.uniform(
            -0.8,
            0.8
        )

        self.humidity = max(
            35,
            min(
                80,
                self.humidity
            )
        )

        # Motion
        self.motion = random.random() < 0.08

        # Auto mode
        if self.auto_mode:

            if self.temperature >= 28:

                self.fan = True

            else:

                self.fan = False

            if self.temperature >= 31:

                self.ac = True

            else:

                self.ac = False

        # Energy calculation
        self.energy = 0.05

        if self.light:

            self.energy += 0.10

        if self.fan:

            self.energy += 0.30

        if self.ac:

            self.energy += 1.20

        # Store temperature
        self.temp_history.append(
            self.temperature
        )

        if len(self.temp_history) > 45:

            self.temp_history.pop(0)

        # Refresh visible dashboard
        self.refresh_dashboard_values()

        self.root.after(
            1500,
            self.update_sensors
        )

    # ==================================================
    # REFRESH DASHBOARD
    # ==================================================

    def refresh_dashboard_values(self):

        if not hasattr(
            self,
            "temp_card"
        ):

            return

        try:

            self.temp_card.value_label.config(
                text=f"{self.temperature:.1f} °C"
            )

            self.humidity_card.value_label.config(
                text=f"{self.humidity:.0f} %"
            )

            self.energy_card.value_label.config(
                text=f"{self.energy:.2f} kWh"
            )

            security = (
                "SECURE"
                if self.door_locked
                else "UNLOCKED"
            )

            self.security_card.value_label.config(
                text=security,
                fg=(
                    self.green
                    if self.door_locked
                    else self.red
                )
            )

            self.draw_graph()

        except tk.TclError:

            pass

    # ==================================================
    # GRAPH
    # ==================================================

    def draw_graph(self):

        if not hasattr(
            self,
            "graph"
        ):

            return

        self.graph.delete("all")

        width = max(
            self.graph.winfo_width(),
            600
        )

        height = max(
            self.graph.winfo_height(),
            150
        )

        # Grid
        for y in range(
            25,
            height,
            30
        ):

            self.graph.create_line(
                0,
                y,
                width,
                y,
                fill="#2a3948"
            )

        if len(
            self.temp_history
        ) < 2:

            return

        low = (
            min(self.temp_history)
            - 1
        )

        high = (
            max(self.temp_history)
            + 1
        )

        if high == low:

            high = low + 1

        points = []

        for i, value in enumerate(
            self.temp_history
        ):

            x = (
                10
                + (
                    i
                    / (
                        len(
                            self.temp_history
                        ) - 1
                    )
                )
                * (
                    width - 20
                )
            )

            y = (
                height
                - 15
                - (
                    (value - low)
                    / (high - low)
                )
                * (
                    height - 35
                )
            )

            points.extend(
                [x, y]
            )

        self.graph.create_line(
            points,
            fill=self.cyan,
            width=3,
            smooth=True
        )

        self.graph.create_text(
            width - 10,
            15,
            text=f"{self.temperature:.1f} °C",
            fill=self.cyan,
            anchor="e",
            font=("Segoe UI", 9, "bold")
        )

    # ==================================================
    # CLOCK
    # ==================================================

    def update_clock(self):

        self.clock.config(
            text=datetime.now().strftime(
                "%d-%m-%Y   %I:%M:%S %p"
            )
        )

        self.root.after(
            1000,
            self.update_clock
        )


# ======================================================
# START APPLICATION
# ======================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SmartHomeDashboard(root)

    root.mainloop()