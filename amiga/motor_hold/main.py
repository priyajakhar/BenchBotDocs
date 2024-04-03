import asyncio
from motor_controller_y import MotorControllerY

y_motor_control = MotorControllerY()

async def move_y_axis(dist):
    for i in range(3):
        await y_motor_control.move_y(float(dist))
        await y_motor_control.hold_motors(time_s=2)

if __name__ == "__main__":
    asyncio.run(move_y_axis(50))