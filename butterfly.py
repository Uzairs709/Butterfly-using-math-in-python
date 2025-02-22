import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class PolarPlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polar Curve Animation")
        self.setGeometry(100, 100, 1200, 900)  # Increased window size

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        self.canvas = FigureCanvas(plt.figure(figsize=(12, 12)))  # Further increased canvas size
        layout.addWidget(self.canvas)

        self.start_button = QPushButton("Start Animation")
        self.start_button.clicked.connect(self.start_animation)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Animation")
        self.stop_button.clicked.connect(self.stop_animation)
        layout.addWidget(self.stop_button)

        self.init_plot()
        self.anim = None
        self.repeat_count = 0
        self.max_repeats = 100  # Draw the graph 100 times
        self.lines = []  # Store lines for each cycle
        self.colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'white']  # Color cycle
        self.color_index = 0  # Index to track the current color

    def init_plot(self):
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xlim(-3.5, 3.5)  # Increased limits to prevent cutting
        self.ax.set_ylim(-3.5, 3.5)
        self.ax.set_title("Polar Curve Animation", color='white')  # Set title color to white
        self.ax.set_facecolor('black')  # Set background to black
        self.ax.set_aspect('equal')
        self.ax.axis('off')  # Hide x and y axes
        self.theta = np.linspace(0, 4 * np.pi, 2000)  # Single cycle for resetting

    def polar_function_rotated(self, theta):
        theta_rotated = theta - np.pi / 2
        return np.exp(np.cos(theta_rotated)) - 2 * np.cos(4 * theta_rotated) - (np.sin(theta_rotated / 12)) ** 5

    def update(self, frame):
        if frame >= len(self.theta):
            self.repeat_count += 1
            if self.repeat_count >= self.max_repeats:
                self.stop_animation()
                return
            frame = 0  # Reset drawing for next cycle

        x_rotated = self.polar_function_rotated(self.theta[:frame]) * np.cos(self.theta[:frame])
        y_rotated = self.polar_function_rotated(self.theta[:frame]) * np.sin(self.theta[:frame])

        # Create a new line for the current cycle if it's the first frame
        if frame == 0:
            line, = self.ax.plot([], [], linestyle="solid", lw=2, color=self.colors[self.color_index])
            self.lines.append(line)
            self.color_index = (self.color_index + 1) % len(self.colors)  # Cycle through colors

        # Update the current line
        self.lines[-1].set_data(x_rotated, y_rotated)
        return self.lines

    def start_animation(self):
        if self.anim is None:
            self.repeat_count = 0
            self.lines = []  # Reset previous lines
            self.color_index = 0  # Reset color index
            self.anim = animation.FuncAnimation(self.canvas.figure, self.update, frames=len(self.theta), interval=5,
                                                blit=False, repeat=True)
        self.canvas.draw()

    def stop_animation(self):
        if self.anim is not None:
            self.anim.event_source.stop()
            self.anim = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PolarPlotApp()
    window.show()
    sys.exit(app.exec())