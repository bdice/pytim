# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
""" Module: test_observables
    ========================
"""


class TestObservables():
    """
    This is a collection of basic tests to check
    that the observables are yelding the expected
    result.

    >>> # OBSERVABLES TEST: 1
    >>> import MDAnalysis as mda
    >>> import pytim
    >>> from pytim import observables
    >>> from pytim.datafiles import *
    >>> import numpy as np
    >>> u = mda.Universe(_TEST_ORIENTATION_GRO)
    >>> o = observables.Orientation(u,options='molecular')
    >>> np.set_printoptions(precision=3)

    >>> print(o.compute(u.atoms).flatten())
    [ 1.     0.     0.     0.     1.     0.     0.    -0.707 -0.707]

    >>> np.set_printoptions()

    >>> # OBSERVABLES TEST: 2
    >>> u=mda.Universe(_TEST_PROFILE_GRO)
    >>> o=observables.Number()
    >>> p=observables.Profile(direction='x',observable=o)
    >>> p.sample(u.atoms)
    >>> low,up,avg =  p.get_values(binwidth=1.0)
    >>> print(low[0:3])
    [ 0.  1.  2.]
    >>> print(avg[0:3])
    [ 0.01  0.02  0.03]

    >>> # CORRELATOR TEST
    >>> from pytim.utilities import correlate
    >>> a = np.array([1.,0.,1.,0.,1.])
    >>> b = np.array([0.,2.,0.,1.,0.])
    >>> corr = correlate(b,a)
    >>> ['{:.2f}'.format(i) for i in corr]
    ['-0.00', '0.75', '0.00', '0.75', '0.00']


    >>> corr = correlate(b)
    >>> ['{:.2f}'.format(i) for i in corr]
    ['1.00', '0.00', '0.67', '-0.00', '0.00']

    >>> # PROFILE EXTENDED TEST: checks trajectory averaging
    >>> # and consistency in summing up layers  contributions
    >>> import numpy as np
    >>> import MDAnalysis as mda
    >>> import pytim
    >>> from   pytim.datafiles import *
    >>> from   pytim.observables import Profile
    >>> u = mda.Universe(WATER_GRO,WATER_XTC)
    >>> g=u.select_atoms('name OW')
    >>> inter = pytim.ITIM(u,group=g,max_layers=4,centered=True, molecular=False)
    >>>
    >>> Layers=[]
    >>>
    >>> for n in np.arange(0,5):
    ...     Layers.append(Profile())
    >>> Val=[]
    >>> for ts in u.trajectory[:4]:
    ...     for n in range(len(Layers)):
    ...         if n == 0:
    ...             group = g
    ...         else:
    ...             group = u.atoms[u.atoms.layers == n]
    ...         Layers[n].sample(group)
    >>> for L in Layers:
    ...     Val.append(L.get_values(binwidth=2.0)[2])
    >>>

    >>> print np.round(np.sum(np.array(Val[0]) * np.prod(u.dimensions[:3])) / len(Val[0]),decimals=0)
    4000.0

    >>> # the sum of the layers' contribution is expected to add up only close
    >>> # to the surface
    >>> print not np.sum(np.abs(np.sum(Val[1:],axis=0)[47:] - Val[0][47:])>1e-15)
    True


    """

    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
