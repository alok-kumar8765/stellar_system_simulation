import turtle
import math
import random
import time
import tkinter as tk

class SolarSystemApp:
    def __init__(self):
        # 1. Screen Setup
        self.screen = turtle.Screen()
        self.screen.setup(width=1300, height=850)
        self.screen.bgcolor("#03030a")
        self.screen.title("Stellar Orbit - Solar System Simulation")
        self.screen.tracer(0, 0) # Disable auto-updates for manual frame management

        self.running = True
        
        # Handle graceful window closure to prevent TclError
        try:
            self.screen._root.protocol("WM_DELETE_WINDOW", self.quit_app)
        except Exception:
            pass

        # 2. Initialize Environment Layers
        self._create_starfield(200)
        self._draw_sun()
        
        # 3. Define Planet Configurations (Name, Size, Orbit Radius, Speed, Color)
        planet_configs = [
            ("Mercury", 4,  70,  2.2, "#a8a8a8"),
            ("Venus",   7,  110, 1.7, "#e3bb76"),
            ("Earth",   9,  160, 1.2, "#2277ff"),
            ("Mars",    6,  210, 0.9, "#cc4400"),
            ("Jupiter", 18, 290, 0.5, "#d4a373"),
            ("Saturn",  14, 370, 0.35, "#f4e2bb"),
            ("Uranus",  11, 440, 0.25, "#70d6ff"),
            ("Neptune", 11, 500, 0.2,  "#3a86ff"),
        ]

        # Draw orbit paths before spawning planets
        self._draw_orbits([p[2] for p in planet_configs])

        # Instantiate Planet objects
        self.planets = [Planet(data, self.screen) for data in planet_configs]

    def quit_app(self):
        """Cleanly terminates the simulation loop and exits."""
        self.running = False
        try:
            self.screen.bye()
        except Exception:
            pass

    def _create_starfield(self, count):
        """Generates a static background starfield."""
        star = turtle.Turtle()
        star.hideturtle()
        star.speed(0)
        star.color("white")
        
        for _ in range(count):
            x = random.randint(-650, 650)
            y = random.randint(-425, 425)
            size = random.randint(1, 3)
            star.penup()
            star.goto(x, y)
            star.pendown()
            star.dot(size, random.choice(["#ffffff", "#e0e6ff", "#fffaed"]))

    def _draw_sun(self):
        """Draws a multi-layered glowing sun at the center."""
        sun = turtle.Turtle()
        sun.hideturtle()
        sun.speed(0)
        
        # Outer Corona / Glow
        sun.penup()
        sun.goto(0, -42)
        sun.color("#ff3300")
        sun.begin_fill()
        sun.circle(42)
        sun.end_fill()

        # Mid Glow Layer
        sun.penup()
        sun.goto(0, -32)
        sun.color("#ff9900")
        sun.begin_fill()
        sun.circle(32)
        sun.end_fill()

        # Core Bright Sun
        sun.penup()
        sun.goto(0, -22)
        sun.color("#ffcc00")
        sun.begin_fill()
        sun.circle(22)
        sun.end_fill()

    def _draw_orbits(self, distances):
        """Draws faint circular reference lines for planetary orbits."""
        orbit = turtle.Turtle()
        orbit.hideturtle()
        orbit.speed(0)
        orbit.color("#15152b")
        orbit.pensize(1)

        for dist in distances:
            orbit.penup()
            orbit.goto(0, -dist)
            orbit.pendown()
            orbit.circle(dist)

    def run(self):
        """Main execution loop with robust exception handling for window exits."""
        while self.running:
            try:
                for planet in self.planets:
                    planet.update_position()
                
                self.screen.update()
                time.sleep(0.015) # Throttle loop (~60 FPS target)
            except (turtle.Terminator, tk.TclError):
                break


class Planet:
    def __init__(self, config, screen):
        self.name, self.radius, self.distance, self.speed, self.color = config
        self.angle = random.uniform(0, 360) # Random initial orbital phase
        
        # Dedicated turtle instance per planet
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.shape("circle")
        self.t.shapesize(self.radius / 10) # Scale turtle shape factor
        self.t.color(self.color)
        self.t.penup()
        self.t.speed(0)

        # Dedicated text turtle for planet labels
        self.writer = turtle.Turtle()
        self.writer.hideturtle()
        self.writer.speed(0)
        self.writer.color("#a0a5c0")
        self.writer.penup()

    def update_position(self):
        """Advances orbital angle, recalculates coordinates, and updates text label."""
        self.angle += self.speed
        if self.angle >= 360:
            self.angle -= 360

        rad = math.radians(self.angle)
        x = self.distance * math.cos(rad)
        y = self.distance * math.sin(rad)

        # Update planet node
        self.t.goto(x, y)
        self.t.showturtle()

        # Update label position and text
        self.writer.goto(x, y + self.radius + 8)
        self.writer.clear()
        self.writer.write(self.name, align="center", font=("Arial", 8, "normal"))


if __name__ == "__main__":
    app = SolarSystemApp()
    app.run()