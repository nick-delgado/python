import sys
import fileinput
import pandas as pd


def proto(line):
    result = "*%s\r\n$%s\r\n%s\r\n" % (str(len(line)), str(len(line[0])), line[0])
    for arg in line[1:]:
        result += "$%s\r\n%s\r\n" % (str(len(arg)), arg)
    return result

def parse(filename):
    df = pd.read_csv(filename)
    # ... now df is a dataframe with all the winds data
    #...loop through each row
    for index, row in df.iterrows():
        longitude = row.long
        latitude = row.lat
        jan_json = row.jan
        feb_json = row.feb
        mar_json = row.mar
        apr_json = row.apr
        may_json = row.may
        jun_json = row.jun
        jul_json = row.jul
        aug_json = row.aug
        sep_json = row.sep
        oct_json = row.oct
        nov_json = row.nov
        dec_json = row.dec

        if (float(latitude) < 85.05) and (float(latitude) > -85.05):
            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.jan\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(jan_json.rstrip())), str(jan_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.feb\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(feb_json.rstrip())), str(feb_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.mar\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(mar_json.rstrip())), str(mar_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.apr\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(apr_json.rstrip())), str(apr_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.may\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(may_json.rstrip())), str(may_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.jun\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(jun_json.rstrip())), str(jun_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.jul\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(jul_json.rstrip())), str(jul_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.aug\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(aug_json.rstrip())), str(aug_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.sep\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(sep_json.rstrip())), str(sep_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.oct\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(oct_json.rstrip())), str(oct_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.nov\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(nov_json.rstrip())), str(nov_json.rstrip()))
            sys.stdout.write(redis_proto)

            redis_proto = ""
            redis_proto += "*5\r\n"
            redis_proto += "$6\r\nGEOADD\r\n"
            redis_proto += "$9\r\nwinds.dec\r\n"
            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
            redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
            redis_proto += "${}\r\n{}\r\n".format(str(len(dec_json.rstrip())), str(dec_json.rstrip()))
            sys.stdout.write(redis_proto)

        else:
            if (float(latitude)==-85.0):
                latitude = -85.0512
                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.jan\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(jan_json.rstrip())), str(jan_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.feb\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(feb_json.rstrip())), str(feb_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.mar\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(mar_json.rstrip())), str(mar_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.apr\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(apr_json.rstrip())), str(apr_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.may\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(may_json.rstrip())), str(may_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.jun\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(jun_json.rstrip())), str(jun_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.jul\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(jul_json.rstrip())), str(jul_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.aug\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(aug_json.rstrip())), str(aug_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.sep\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(sep_json.rstrip())), str(sep_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.oct\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(oct_json.rstrip())), str(oct_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.nov\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(nov_json.rstrip())), str(nov_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.dec\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(dec_json.rstrip())), str(dec_json.rstrip()))
                sys.stdout.write(redis_proto)

            if (float(latitude)== 85.0):
                latitude = 85.0510

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.jan\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(jan_json.rstrip())), str(jan_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.feb\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(feb_json.rstrip())), str(feb_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.mar\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(mar_json.rstrip())), str(mar_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.apr\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(apr_json.rstrip())), str(apr_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.may\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(may_json.rstrip())), str(may_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.jun\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(jun_json.rstrip())), str(jun_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.jul\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(jul_json.rstrip())), str(jul_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.aug\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(aug_json.rstrip())), str(aug_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.sep\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(sep_json.rstrip())), str(sep_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.oct\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(oct_json.rstrip())), str(oct_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.nov\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(nov_json.rstrip())), str(nov_json.rstrip()))
                sys.stdout.write(redis_proto)

                redis_proto = ""
                redis_proto += "*5\r\n"
                redis_proto += "$6\r\nGEOADD\r\n"
                redis_proto += "$9\r\nwinds.dec\r\n"
                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
                redis_proto += "${}\r\n{}\r\n".format(len(str(latitude)), str(latitude))
                redis_proto += "${}\r\n{}\r\n".format(str(len(dec_json.rstrip())), str(dec_json.rstrip()))
                sys.stdout.write(redis_proto)



#    file = open(filename)
#    header = file.readline() #Read the first line
#
#    #while (line = file.readline()) :
#    for line in file.readlines():
#        #     '90.0','0.0','{"test":"test"}'
#        delim_1 = line.find(',')
#        longitude = line[:delim_1]
#        delim_2 = line.find(',',delim_1+1)
#
#        latitude = line[delim_1+1:line.find(',',delim_1+1)]
#        json = line[delim_2+1:]
#        #now we need to break the last string
#
#        redis_command = str('GEOADD ') + str(longitude) + " " + str(latitude) +" "+str(json)+  "\n"
#
#        if (float(latitude) < 85.05) and (float(latitude) > -85.05):
#            redis_proto = ""
#            redis_proto += "*5\r\n"
#            redis_proto += "$6\r\nGEOADD\r\n"
#            redis_proto += "$5\r\nwinds\r\n"
#            redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
#            redis_proto += "${}\r\n{}\r\n".format(str(len(latitude)), str(latitude))
#            redis_proto += "${}\r\n{}\r\n".format(str(len(json.rstrip())), str(json.rstrip()))
#            sys.stdout.write(redis_proto)
#
#        else:
#            if (float(latitude)==-85.0):
#                latitude = -85.0512
#                redis_proto = ""
#                redis_proto += "*5\r\n"
#                redis_proto += "$6\r\nGEOADD\r\n"
#                redis_proto += "$5\r\nwinds\r\n"
#                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
#                redis_proto += "${}\r\n{}\r\n".format(str(len(latitude)), str(latitude))
#                redis_proto += "${}\r\n{}\r\n".format(str(len(json.rstrip())), str(json.rstrip()))
#                sys.stdout.write(redis_proto)
#            if (float(latitude)== 85.0):
#                latitude = 85.0510
#
#                redis_proto = ""
#                redis_proto += "*5\r\n"
#                redis_proto += "$6\r\nGEOADD\r\n"
#                redis_proto += "$5\r\nwinds\r\n"
#                redis_proto += "${}\r\n{}\r\n".format(len(str(longitude)), longitude)
#                redis_proto += "${}\r\n{}\r\n".format(str(len(latitude)), str(latitude))
#                redis_proto += "${}\r\n{}\r\n".format(str(len(json.rstrip())), str(json.rstrip()))
#                sys.stdout.write(redis_proto)

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        f = open(filename, 'r')
    except IndexError:
        f = sys.stdin.readlines()

    parse(filename)
#    for line in f:
        #print parse(line.rstrip().split(' ')),
