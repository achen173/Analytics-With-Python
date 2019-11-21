import sys
import csv
import random
import math


MAX_ITERS = 100


class Location(object):
    def __init__(self, nm, lt, ln):
        self.name = nm
        self.lat = lt
        self.lng = ln

    def get_name(self):
        return self.name

    def get_lat(self):
        return self.lat

    def get_lng(self):
        return self.lng

    def get_coords(self):
        return self.lat, self.lng


def read_data(file_name):
    locs = []
    with open(file_name) as infile:
        reader = csv.reader(infile)
        next(reader)  # skip the header
        for row in reader:
            name = row[0]
            lat = float(row[1])
            lng = float(row[2])
            locs.append(Location(name, lat, lng))
    return locs


def kmeans(locs, k):
    """Use k-means clustering to cluster a list of Location objects.

    Arguments:
        locs -- list of Location objects to cluster
        k -- the number of clusters

    Returns:
        A list of lists of location objects, defining the clusters
    """

    # Initialize centroids to random data points.  Since we'll be using the centroids as
    # dictionary keys, we'll only grab a tuple containing latitude and longitude
    centroid_locs = random.sample(locs, k)
    centroids = [ (loc.lat, loc.lng) for loc in centroid_locs ]
    centroid__cluster = {}  # (42.1, -119.3) -> [ loc1, loc2, loc3, ... ]

    # Run a fixed number of iterations or until convergence is reached
    for i in range(MAX_ITERS):

        # Clusters will be stored in a dictionary, with centroids as keys
        centroid__cluster = {}
        for centroid_coords in centroids:
            centroid__cluster[centroid_coords] = []

        # Assign each location object to its closest centroid's cluster
        # best_centroid_dist = sys.maxsize
        for loc in locs:
            best_centroid = None  # this is just a placeholder for now
            best_centroid_dist = sys.maxsize
            for centroid_coords in centroids:
                best_centroid_dist_temp = distance(loc.get_coords(), centroid_coords)
                if (best_centroid_dist_temp < best_centroid_dist):
                    best_centroid_dist = best_centroid_dist_temp
                    best_centroid = centroid_coords
            # FILL THIS IN
            # You're probably going to want to iterate over the centroids, calculate the
            # distance to each one, and keep track of the one that's the closest.
            # best_centroid = random.choice(centroids)  # This will need to be fixed!

            centroid__cluster[best_centroid].append(loc)

        # Now recompute the centroid value for each cluster
        centroids = []  # throw out the old centroids
        for cluster in centroid__cluster.values():
            lat_mean = sum([ loc.get_lat() for loc in cluster ]) / len(cluster)
            lng_mean = sum([ loc.get_lng() for loc in cluster ]) / len(cluster)
            new_centroid = (lat_mean, lng_mean)
            centroids.append(new_centroid)

        # FILL THIS IN
        # Bonus: how would you add a convergence test to break out of the loop.  Some
        # possibilities are: stop if cluster groups remain the same after reassignment,
        # stop if centroids don't change (more than some threshoold), or stop if the sum
        # of squared errors (the distance between each point and its cluster centroid)
        # doesn't change beyond some threshold.

    return list(centroid__cluster.values())


def distance(coords1, coords2):
    x1, y1 = coords1
    x2, y2 = coords2
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return dist


#############################

if __name__ == '__main__':

    #k = int(sys.argv[1])
    k = 5
    locs = read_data('mustard_geo.csv')

    clusters = kmeans(locs, k)

    for i, clust in enumerate(clusters):
        print("Cluster{}:".format(i))
        for loc in clust:
            print(loc.get_name())
        print("\n")
