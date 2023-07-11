
## RGB + LR + Depth

### RGB (1024x1024) unencoded, LR (1280x800), Depth (1280x800) SubP = T
| FPS  | Bandwidth | CPU (LeonOS, LeonRT) |
| ------------- | ------------- | ------------- |
| 20 | 610~660'  | 99.99, 10.5 |
| 15  | 638~645  | 94.5, 10 |
| 10  | 427~435  | 57, 6.4 |
| 5  | 195~235"  | 29, 3.2 |
| 3  | 110~155"  | 17.5, 1.95 |
| 1  | 60~85  | 12.5, 0.75* |			


### RGB (1024x1024) encoded, LR (1280x800), Depth (1280x800) SubP = T
| FPS  | Bandwidth | CPU (LeonOS, LeonRT) |
| ------------- | ------------- | ------------- |
| 20 | 555~565  | 99.99, 13 |
| 15  | 505~515  | 79, 10.5 |
| 10  | 320~353  | 50, 6.5 |
| 5  | 150~195  | 25.5, 3.3 |
| 3  | 75~115"  | 15.5, 2 |
| 1  | 45~51  | 5.5~10.5, 0.8* |	
*lot of CPU variations
'various uncharacteristic up/down spikes
"jumps between extremes only