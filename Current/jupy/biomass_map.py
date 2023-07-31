# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 10:16:25 2023

@author: skovsen
"""


import numpy as np

import matplotlib.pyplot as plt
import pandas
import utm
from scipy import spatial
import scipy

from sklearn.cluster import AgglomerativeClustering
from matplotlib_scalebar.scalebar import ScaleBar


class LinearNDInterpolatorExt(object):
    def __init__(self, points, values):
        self.funcinterp = scipy.interpolate.LinearNDInterpolator(points, values)
        self.funcnearest = scipy.interpolate.NearestNDInterpolator(points, values)

    def __call__(self, *args):
        t = self.funcinterp(*args)
        u = self.funcnearest(*args)

        t[np.isnan(t)] = u[np.isnan(t)]
        return t
    
    
data= pandas.read_csv('arg_max_summary_hvcam_median_filtered_for_priya3.csv', sep=';')


#N_samples = 2000
im_size = 5328.*4608.
min_points_per_cluster = 50


coordinateUTM = utm.from_latlon(data['latitude'].to_numpy(),data['longitude'].to_numpy())

x = coordinateUTM[0]#[0:N_samples]

y = coordinateUTM[1]#[0:N_samples]

z = data['live_biomass_pixels'].to_numpy()/im_size
#z = data['residue_pixels'].to_numpy()/im_size
    
X = np.vstack((x, y)).T
print(X.shape)
#clust = OPTICS(min_samples=50, xi=0.5, min_cluster_size=0.05)
#clust.fit(X)


    
    
clust = AgglomerativeClustering(n_clusters=None, distance_threshold=40, linkage='single').fit(X)
clust.labels_
num_clusters = np.max(clust.labels_)
print(np.sum(clust.labels_ == -1))
for clusterId in range(num_clusters+1):
    print(np.sum(clust.labels_ == clusterId))
    if(np.sum(clust.labels_ == clusterId) > min_points_per_cluster): #only process if more than 30 image samples is part of the cluster
        xk = x[clust.labels_ == clusterId]
        yk = y[clust.labels_ == clusterId]
        zk = z[clust.labels_ == clusterId]
        
        resolution = 5  # grid is 5 x 5 meters per cell
        X_grid_lin = np.arange(min(xk)-5, max(xk)+5, step=resolution)
        Y_grid_lin = np.arange(min(yk)-5, max(yk)+5, step=resolution)
    
        X_grid, Y_grid = np.meshgrid(X_grid_lin, Y_grid_lin)  # 2D grid for interpolation
        
       
        mesh_flat_dim = len(X_grid_lin)*len(Y_grid_lin)
        
        a = np.reshape(X_grid, mesh_flat_dim)
        b = np.reshape(Y_grid, mesh_flat_dim)
        ab = np.vstack((a,b)).T
        
        distance,index = spatial.KDTree(np.vstack((xk,yk)).T).query(ab)
        
        X_grid_closest_point = np.reshape(distance, (len(Y_grid_lin),len(X_grid_lin)))
        Y_grid_closest_point = np.reshape(distance, (len(X_grid_lin),len(Y_grid_lin)))

        interp = LinearNDInterpolatorExt(list(zip(xk, yk)), zk)
    
    
        
        X_grid_masked = X_grid
        Y_grid_masked = Y_grid
        Z_grid_masked = interp(X_grid_masked, Y_grid_masked)
        Z_grid_masked[X_grid_closest_point>12]=np.nan
        
    
        plt.magma()
        plt.pcolormesh(X_grid_masked, Y_grid_masked, Z_grid_masked, shading='auto')
        
        plt.clim(0, 1)  # manually setup the range of the colorscale and colorbar
    
        plt.plot(xk, yk, color='green', marker='o', label="input point", markersize=0.8, linestyle="None")
        #ax = nybb.plot()
        ax = plt.gca()
        ax.add_artist(ScaleBar(resolution))
        #plt.legend()
    
        #plt.colorbar()
        from matplotlib.ticker import FuncFormatter

        fmt = lambda x, pos: '{:.0%}'.format(x)
        cbar = plt.colorbar(format=FuncFormatter(fmt))

        plt.title('Live plant matter coverage')
    
        plt.axis("equal")
        plt.axis('off')
    
       # plt.show()
        plt.savefig("map_" + str(clusterId) + ".png", bbox_inches='tight', dpi=300)
        plt.show()
        plt.clf()
    