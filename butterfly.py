import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class PolarPlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Butterfly")

        # Create the central widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Create canvas with increased size
        self.canvas = FigureCanvas(plt.figure(figsize=(12, 12)))
        layout.addWidget(self.canvas)
        self.canvas.figure.patch.set_facecolor('black')

        self.init_plot()
        self.anim = None
        self.repeat_count = 0
        self.max_repeats = 100  # Number of full cycles to draw
        self.lines = []  # Store line segments

        # Generate a smooth gradient of colors from a colormap (e.g. plasma)
        # Here we generate 200 colors; you can adjust the number for a smoother transition.
        cmap = cm.get_cmap("plasma")
        self.colors = [cmap(i) for i in np.linspace(0, 1, 200)]
        self.color_index = 0  # Track current color index

        # Tracking the last segment index (each segment is 50ms, i.e. 10 frames)
        self.last_segment_index = -1
        self.segment_start_frame = 0

        # Automatically start animation after 20ms delay
        QTimer.singleShot(20, self.start_animation)

    def init_plot(self):
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xlim(-3.5, 3.5)
        self.ax.set_ylim(-3.5, 3.5)
        self.ax.set_facecolor('black')
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.theta = np.linspace(0, 12 * np.pi, 2000)

    def polar_function_rotated(self, theta):
        theta_rotated = theta - np.pi / 2
        return np.exp(np.cos(theta_rotated)) - 2 * np.cos(4 * theta_rotated) - (np.sin(theta_rotated / 12)) ** 5

    def update(self, frame):
        # Calculate elapsed time in seconds (each frame is 5ms)
        elapsed_ms = frame * 5
        # Determine the current segment based on 50ms intervals
        current_segment = elapsed_ms // 50

        # If we are at a new segment, start a new line segment.
        if current_segment > self.last_segment_index:
            self.last_segment_index = current_segment
            # Start the new segment from the last point (if available) to ensure smooth connection.
            self.segment_start_frame = frame - 3 if frame > 0 else frame
            # Create new line segment with the next color in our smooth gradient.
            line, = self.ax.plot([], [], linestyle="solid", lw=2, color=self.colors[self.color_index])
            self.lines.append(line)
            self.color_index = (self.color_index + 1) % len(self.colors)

        # When we reach the end of theta, reset for the next cycle.
        if frame >= len(self.theta):
            self.repeat_count += 1
            if self.repeat_count >= self.max_repeats:
                self.anim.event_source.stop()
                self.anim = None
                return self.lines
            frame = 0
            self.last_segment_index = -1
            self.segment_start_frame = 0
            self.lines = []

        # Update only the current segment from segment_start_frame to current frame.
        current_theta = self.theta[self.segment_start_frame:frame]
        x_rotated = self.polar_function_rotated(current_theta) * np.cos(current_theta)
        y_rotated = self.polar_function_rotated(current_theta) * np.sin(current_theta)

        if self.lines:
            self.lines[-1].set_data(x_rotated, y_rotated)
        return self.lines

    def start_animation(self):
        if self.anim is None:
            self.repeat_count = 0
            self.lines = []
            self.color_index = 0
            self.last_segment_index = -1
            self.segment_start_frame = 0
            self.anim = animation.FuncAnimation(
                self.canvas.figure,
                self.update,
                frames=len(self.theta),
                interval=5,
                blit=False,
                repeat=True
            )
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PolarPlotApp()
    window.showMaximized()  # Open the window maximized
    sys.exit(app.exec())
