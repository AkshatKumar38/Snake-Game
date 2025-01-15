import threading
import matplotlib
matplotlib.use('TkAgg') 

import matplotlib.pyplot as plt

class PlotThread:
    def __init__(self):
        self.rewards = []
        self.epsilons = []
        self.avg_q_values = []
        self.lock = threading.Lock()
        self.running = True

    def update_data(self, rewards, epsilons, avg_q_values):
        with self.lock:
            self.rewards = rewards[:]
            self.epsilons = epsilons[:]
            self.avg_q_values = avg_q_values[:]

    def plot(self):
        plt.ion()
        plt.figure(1, figsize=(12, 8))
        while self.running:
            with self.lock:
                if len(self.rewards) > 0:
                    plt.clf()
                    episodes = range(1, len(self.rewards) + 1)

                    # Total rewards
                    plt.subplot(3, 1, 1)
                    plt.plot(episodes, self.rewards, label="Total Reward", color="blue")
                    plt.xlabel("Episodes")
                    plt.ylabel("Total Reward")
                    plt.title("Total Reward Over Episodes")
                    plt.grid(True)
                    plt.legend()

                    # Epsilon values
                    plt.subplot(3, 1, 2)
                    plt.plot(episodes, self.epsilons, label="Epsilon (Exploration Rate)", color="green")
                    plt.xlabel("Episodes")
                    plt.ylabel("Epsilon")
                    plt.title("Exploration Rate Over Episodes")
                    plt.grid(True)
                    plt.legend()

                    # Average Q-values
                    plt.subplot(3, 1, 3)
                    plt.plot(episodes, self.avg_q_values, label="Average Q-Value", color="red")
                    plt.xlabel("Episodes")
                    plt.ylabel("Average Q-Value")
                    plt.title("Average Q-Value Over Episodes")
                    plt.grid(True)
                    plt.legend()

                    plt.tight_layout()
                    plt.pause(0.1)
        plt.close()

    def start(self):
        self.thread = threading.Thread(target=self.plot, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
