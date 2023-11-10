import pandas as pd


# creates a KML formatted placemark with the given coordinate
def placemark(coordinate):
    # uses f-string to insert parameter into string
    return f"""
        <Placemark>
            <styleUrl>#m_red-dot</styleUrl>
                <Point>
                    <altitudeMode>relativeToGround</altitudeMode>
                    <coordinates>{coordinate}</coordinates>
                </Point>
        </Placemark>
    """


class Converter:

    # input csv file
    def __init__(self, csvfile):
        self.csvfile = csvfile

    # converts csv file
    def convert(self, outputfile):
        # create DataFrame out of csv file with columns: Lat, Long, Alt
        df = pd.read_csv(self.csvfile)

        # creates 'coordinates' column in DataFrame through vectorization of longitude, latitude, and altitude
        df['coordinates'] = df['Long'].astype(str) + ',' + df['Lat'].astype(str) + ',' + df['Alt'].astype(str)

        # create/open new KML file to write to.
        with open(outputfile, 'w') as kml_file:
            # write header and style
            kml_file.write("""<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://earth.google.com/kml/2.0">
            <Document>
            <name>Mapped Drone</name>
            <StyleMap id="m_red-dot">
                <Pair>
                    <key>normal</key>
                    <styleUrl>#s_red-dot</styleUrl>
                </Pair>
            </StyleMap>
        <Style id="s_red-dot">
            <IconStyle>
                <color>ff0000ff</color>
                <scale>1.8</scale>
                    <Icon>
                        <href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>
                    </Icon>
            </IconStyle>
        </Style>
        """)

            # iterate through coordinates column, creating a placemark with each one
            for coords in df['coordinates']:
                kml_file.write(placemark(coords))

            # write KML footer
            kml_file.write('</Document>\n</kml>\n')

        return kml_file
