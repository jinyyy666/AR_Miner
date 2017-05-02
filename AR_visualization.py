import numpy as np

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from nltk.corpus import stopwords


def radar_factory(num_vars, frame='circle'):
    """
    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):
        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
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
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

def plot_group_ranking(group_scores, sorted_group_indices, top_words_list, group_count):
    """
    This function takes in the group rankings, indices, and their corresponding keywords and plots a radar chart and a table
    """
    theta = radar_factory(group_count, frame='polygon')

    key_words_list = generate_key_words(top_words_list)

    columns = ('Rank', 'Group index', 'Score', 'Key words')
    cell_text = []
    for i in xrange(group_count):
        cell_text.append([i + 1, sorted_group_indices[i], group_scores[i], key_words_list[sorted_group_indices[i]]])

    fig = plt.figure()
    fig.set_size_inches(7, 7)
    ax = fig.add_subplot(1, 1, 1, projection='radar')
    ax.set_title('Group scores', weight='bold', size='large', position=(1, 1), horizontalalignment='center', verticalalignment='center')
    ax.plot(theta, group_scores[0:group_count], color='k')
    ax.set_varlabels(sorted_group_indices[0:group_count])
    table = ax.table(cellText=cell_text, colLabels=columns, colWidths = [0.6, 2.0, 3.0, 10.0], loc='bottom', bbox=[0, -0.6, 1.5, 0.5])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    plt.show()

def generate_key_words(top_words_list):
    """
    :param top_words_list: 
    :return: a list of keywords that does not contain stop words
    """
    stop_words = set(stopwords.words('english'))

    key_words_list = []
    for top_words in top_words_list:
        key_words = ''

        for word in top_words:
            if word not in stop_words:
                key_words += ' '
                key_words += word

        key_words_list.append(key_words)

    return key_words_list
