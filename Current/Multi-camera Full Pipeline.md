
## RGB (1024x1024) encoded, LR (1280x800) encoded, Depth SubP = T

### 2 Cameras
| FPS  | Bandwidth | CPU (LeonOS, LeonRT) |
| ------------- | ------------- | ------------- |
| 20 | 640  | 91, 16 |
| 15  | 660  | 82, 12.5 |
| 10  | 438  | 52, 8.5 |
| 5  | 227  | 27, 4.3 |
| 3  | 141  | 13, 2.5 |
| 1  | 95.7  | 9, 0.6~1.6* |

> NOTE: both 15 and 20 fps runs, there were lots of jumps in bandwidth usage

### 4 Cameras
| FPS  | Bandwidth | CPU (LeonOS, LeonRT) |
| ------------- | ------------- | ------------- |
| 20 | 824  | 80, 12 |
| 15  | 842  | 76, 10 |
| 10  | 841  | 66, 8.5 |
| 5  | 443  | 29, 4.2 |
| 3  | 267  | 14, 2.5 |
| 1  | 140  | 10, 1.5 |	

> NOTE: 15 and 20 fps, lots of jumps in bandwidth usage, timings reflect 10 fps rate


### 8 Cameras
| FPS  | Bandwidth | CPU (LeonOS, LeonRT) |
| ------------- | ------------- | ------------- |
| 10  | 870  | 35:55, 2:6 |
| 5  | 858  | 31:47, 4.5 |
| 3  | 513  | 12:20, 2.55 |
| 1  | 282  | 4:11, 0.6:1.7* |

> NOTE: these runs overall had lots of CPU utilization variations

> bandwidth usage maxed out with 10 fps, timings not consistent with frame rate