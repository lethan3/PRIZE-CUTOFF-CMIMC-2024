import argparse
import random




def generate_random(n: int) -> list:
    file = open("solutions/random.txt", "w")
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0: instruction = f"{i},{j} "+random.choice([str(i) for i in range(n)]+["_"])+","+random.choice([str(i) for i in range(n)]+["_"])+","+random.choice(["_"])+","+random.choice(["U","D","L","R"])
            else: instruction = f"{i},{j} "+random.choice([str(i) for i in range(n)]+["_"])+","+random.choice([str(i) for i in range(n)]+["_"])+","+random.choice(["U","D","L","R","_"])+","+random.choice(["U","D","L","R","_"])
            file.write(instruction+"\n")
    file.close()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate a random instruction list")

    parser.add_argument("--n", "-n", type=int, default=5)
    generate_random(parser.parse_args().n)

    