#%%
import random
import time
from os import wait
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import json
import threading
#%%
# fig, ax1 = plt.subplots()
# fig.suptitle('Live Data Plotting', fontsize=20)

# jsonF = [ 
#     { "x": 1, "y": 2 },
#     { "x": 2, "y": 1 },
#     { "x": 3, "y": 12 },
#     { "x": 4, "y": 8 },
#     { "x": 5, "y": 5 },
#     { "x": 6, "y": 15 },
#     { "x": 7, "y": 10 },
#     { "x": 8, "y": 7 },
#     { "x": 9, "y": 20 },
#     { "x": 10, "y": 18 }
# ]
# xs = []
# # ys = [2]

# metrics_values = {
#     'accuracy': [0.1, 0.2, 0.3, 0.4, 0.5],
#     'precision': [0.2, 0.3, 0.4, 0.5, 0.6],
#     'recall': [0.3, 0.4, 0.5, 0.6, 0.7]
# }

# # Function to update the plot
# def animate(i):
#     # Read data from the JSON file
#     #print('hi')
#     # if jsonF: 
#     #     data = jsonF.pop(0)  # Simulate reading from a file    
        
#     #     # Extract x and y values from the list of objects
    
#     #     #xs.append(data['x'])
#     #     ys.append(data['y'])
#     #     #print(xs)
#     #     # Clear the axis and plot the new data
     
#     ax1.clear()

#     ax1.set_xlabel('X-axis')
#     ax1.set_ylabel('Y-axis')
#     ax1.plot(ys)
#     ax1.relim()  # Recalculate limits
#     ax1.autoscale_view()  # Autoscale the view
#     ax1.legend()

# Set up the animation



def update_plot() : 
    style.use('fivethirtyeight')
    ani = animation.FuncAnimation(fig, animate)
    


#Show the plot



   
#%% 
# Example metrics values
# metrics_values = {
#     'accuracy': [0.1, 0.2, 0.3, 0.4, 0.5],
#     'precision': [0.2, 0.3, 0.4, 0.5, 0.6],
#     'recall': [0.3, 0.4, 0.5, 0.6, 0.7]
# }

# # Create the figure and axis
# fig, ax = plt.subplots()
# lines = {}  # Dictionary to store line objects for each metric

# # Function to update the plot
# def update(frame):
#     ax.clear()  # Clear the axis to avoid overlapping lines
#     ax.set_title("Live Metrics Plot")
#     ax.set_xlabel("Iterations")
#     ax.set_ylabel("Values")

#     # Plot each metric dynamically
#     for metric_name, values in metrics_values.items():
#         if metric_name not in lines:
#             # Create a new line for this metric if it doesn't exist
#             lines[metric_name], = ax.plot(range(len(values)), values, label=metric_name)
#         else:
#             # Update the existing line's data
#             lines[metric_name].set_data(range(len(values)), values)

#     ax.relim()  # Recalculate limits
#     ax.autoscale_view()  # Autoscale the view
#     ax.legend()

# # Simulate adding new data to metrics_values
# def simulate_data():
#     metrics_values['accuracy'].append(metrics_values['accuracy'][-1] + 0.1)
#     metrics_values['precision'].append(metrics_values['precision'][-1] + 0.1)
#     metrics_values['recall'].append(metrics_values['recall'][-1] + 0.1)

# # Set up the animation

# # Simulate data updates in the background
# for _ in range(10):
#     simulate_data()
#     print("Simulated new data")
#     time.sleep(5)
#     ani = animation.FuncAnimation(fig, update, frames=100, interval=1000, cache_frame_data=False)
#     plt.show()

# # Show the plot

# %%
ys = [2]
def update_metrics():
    for i in range(10):
        time.sleep(1)
        ys.append(ys[-1] + 1 * random.randint(-10, 10)) 
        # update_plot()
        print("Simulated new data")

def live_metrics_plot():
    fig, ax = plt.subplots()
    #lines = {}
    fig.suptitle('Live Data Plotting', fontsize=20)

    def update(frame):
        ax.clear()
        
        
        ax.plot(ys)

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.relim()  # Recalculate limits
        ax.autoscale_view()  # Autoscale the view
        ax.legend()

        # ax.set_title(f"{self.name} - Metrics")
        # ax.set_xlabel('iterations')
        # ax.set_ylabel('values')
        # ax.legend()
        #plt.tight_layout()
        

    ani = animation.FuncAnimation(fig, update)  # update every 1 sec
    plt.show()
    
if __name__ == "__main__":
    # Simulate data updates in the background
    threading.Thread(target=update_metrics, daemon=True).start()

    # Show plot in main thread
    live_metrics_plot()
# %%
