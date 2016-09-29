# -*- coding:utf-8 -*-

from pylab import *

def perceptron():
    data = np.random.rand(100, 2)
    xdata = data[::, 0]
    ydata = data[::, 1]

    bdown = []
    bup = []
    max_xdata = max(xdata)
    min_xdata = min(xdata)
    max_ydata = max(ydata)
    min_ydata = min(ydata)
    k = (min_ydata - max_ydata)/(max_xdata - min_xdata)
    b = (min_ydata * min_xdata + max_xdata * max_ydata)/(max_xdata - min_xdata)

    bup = data.dot(np.array([k* -1 , 1])) > b
    bdown = data.dot(np.array([k* -1 , 1])) < b
    xline = [max(xdata), min(xdata)]
    yline = [min(ydata), max(ydata)]

    plot(xline, yline, color='green')
    scatter(xdata[bup], ydata[bup], marker='+', color='red')
    scatter(xdata[bdown], ydata[bdown], marker='*', color='black')

    xlim(min(xdata) - 0.1, max(xdata) + 0.5)
    ylim(min(ydata) - 0.1, max(ydata) + 0.5)
    ax = gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    annotate(r'$w\cdot x + b= 0$', xy = (max(xdata), min(ydata)), xycoords='data')

    show()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("wrong arg")
        sys.exit(-1)

    method = sys.argv[1]

    if method == 'perceptron':
        perceptron()