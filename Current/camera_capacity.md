# Camera Mathematical Model


| Node              | Bandwidth Utilization |
| :---------------- | :------ |
| RGB 1024x1024        |   13.25*FPS + 4.25   |
| RGB 2048x2048           |   40.63*FPS + 68.34   |
| RGB 1024x1024 encoded    |  1.94*FPS - 0.31   |
| LR 1280x800 |  16.5*FPS + 15.8   |
| LR 1280x800 encoded |  4.42*FPS + 4.75   |
| Depth 1280x800 |  16.08*FPS + 11.39   |

- Base bandwidth deduction when combining nodes is (1.42*FPS + 0.91).
- 2048x2048 resolution is 4x more pixels than 1024x1024, as such the bandwidth utilization also becomes approx 4x.
- Encoding 1024x1024 RGB takes about 8x less bandwidth.
