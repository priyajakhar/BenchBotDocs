### Test Data

**Camera Orientation**

* x is up and down (yaw)
* y is along the length of the camera (pitch)
* z is along front and back of camera (roll)


| Run     |    0   |   90   |   180  |  270   |  360   |
|  :----: | :----: | :----: | :----: | :----: | :----: |
| 2 | 130 | 260 | 340 | 10  | 180 |
| 3 | 200 | 280 | 330 | 5   | 240 |
| 4 | 240 | 300 | 0   | 40  | 218 |

Run 1 was done without any regards for angle changes so observation of values at each checkpoint do not exist.

Run 2, 3 and 4 were all done in same manner. For Runs 1-4, the camera was held in the same position on the truck.

Run 5 and 6 were done in a different position (one side of the truck).

Run 5 was not done for entire round of truck, was stopped much earlier because values were not changing much.

Run 6 was done for an entire round to confirm the effect being observed for Run 5.

It seems to be a case of interference.

<br>
<br>

> math.atan2: sequence of values in division matters

> The returned value is between PI and -PI