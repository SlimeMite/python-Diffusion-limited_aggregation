import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class ArrayVisualizer:
    def __init__(self, data: np.ndarray, mask: np.ndarray):
        if data.shape != mask.shape:
            raise ValueError("Data and mask arrays must have the same shape")
        self.data = data
        self.mask = mask
        self.fig, self.ax = plt.subplots()
        self.image = None

    def create_plot(self):
        plt.ion()
        cmap = plt.cm.RdYlGn_r  # Reverse RdYlGn for green (low) to red (high)
        norm = None

        # Determine min and max values ignoring zeros
        nonzero_values = self.data[(self.data != 0) & (~self.mask)]
        if nonzero_values.size > 0:
            vmin, vmax = np.min(nonzero_values), np.max(nonzero_values)
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

        # Create an RGBA image
        colored_data = np.zeros((*self.data.shape, 4))  # RGBA format

        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                if self.mask[i, j]:
                    colored_data[i, j] = [0, 0, 0, 1]  # Black for masked positions
                elif self.data[i, j] == 0:
                    colored_data[i, j] = [1, 1, 1, 0]  # Transparent for zero
                else:
                    color = cmap(norm(self.data[i, j])) if norm else [1, 1, 1, 0]
                    colored_data[i, j] = color

        if self.image is None:
            self.image = self.ax.imshow(colored_data, interpolation='nearest')
        else:
            self.image.set_data(colored_data)

        self.ax.axis('off')
        self.fig.canvas.draw_idle()
        plt.show(block=False)


    def update_plot(self, new_data: np.ndarray, new_mask: np.ndarray):
        if new_data.shape != new_mask.shape:
            raise ValueError("New data and mask must have the same shape")
        self.data = new_data
        self.mask = new_mask
        self.create_plot()

    def remove_plot(self):
        plt.close(self.fig)
        plt.ioff()  # Disable interactive mode

    def update_display(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


if __name__ == "__main__":
    # Example usage
    data = np.array([[0, 1, 2], [3, 4, 0], [5, 6, 7]])
    mask = np.array([[False, False, True], [False, True, False], [False, False, False]])
    visualizer = ArrayVisualizer(data, mask)
    visualizer.create_plot()