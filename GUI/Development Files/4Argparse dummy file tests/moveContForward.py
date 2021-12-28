import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s')
parser.add_argument('-t')
args = parser.parse_args()

print("Move continuously forward")
print("Speed is " + args.s + " and time duration is " + args.t)