import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


def _radar_factory(num_vars):
    theta = 2*np.pi * np.linspace(0, 1-1./num_vars, num_vars)
    theta += np.pi/2

    def unit_poly_verts(theta):
        x0, y0, r = [0.5] * 3
        verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
        return verts

    class RadarAxes(PolarAxes):
        name = 'radar'
        RESOLUTION = 1

        def fill(self, *args, **kwargs):
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(theta * 180/np.pi, labels)

        def _gen_axes_patch(self):
            verts = unit_poly_verts(theta)
            return plt.Polygon(verts, closed=True, edgecolor='k')

        def _gen_axes_spines(self):
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            verts.append(verts[0])
            path = Path(verts)
            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def radar_graph(labels=[], values=[]):
    N = len(labels)
    theta = _radar_factory(N)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='radar')
    ax.plot(theta, values, color='r')
    ax.set_varlabels(labels)
    #plt.show()
    plt.savefig("radar.png", dpi=100)

labels = ['Space', 'a-z', 'A-Z', 'Numeric', 'Punct.', 'Special']
values = [0.21, 0.00, 0.67, 0.10, 0.02, 0.00]

radar_graph(labels, values)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

string = '32 ND I NTERNATIONAL C OSMIC R AY C ONFERENCE , B EIJING 2011'

num_space = len(re.findall(r'[\s]', string))
num_alpha_lower = len(re.findall(r'[a-z]', string))
num_alpha_upper = len(re.findall(r'[A-Z]', string))
num_numeric = len(re.findall(r'[\d]', string))
num_punct = len(re.findall(r'[\(\).,?:;]', string))
num_special = len(re.findall(r'[^\sa-zA-Z\d\(\).,?:;]', string))

print '%.02f' % (1. * num_space / len(string))
print '%.02f' % (1. * num_alpha_lower / len(string))
print '%.02f' % (1. * num_alpha_upper / len(string))
print '%.02f' % (1. * num_numeric / len(string))
print '%.02f' % (1. * num_punct / len(string))
print '%.02f' % (1. * num_special / len(string))
