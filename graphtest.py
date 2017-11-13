import matplotlib.pyplot as plot

fig = plot.figure(figsize=(8,8))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
pie_chart = ax.pie([10, 20, 30, 40])
fig.savefig("piechart.png")
