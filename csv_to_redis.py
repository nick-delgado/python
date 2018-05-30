import sys
import fileinput


def proto(line):
    result = "*%s\r\n$%s\r\n%s\r\n" % (str(len(line)), str(len(line[0])), line[0])
    for arg in line[1:]:
        result += "$%s\r\n%s\r\n" % (str(len(arg)), arg)
    return result

def parse(filename):
    file = open(filename)
    header = file.readline() #Read the first line

    #while (line = file.readline()) :
    for line in file.readlines():
        #     '90.0','0.0','{"test":"test"}'
        delim_1 = line.find(',')
        longitude = line[:delim_1]
        delim_2 = line.find(',',delim_1+1)

        latitude = line[delim_1+1:line.find(',',delim_1+1)]
        json = line[delim_2+1:]

        redis_command = str('GEOADD ') + str(longitude) + " " + str(latitude) +" "+str(json)+  "\n"

        if (float(latitude) < 85.05) and (float(latitude) > -85.05):
            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$5\r\nwinds\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(str(len(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(json.rstrip())), str(json.rstrip()))
            sys.stdout.write(redis_proto)

        else:
            if (float(latitude)==-85.0):
                latitude = -85.0512
                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$5\r\nwinds\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(str(len(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(json.rstrip())), str(json.rstrip()))
                sys.stdout.write(redis_proto)
            if (float(latitude)== 85.0):
                latitude = 85.0510

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$5\r\nwinds\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(str(len(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(json.rstrip())), str(json.rstrip()))
                sys.stdout.write(redis_proto)

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        f = open(filename, 'r')
    except IndexError:
        f = sys.stdin.readlines()

    parse(filename)
#    for line in f:
        #print parse(line.rstrip().split(' ')),
