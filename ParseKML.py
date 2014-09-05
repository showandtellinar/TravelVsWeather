__author__ = 'Danny Brady'
import sys
import getopt
import re


def main(argv):
    help = "ParseKML.py -i <kml file path> -o <output file path>"
    in_file = ""
    out_file = ""

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["infile=", "outfile="])
    except getopt.GetoptError:
        print help
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print help
            sys.exit(1)
        elif opt in ('-i', '--infile'):
            in_file = arg
        elif opt in ('-o', '--outfile'):
            out_file = arg

    if in_file == "" or out_file == "":
        print help
        sys.exit(1)

    print "KML input file is:", in_file
    print "Output file(csv) is:", out_file

    last_time = None
    line_counter = 0
    with open(out_file, "w") as d:
        d.write("datetime,long,lat\n")
        with open(in_file) as f:
            lines = f.readlines()
            for line in lines:
                #print line
                dt_m = re.match(r"<when>(?P<datetime>.*?)</when>", line)
                if dt_m is not None:
                    last_time = dt_m.group("datetime")
                    continue
                coor_m = re.match(r"<gx:coord>(?P<long>.*?) (?P<lat>.*?) .*</gx:coord>", line)
                if coor_m is not None:
                    d.write("{},{},{}\n".format(last_time, coor_m.group("long"), coor_m.group("lat")))
                    line_counter += 1
                    continue

    print "Wrote {} lines to file".format(line_counter)

if __name__ == "__main__":
    main(sys.argv[1:])