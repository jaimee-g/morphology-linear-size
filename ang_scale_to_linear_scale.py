#converting redshift to distance, and finding linear scale from angular scale of 3c336 and 3c310

from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

# Define cosmology, find ref for plank most recent for cosmo values 
cosmo = FlatLambdaCDM(H0=67.7, Om0=0.310)

# Colourblind-friendly palette
colors = {
'yellow': (255/255, 176/255, 0/255),
'orange': (254/255, 97/255, 0/255),
'pink': (220/255, 38/255, 127/255),
'purple': (120/255, 94/255, 240/255),
'blue': (100/255, 143/255, 255/255)
}

#dictionary of source and FR classification
fr_classification = {
    "3C336": "FR2",
    "3C310": "FR1",
    "3C123": "FR2",
    "3C263": "FR2",
    "3C31": "FR1",
    "3C465": "FR1",
    "3C175": "FR2",
    "3C264": "FR1",
    "3C66B": "FR1",
    "3C207": "FR2",
    "3C296": "FR1",
    "3C83.1B": "FR1"
}

#dictionary of redshifts for all sources (3sf)
redshifts = {
    "3C336": 0.927,
    "3C310": 0.0540,
    "3C123": 0.218,
    "3C263": 0.646,
    "3C31": 0.0167,
    "3C465": 0.0293,
    "3C175": 0.768,
    "3C264": 0.0208,
    "3C66B": 0.0215,
    "3C207": 0.684,
    "3C296": 0.0237,
    "3C83.1B": 0.0255
}

#dictionary of length of sources in arcsec, need to find lengths (3sf)
ang_scale = {
    "3C336": 21.30 * u.arcsec, #didnt use new method, a lot of noise around the sourcec so unsure
    "3C310": (6.48 * 60) * u.arcsec, #updated using new method, 5.45 arcmin old value
    "3C123": 19.75 * u.arcsec, #didnt use new method, a lot of noise around the sourcec so unsure
    "3C263": 46.03 * u.arcsec, #didnt use new method, a lot of noise around the sourcec so unsure
    "3C31": (48.76 * 60) * u.arcsec, #contour and rms applied, but this is a wide angle tail RG
    "3C465": (10.42 * 60) * u.arcsec, #contour and rms applied, but this is a wide angle tail RG
    "3C175": 45.14 * u.arcsec, #didnt use new method, a lot of noise around the sourcec so unsure
    "3C264": (15.52 * 60) * u.arcsec, #contour and rms applied, but this is a wide angle tail RG
    "3C66B": (13.08 * 60) * u.arcsec, #used new method, old value 12.10
    "3C207": 40.13 * u.arcsec, #didnt use new method, a lot of noise around the sourcec so unsure
    "3C296": (7.77 * 60) * u.arcsec, #used new method, old value 7.20
    "3C83.1B": (17.25 * 60) * u.arcsec #contour and rms applied, but this is a wide angle tail RG
}

#loop across all sources to find angular diameter distance and linear size

linear_size_dict = {}

for source in redshifts.keys():
    # Angular diameter distance
    ang_diam = cosmo.angular_diameter_distance(redshifts[source]) # in Mpc

    #length
    theta = ang_scale[source]

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

#dictionary of source and linear size values 
print(linear_size_dict)

#dictionary of source and linear size values 

#split linear_size_dict into two dictionaries based on FR classification
fr1_linear_size = {source: size for source, size in linear_size_dict.items() if fr_classification[source] == "FR1"}
fr2_linear_size = {source: size for source, size in linear_size_dict.items() if fr_classification[source] == "FR2"}

#print("FR1 linear sizes:", fr1_linear_size)
#print("FR2 linear sizes:", fr2_linear_size)

#boxplot of linear sizez for fr1,fr2 and all sources

# Data
all_linear_sizes = np.array(list(linear_size_dict.values()))
fr1_linear_sizes = np.array(list(fr1_linear_size.values()))
fr2_linear_sizes = np.array(list(fr2_linear_size.values()))

data = [fr1_linear_sizes, fr2_linear_sizes, all_linear_sizes]
fig, ax = plt.subplots(figsize=(7, 5))

# Create boxplot
bp = ax.boxplot(data,labels=['FR I', 'FR II', 'All Sources'],patch_artist=True,showfliers=False,widths=0.6)

# Colour boxes
box_colors = [colors['blue'], colors['pink'], colors['orange']]
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)

# Style lines
for median in bp['medians']:
    median.set(color='black', linewidth=2)

for whisker in bp['whiskers']:
    whisker.set(color='black')

for cap in bp['caps']:
    cap.set(color='black')

# Overlay individual data points
for i, group in enumerate(data, start=1):

    # Add random horizontal jitter
    x = np.random.normal(i, 0.04, size=len(group))

    ax.scatter(x, group, facecolors='white', edgecolors='black', s=70, linewidth=1.2, alpha=0.9, zorder=3)

ax.set_ylabel('Projected Linear Size (kpc)')
ax.set_title('Projected Linear Sizes of FR I and FR II Sources')
ax.grid(axis='y', alpha=0.25)

plt.tight_layout()
plt.show()

#histogram plot


"""""
#plot histogram of linear sizes for Fr1 and FR2 sources on the same plot, with diff colours 
bins = np.linspace(min(linear_size_dict.values()),
max(linear_size_dict.values()),6)

plt.hist([list(fr1_linear_size.values()), list(fr2_linear_size.values()),list(linear_size_dict.values())], bins=bins, color=['blue', 'orange', 'green'], label=['FR1', 'FR2', 'All Sources'], alpha=0.7)
plt.xlabel('Linear Size (kpc)')
plt.ylabel('Frequency')
plt.title('Histogram of Linear Sizes')
plt.legend()
plt.show()
"""

#boxplot?
"""""
fr1 = np.array(list(fr1_linear_size.values()))
fr2 = np.array(list(fr2_linear_size.values()))

data = [fr1, fr2]

fig, ax = plt.subplots(figsize=(7, 5))

box = ax.boxplot(data, labels=[f'FR I\n(n={len(fr1)})', f'FR II\n(n={len(fr2)})'], patch_artist=True, widths=0.5, showmeans=True, meanprops={'marker': 'D','markerfacecolor': 'white','markeredgecolor': 'black','markersize': 6}, medianprops={'color': 'black','linewidth': 2})

# Colour the boxes
colours = ['royalblue', 'darkorange']

for patch, colour in zip(box['boxes'], colours):
    patch.set_facecolor(colour)
    patch.set_alpha(0.45)

# Overlay all individual sources with slight horizontal jitter
rng = np.random.default_rng(42)

for position, values, colour in zip([1, 2], data, colours):
    jitter = rng.normal(0, 0.045, size=len(values))

    ax.scatter(
    position + jitter,values,color=colour,edgecolor='black',s=55,zorder=3)

ax.set_ylabel('Projected Linear Size (kpc)')
ax.set_xlabel('Radio Morphology')
ax.set_title('Projected Linear Sizes of FR I and FR II Sources')
ax.grid(axis='y', alpha=0.25)


plt.tight_layout()
plt.show()
"""

#dot plot
"""""
fr1 = list(fr1_linear_size.values())
fr2 = list(fr2_linear_size.values())

plt.figure(figsize=(8,3))

plt.scatter(fr1, np.ones(len(fr1)), color='blue', s=80, label='FR I')

plt.scatter(fr2, np.ones(len(fr2))*2, color='orange', s=80, label='FR II')

plt.yticks([1,2], ['FR I', 'FR II'])
plt.xlabel('Linear Size (kpc)')
plt.title('Linear Sizes of Sample Sources')
plt.legend()
plt.tight_layout()
plt.show()
"""

#previous work for 3C336 and 3C310, to check if the new method is working correctly
"""""

# Angular diameter distance
ang_diam_3c336 = cosmo.angular_diameter_distance(redshifts["3C336"]) # in Mpc
ang_diam_3c310 = cosmo.angular_diameter_distance(redshifts["3C310"]) # in Mpc

#length
theta_3c310 = ang_scale["3C310"]
theta_3c336 = ang_scale["3C336"]

#linear size
linear_3c310 = theta_3c310.to(u.radian).value * ang_diam_3c310.to(u.kpc)
linear_3c336 = theta_3c336.to(u.radian).value * ang_diam_3c336.to(u.kpc)

#printing results
print("3C310:")
print("  DA =", ang_diam_3c310)
print("  Linear size =", linear_3c310.to(u.kpc))

print("\n3C336:")
print("  DA =", ang_diam_3c336)
print("  Linear size =", linear_3c336.to(u.kpc))
"""
