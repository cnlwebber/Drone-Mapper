import pandas as pd
import re


class TrackConverter:

    # input csv file, create string to hold when and where of track element.
    def __init__(self, csvfile):
        self.csvfile = csvfile
        self.stringlist = []

    # converts csv file
    def convert(self, outputfile, header, t_format):
        # create DataFrame out of csv file with columns: Lat, Long, Alt
        df = pd.read_csv(self.csvfile)

        # creates 'coordinates' column in DataFrame through vectorization of longitude, latitude, and altitude
        df['coordinates'] = df['Long'].astype(str) + ',' + df['Lat'].astype(str) + ',' + df['Alt'].astype(str)

        # create/open new KML file to write to.
        with open(outputfile, 'w') as kml_file:

            kml_file.write(header + "\n<!-- Beginning of Track -->\n")

            # iterate through time column, adding when values to string list
            for when in df['Time']:
                self.stringlist.append("<when>" + when + "</when>")

            # iterate through coordinates column, adding coords to string list
            for coords in df['coordinates']:
                self.stringlist.append("<gx:coord>" + coords + "</gx:coord>")

            # write to kml file the formatted gx:track by joining string list into single string
            kml_file.write(track('\n'.join(self.stringlist).strip(), t_format))

            # write KML footer
            kml_file.write('\n    </Document>\n</kml>\n')

        return kml_file


def track(the_data, the_t_format):
    # search for </gx:Track>, split the string there, count the whitespace, then insert the data before
    # with the correct leading whitespace
    line_split = re.search(r"(\s*)(<gx:Track>.*)", the_t_format)
    whitespace = len(line_split.group(1))
    lines = the_data.splitlines()
    modified_lines = [(whitespace + 6) * " " + line for line in lines]
    modified_string = "\n".join(modified_lines)
    str_list = re.split(r"(</gx:Track>.*)", the_t_format, 1)
    str_list[0] = str_list[0].rstrip()
    str_list[1] = whitespace * " " + "  " + str_list[1]
    str_list.insert(1, "\n{element}\n")
    return ''.join(str_list).format(element=modified_string)


# For Matt's requirements:
#
# Take the gx:Track created in this script, then add it to a multitrack.
# The multitrack will contain separate "gx:Tracks" that are actually just single place marks
# In theory, the multitrack should be able to show the perfect gx:Track line, and the place marks of a second data set
#