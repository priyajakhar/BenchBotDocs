import asyncio
from motor_controller_y import MotorControllerY

y_motor_control = MotorControllerY()

async def move_y_axis(dist):
    
    for i in range(2):
        print(f"Iteration: {i+1}, Distance: {(i+1)*0.5} m")
        await y_motor_control.move_y(float(dist))
        await y_motor_control.hold_motors(time_s=5)


if __name__ == "__main__":
    asyncio.run(move_y_axis(50))