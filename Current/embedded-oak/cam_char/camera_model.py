#!/usr/bin/env python3

import os
import sys
import time
import numpy as np

stats = dict()

stats.update({'rgb_1024': {
                            'bw': [13.25, 4.25],
                            'cpu_os': [1.78, 0.96],
                            'cpu_rt': [0.12, 0.05]
                        },                        
            'rgb_2048': {
                            'bw': [40.63, 68.34],
                            'cpu_os': [4.35, 3.29],
                            'cpu_rt': [0.2, -0.03]
                        },
            'rgb_enc_1024': {
                            'bw': [1.94, -0.31],
                            'cpu_os': [1.14, 0.55],
                            'cpu_rt': [0.13, 0.04]
                        },
            'mono_800': {
                            'bw': [16.5, 15.8],
                            'cpu_os': [2.34, 1.79],
                            'cpu_rt': [0.17, 0.14]
                        },
            'mono_enc_800': {
                            'bw': [4.42, 4.75],
                            'cpu_os': [1.6, 1],
                            'cpu_rt': [0.32, 0.05]
                        },
            'depth_sp_800': {
                            'bw': [16.08, 11.39],
                            'cpu_os': [2.48, 1.48],
                            'cpu_rt': [0.31, -0.14]
                        }            
            })

# pipeline = ['rgb_enc_1024']
pipeline = ['rgb_enc_1024', 'mono_800']
# pipeline = ['rgb_enc_1024', 'mono_800', 'depth_sp_800']

if __name__ == '__main__':
    predict_fps = 5
    bw = 0
    cpu_os = 0
    cpu_rt = 0
    
    for node in pipeline:
        if node in stats:
            # calculate bandwidth usage
            equ = np.poly1d(stats[node]['bw'])
            bw += equ(predict_fps)
            # calculate LeonOS usage
            equ = np.poly1d(stats[node]['cpu_os'])
            cpu_os += equ(predict_fps)
            # calculate LeonRT usage
            equ = np.poly1d(stats[node]['cpu_rt'])
            cpu_rt += equ(predict_fps)
    
    print("\n\nPredicted usage:")
    print("Bandwidth:", round(bw), "LeonOS:", round(cpu_os), "LeonRT:", round(cpu_rt) )
    print("\n\n")


