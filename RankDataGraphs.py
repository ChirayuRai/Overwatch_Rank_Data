# Example python program to read data from a PostgreSQL table
# and load into a pandas DataFrame

import psycopg2
import pandas as pds
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


# Create an engine instance
alchemyEngine = create_engine('postgres://postgres:home@localhost:5432/owrank', pool_recycle=3600);

# Connect to PostgreSQL server
dbConnection = alchemyEngine.connect();

# Read data from PostgreSQL database table and load into a DataFrame instance
dataFrame = pds.read_sql("select * from \"ranks\"", dbConnection);
pds.set_option('display.expand_frame_repr', False);

# Print the DataFrame
# plt.title("How I Throw With Each Rank")

plt.plot(dataFrame.time_created, dataFrame.tank, label="Tank")
plt.plot(dataFrame.time_created, dataFrame.damage, label="Damage")
plt.plot(dataFrame.time_created, dataFrame.support, label="Support")

# Makes the labels look better
plt.xticks(rotation=40, horizontalalignment='right')

plt.xlabel("Time")
plt.ylabel("Rank")

plt.legend()

plt.show()

# Close the database connection
dbConnection.close();
