#!/usr/local/opt/python/bin/python2.7
"""Returns distance in meters between two geohashes."""
from math import radians, cos, sin, asin, sqrt


class GeohashDelta():
    """Use the Haversine equation to calculate delta in meters."""

    #  Note: the alphabet in geohash differs from the common base32
    #  alphabet described in IETF's RFC 4648
    #  (http://tools.ietf.org/html/rfc4648)
    __base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    __decodemap = {}

    def __init__(self, hash1, hash2):
        """."""
        for i in range(len(self.__base32)):
            self.__decodemap[self.__base32[i]] = i
        lat1, lon1, lat_err1, lon_err1 = self.__decode(hash1)
        lat2, lon2, lat_err2, lon_err2 = self.__decode(hash2)
        print self.__haversine(lat1, lon1, lat2, lon2)

    def __decode(self, geohash):
        """Decode the geohash to values plus error margins."""
        # Returns four floats: lat, lon, lat err, lon err
        lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
        lat_err, lon_err = 90.0, 180.0
        is_even = True
        for c in geohash:
            cd = self.__decodemap[c]
            for mask in [16, 8, 4, 2, 1]:
                if is_even:  # adds longitude info
                    lon_err /= 2
                    if cd & mask:
                        lon_interval = ((lon_interval[0] + lon_interval[1])/2,
                                        lon_interval[1])
                    else:
                        lon_interval = (lon_interval[0], (lon_interval[0] +
                                        lon_interval[1])/2)
                else:  # adds latitude info
                    lat_err /= 2
                    if cd & mask:
                        lat_interval = ((lat_interval[0] + lat_interval[1])/2,
                                        lat_interval[1])
                    else:
                        lat_interval = (lat_interval[0], (lat_interval[0] +
                                        lat_interval[1])/2)
                is_even = not is_even
        lat = (lat_interval[0] + lat_interval[1]) / 2
        lon = (lon_interval[0] + lon_interval[1]) / 2
        return lat, lon, lat_err, lon_err

    def __haversine(self, lat1, lon1, lat2, lon2):
        """Return delta of two coords in m."""
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r * 1000


if __name__ == '__main__':
    gd = GeohashDelta('dn5bpxd', 'djupbqe')
