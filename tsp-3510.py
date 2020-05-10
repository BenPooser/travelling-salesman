import sys
import time
import numpy as np
start_time = time.time()
import random
import statistics


# Command arguments
input_coords = sys.argv[1]
output_tour = sys.argv[2]
max_time = sys.argv[3]

# Storing x and y values in matrix
coords = open(input_coords, 'r')
matrix_coords = []
for coord in coords:
	line = coord.split()
	temp = np.array([float(line[1]), float(line[2])])
	if len(matrix_coords) == 0:
		matrix_coords = temp
	else:
		matrix_coords = np.vstack((matrix_coords, temp))
coords.close()
# A given city x's coordinates are given by matrix_coords[x]

# Calculating Euclidean Distances
dist = np.transpose(matrix_coords[:,:,np.newaxis]) - matrix_coords[:,:,np.newaxis]
dist = np.transpose(np.square(dist))
dist = dist.sum(axis=1)
dist = np.sqrt(dist)
dist = np.rint(dist)
dist = dist.astype(int)
# The Euclidean Distance between 2 coordinates i and j is given by dist[i][j]

# Start with random path, swap nodes til time is up
num_cities = matrix_coords.shape[0]
current_tour = np.arange(1, num_cities + 1)
best_tour = current_tour
total_cost = 0
for i in range(current_tour.size):
    if i + 1 == current_tour.size:
        total_cost += dist[current_tour[i]-1][current_tour[0]-1]
    else:
        total_cost += dist[current_tour[i]-1][current_tour[i + 1]-1]
best_cost = total_cost

first_run = True
while (time.time() - start_time + 0.05 < int(max_time)):
	# Random Nearest Neighbor
	start = np.random.randint(1,num_cities+1)
	new_tour = np.array([start])
	done = False
	while new_tour.size < num_cities - 3 and not done:
		k = 2
		curr_dist = dist[new_tour[new_tour.size-1]-1]
		next_shortest = np.argpartition(dist[new_tour[new_tour.size-1]-1], k)
		next_shortest = next_shortest[:k]
		next_shortest = np.argwhere(curr_dist == curr_dist[next_shortest].max()) + 1
		while next_shortest in new_tour:
			k += 1
			curr_dist = dist[new_tour[new_tour.size-1]-1]
			try:
				next_shortest = np.argpartition(dist[new_tour[new_tour.size-1]-1], k)
				next_shortest = next_shortest[:k]
				next_shortest = np.argwhere(curr_dist == curr_dist[next_shortest].max()) + 1
			except:
				done = True
				break
		if new_tour.size + 1 < num_cities - 1 and not done:
			k += 1
			curr_dist = dist[new_tour[new_tour.size-1]-1]
			next_next_shortest = np.argpartition(dist[new_tour[new_tour.size-1]-1], k)
			next_next_shortest = next_next_shortest[:k]
			next_next_shortest = np.argwhere(curr_dist == curr_dist[next_next_shortest].max()) + 1
			while next_next_shortest in new_tour:
				k += 1
				curr_dist = dist[new_tour[new_tour.size-1]-1]
				try:
					next_next_shortest = np.argpartition(dist[new_tour[new_tour.size-1]-1], k)
					next_next_shortest = next_next_shortest[:k]
					next_next_shortest = np.argwhere(curr_dist == curr_dist[next_next_shortest].max()) + 1
				except:
					done = True
					break
		# if new_tour.size + 2 < num_cities - 1:
		#     k += 1
		#     if k >= 29:
		#         done = True
		#         print("Restarted at first next_next_next_shortest")
		#         break
		#     curr_dist = dist[new_tour[new_tour.size-1]-1]
		#     next_next_next_shortest = np.argpartition(dist[new_tour[new_tour.size-1]-1], k)
		#     next_next_next_shortest = next_next_next_shortest[:k]
		#     next_next_next_shortest = np.argwhere(curr_dist == curr_dist[next_next_next_shortest].max()) + 1
		#     while next_next_next_shortest in new_tour:
		#         k += 1
		#         if k >= 29:
		#             done = True
		#             print("Restarted at second next_next_next_shortest")
		#             break
		#         curr_dist = dist[new_tour[new_tour.size-1]-1]
		#         next_next_next_shortest = np.argpartition(dist[new_tour[new_tour.size-1]-1], k)
		#         next_next_next_shortest = next_next_next_shortest[:k]
		#         next_next_next_shortest = np.argwhere(curr_dist == curr_dist[next_next_next_shortest].max()) + 1
		# next_addition = random.choice((next_shortest, next_next_shortest, next_next_next_shortest))
		if done:
			continue
		else:
			next_addition = random.choice((next_shortest, next_next_shortest))
		new_tour = np.append(new_tour, next_addition)
	# Add in last 2 elements:
	if done == True:
		continue
	missing = set(range(1, num_cities + 1)).difference(new_tour)
	missing = sorted(missing)
	random_order = np.array((missing))
	np.random.shuffle(random_order)
	new_tour = np.append(new_tour, random_order)

	# Ensure all elements in new_tour
	# j = 1
	# restart = False
	# for i in np.sort(new_tour):
	#     if i != j:
	#         restart = True
	#         break
	#     j += 1
	# if restart:
	#     print(new_tour)
	#     print("Restarted at bad tour")
	#     continue

	# 3-opt, was 2-opt
	first = -1
	unchanged = 0
	while (unchanged < new_tour.size - 2 and time.time() - start_time < int(max_time)):
		if first + 1 == new_tour.size:
			first = 0
		else:
			first += 1
		second = 0
		third = 0
		fourth = 0
		fifth = 0
		if first + 1 == new_tour.size:
			second = 0
		else:
			second = first + 1
		if second + 1 == new_tour.size:
			third = 0
		else:
			third = second + 1
		if third + 1 == new_tour.size:
			fourth = 0
		else:
			fourth = third + 1
		if fourth + 1 == new_tour.size:
			fifth = 0
		else:
			fifth = fourth + 1

		# Swap middle two if results in shorter path
		# pre_swap = dist[new_tour[first]-1][new_tour[second]-1] + dist[new_tour[third]-1][new_tour[fourth]-1]
		# post_swap = dist[new_tour[first]-1][new_tour[third]-1] + dist[new_tour[second]-1][new_tour[fourth]-1]
		# if post_swap < pre_swap:
		#     new_tour[second], new_tour[third] = new_tour[third], new_tour[second]
		#     unchanged = 0
		# else:
		#     unchanged += 1

		# Swap middle three if results in shorter path
		two_three_four = dist[new_tour[first]-1][new_tour[second]-1] + dist[new_tour[second]-1][new_tour[third]-1] + dist[new_tour[third]-1][new_tour[fourth]-1] + dist[new_tour[fourth]-1][new_tour[fifth]-1]
		two_four_three = dist[new_tour[first]-1][new_tour[second]-1] + dist[new_tour[second]-1][new_tour[fourth]-1] + dist[new_tour[fourth]-1][new_tour[third]-1] + dist[new_tour[third]-1][new_tour[fifth]-1]
		three_two_four = dist[new_tour[first]-1][new_tour[third]-1] + dist[new_tour[third]-1][new_tour[second]-1] + dist[new_tour[second]-1][new_tour[fourth]-1] + dist[new_tour[fourth]-1][new_tour[fifth]-1]
		three_four_two = dist[new_tour[first]-1][new_tour[third]-1] + dist[new_tour[third]-1][new_tour[fourth]-1] + dist[new_tour[fourth]-1][new_tour[second]-1] + dist[new_tour[second]-1][new_tour[fifth]-1]
		four_two_three = dist[new_tour[first]-1][new_tour[fourth]-1] + dist[new_tour[fourth]-1][new_tour[second]-1] + dist[new_tour[second]-1][new_tour[third]-1] + dist[new_tour[third]-1][new_tour[fifth]-1]
		four_three_two = dist[new_tour[first]-1][new_tour[fourth]-1] + dist[new_tour[fourth]-1][new_tour[third]-1] + dist[new_tour[third]-1][new_tour[second]-1] + dist[new_tour[second]-1][new_tour[fifth]-1]
		best_combo = min(two_three_four, two_four_three, three_two_four, three_four_two, four_two_three, four_three_two)
		if best_combo == two_four_three:
			new_tour[third], new_tour[fourth] = new_tour[fourth], new_tour[third]
			unchanged = 0
		elif best_combo == three_two_four:
			new_tour[second], new_tour[third] = new_tour[third], new_tour[second]
			unchanged = 0
		elif best_combo == three_four_two:
			new_tour[second], new_tour[third], new_tour[fourth] = new_tour[third], new_tour[fourth], new_tour[second]
			unchanged = 0
		elif best_combo == four_two_three:
			new_tour[second], new_tour[third], new_tour[fourth] = new_tour[fourth], new_tour[second], new_tour[third]
			unchanged = 0
		elif best_combo == four_three_two:
			new_tour[second], new_tour[fourth] = new_tour[fourth], new_tour[second]
			unchanged = 0
		else:
			unchanged += 1

	total_cost = 0
	for i in range(new_tour.size):
		if i + 1 == new_tour.size:
			total_cost += dist[new_tour[i]-1][new_tour[0]-1]
		else:
			total_cost += dist[new_tour[i]-1][new_tour[i + 1]-1]
	if first_run or total_cost < best_cost:
		if first_run:
			first_run = False
		best_cost = total_cost
		best_tour = new_tour
		# print(best_cost)
		# print(best_tour)
	# print(total_cost)
	# print(new_tour)
# print(best_cost)
# print(best_tour)

# Putting best_tour and best_cost in output file
output_file = open(str(output_tour), 'w')
output_file.write(str(best_cost) + '\n')
for location in best_tour:
	output_file.write(str(location) + ' ')
output_file.write(str(best_tour[0]) + '\n')
output_file.close()
