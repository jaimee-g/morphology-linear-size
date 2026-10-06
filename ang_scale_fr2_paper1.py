#converting redshift to distance, and finding linear scale from angular scale of 3c336 and 3c310

from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

# Define cosmology for Planck 2018 values, https://arxiv.org/abs/1807.06209
cosmo = FlatLambdaCDM(H0=67.4, Om0=0.315)

# Colourblind-friendly palette
colors = {
'yellow': (255/255, 176/255, 0/255),
'orange': (254/255, 97/255, 0/255),
'pink': (220/255, 38/255, 127/255),
'purple': (120/255, 94/255, 240/255),
'blue': (100/255, 143/255, 255/255)
}

#FR2 sources
fr_classification = {
    "3C336": "FR2",
    "3C123": "FR2",
    "3C263": "FR2",
    "3C207": "FR2"
}

#redshifts of selected sources 
redshifts = {
    "3C336": 0.927,
    "3C123": 0.218,
    "3C263": 0.646,
    "3C207": 0.684
}

#ang scale values of selected sources in arcsecs, full extent NOT peak to peak values
ang_scales = {
    "3C336": 41.64 * u.arcsec,
    "3C123": 52.81 * u.arcsec,
    "3C263": (1.07 * 60) * u.arcsec,
    "3C207": 34.60 * u.arcsec
}

linear_size_dict = {}

for source in redshifts.keys():
    # Angular diameter distance
    ang_diam = cosmo.angular_diameter_distance(redshifts[source]) # in Mpc

    #length
    theta = ang_scales[source]

    #linear size
    linear_size = theta.to(u.radian).value * ang_diam.to(u.kpc)
    if linear_size == 0:
        pass
    else:   
    #printing results

        print(f"{source}:")
        print("  DA =", ang_diam)
        print("  Linear size =", linear_size.to(u.kpc))
        linear_size_dict[source] = linear_size.value
