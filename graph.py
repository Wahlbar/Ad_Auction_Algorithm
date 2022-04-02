import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        return


    # //TODO: Use seaborn, label and
    def drawAdPerSexHistogram(self, retailAdsMale, retailAdsFemale, economicAdsMale, economicAdsFemale):
        labels = ['retail ads - male users', 'retail ads - female users', 'economic ads - male users', 'economic ads - female users']
        width = 14
        height = 8
        colors = ['darkblue', 'darkorange', 'blue', 'orange']
        fig, ax = plt.subplots(figsize=(width, height))
        ax.bar(labels, [retailAdsMale, retailAdsFemale, economicAdsMale, economicAdsFemale], color = colors )
        plt.show()

    # // TODO: todo
    def drawRevenueRatio(self):
        return