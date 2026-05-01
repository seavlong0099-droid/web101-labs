import matplotlib.pyplot as plt

data = [
    30.3, 39.0, 33.9, 38.6, 44.6, 31.4, 26.7, 51.9, 31.9,
    27.2, 52.9, 45.8, 63.3, 36.0, 64.0, 31.4, 42.2, 41.1,
    37.0, 34.4, 35.5, 62.2, 30.3, 40.0, 36.0, 39.4, 34.4,
    28.3, 39.1, 55.0, 35.0, 28.8, 25.7, 62.7, 32.4, 31.9,
    37.5, 31.5, 32.0, 35.5, 37.5, 41.0, 37.5, 48.6, 28.1
]

plt.hist(data, bins=10, edgecolor='black')
plt.title('Histogram of Maximum Wind Speeds in Hong Kong Over 45 Years')
plt.xlabel('Wind Speed')
plt.ylabel('Frequency')
plt.show()
