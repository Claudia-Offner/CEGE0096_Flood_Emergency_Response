# CEGE0096 Assignment 2

### Assignment 2 - Team Lemur
Extreme flooding is expected on the Isle of Wight and the authority in charge of planning the emergency response is advising everyone to proceed by foot to the nearest high ground. To support this process, the emergency response authority wants you to develop a software to quickly advise people of the quickest route that they should take to walk to the highest point of land within a 5km radius. This software runs a Flood Planning Emergency analysis to determine the shortest path to the highest elevated area within a 5km radius from a users location. First, the software extracts elevation data within a 5km radius using a raster mask. Then, utilizing rtree and networkx packages, Naismith’s rule is applied to identify the users shortest route to safety. The program outputs a map featuring the surrounding area’s elevation, the evacuation route and key location points.
