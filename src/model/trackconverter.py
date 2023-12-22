import pandas as pd


# creates a KML formatted gx:track with the given coordinate
def track(data):
    # uses f-string to insert data into string
    # PASTE THE FORMATTING FOR THE GX:TRACK HERE
    return f"""
<Folder>
  <Placemark>
    <gx:Track>
        <altitudeMode>relativeToGround</altitudeMode>
        {data}
    </gx:Track>
  </Placemark>
</Folder>
</kml>
    """


class TrackConverter:

    # input csv file, create string to hold when and where of track element.
    def __init__(self, csvfile):
        self.csvfile = csvfile
        self.stringlist = []

    # converts csv file
    def convert(self, outputfile):
        # create DataFrame out of csv file with columns: Lat, Long, Alt
        df = pd.read_csv(self.csvfile)

        # creates 'coordinates' column in DataFrame through vectorization of longitude, latitude, and altitude
        df['coordinates'] = df['Long'].astype(str) + ',' + df['Lat'].astype(str) + ',' + df['Alt'].astype(str)

        # create/open new KML file to write to.
        with open(outputfile, 'w') as kml_file:


            # PASTE HEADER HERE
            # PASTE HEADER HERE
            kml_file.write("""
        """)
            # PASTE HEADER HERE
            # PASTE HEADER HERE

            # iterate through time column, adding when values to string list
            for when in df['Time']:
                self.stringlist.append("        <when>" + when + "</when>")

            # iterate through coordinates column, adding coords to string list
            for coords in df['coordinates']:
                self.stringlist.append("        <gx:coord>" + coords + "</gx:coord>")

            # write to kml file the formatted gx:track by joining string list into single string
            kml_file.write(track('\n'.join(self.stringlist).strip()))

            # write KML footer
            kml_file.write('</Document>\n</kml>\n')

        return kml_file
