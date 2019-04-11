This is used to identify which jobs are within a reasonable radius of universities.
Given the json datafile of jobs information, and the csv export of universities,
we take the location (city, state) for each university and compare it to each job.
This pair of locations is passed to the GoogleMaps distance_matrix API to determine
whether the distance between locations is within the reasonable radius.
All matches within the reasonable distance are dumped to a json file.
