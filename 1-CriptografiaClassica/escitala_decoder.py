import math

file = open("./2020_09_10_12_29_04_marc.monfort.Escitalo", "r")

data = file.read()

def decoder(data, columns):
    rows = math.ceil(len(data)/columns)
    sol = ""

    for i in range(columns):
        for j in range(rows):
            sol = sol + data[j*columns+i]
    return sol


result = open("./solved_escitala.txt", "w")

for i in range(3,len(data)):
    if len(data)%i == 0:
        sol = decoder(data,i)
        if "HAVE" in sol and "MAKE" in sol and "THINK" in sol and "FIND" in sol:
            result.write(sol)
            result.close()
            print("columns = ",i)
            break
