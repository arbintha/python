# -*- coding: utf-8 -*-
"""

@author: puser
Geospatial analysis to understand coverage areas, identify service gaps, and plan network expansions.
"""


import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class GeospatialAnalyzer:
    def __init__(self, file_path):
        self.data = gpd.read_file(file_path)
        self.model = None
        self.centroids = None

    def preprocess_data(self):
        # Convert the data to the correct coordinate reference system if needed
        self.data = self.data.to_crs(epsg=4326)
        print(f"Data CRS: {self.data.crs}")

    def plot_data(self):
        # Plot the geospatial data
        self.data.plot()
        plt.title('Geospatial Data')
        plt.show()

    def visualize_data(self):
        # Create a Folium map to visualize the data
        m = folium.Map(location=[self.data.geometry.centroid.y.mean(), self.data.geometry.centroid.x.mean()], zoom_start=10)
        folium.GeoJson(self.data).add_to(m)
        return m

    def cluster_data(self, n_clusters):
        # Extract the coordinates for clustering
        coordinates = [(geom.centroid.x, geom.centroid.y) for geom in self.data.geometry]
        self.model = KMeans(n_clusters=n_clusters)
        self.data['cluster'] = self.model.fit_predict(coordinates)
        self.centroids = self.model.cluster_centers_

        # Plot the clustered data
        self.data.plot(column='cluster', categorical=True, legend=True)
        plt.scatter(*zip(*self.centroids), color='red')
        plt.title('Clustered Geospatial Data')
        plt.show()

    def evaluate_clusters(self):
        # Evaluate the clustering using Silhouette Score
        coordinates = [(geom.centroid.x, geom.centroid.y) for geom in self.data.geometry]
        silhouette_avg = silhouette_score(coordinates, self.data['cluster'])
        print(f'Silhouette Score: {silhouette_avg}')
        return silhouette_avg

    def suggest_best_model(self):
        # Try different numbers of clusters and suggest the best model
        silhouette_scores = []
        for n_clusters in range(2, 10):
            self.cluster_data(n_clusters)
            score = self.evaluate_clusters()
            silhouette_scores.append((n_clusters, score))

        best_n_clusters = max(silhouette_scores, key=lambda x: x[1])[0]
        print(f'Best number of clusters: {best_n_clusters}')

        # Refit the model with the best number of clusters
        self.cluster_data(best_n_clusters)

        return best_n_clusters

# Create an instance of the GeospatialAnalyzer class
analyzer = GeospatialAnalyzer('large_geospatial_dataset.geojson')

# Preprocess the data
analyzer.preprocess_data()

# Plot the data
analyzer.plot_data()

# Visualize the data
map = analyzer.visualize_data()
map.save('geospatial_data.html')

# Cluster the data with an initial guess of 3 clusters
analyzer.cluster_data(n_clusters=3)

# Evaluate the clusters
analyzer.evaluate_clusters()

# Suggest the best model
best_n_clusters = analyzer.suggest_best_model()

