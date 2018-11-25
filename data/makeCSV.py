import csv

data = []
test_data = []
uid = []
pid = []

with open('Reviews.csv', mode='r') as review_file:
    review_reader = csv.reader(review_file)
    line_count = 0
    for row in review_reader:
        if line_count == 0:
            fieldname = [row[2], row[1], row[6]]
            test_fieldname = [row[2], row[1], row[6], 'test']
            line_count += 1
        else:
            uid.append(row[2])
            pid.append(row[1])
            data.append([row[2], row[1], float(row[6])])
            if line_count % 1000 == 0:
                test_data.append([row[2], row[1], float(row[6]), 'q'])
            else:
                test_data.append([row[2], row[1], float(row[6]), 'c'])
            line_count += 1

uid_set = list(set(uid))
pid_set = list(set(pid))
print(len(uid), len(uid_set))
print(len(pid), len(pid_set))

uid_dict = {}
pid_dict = {}

count = 1
for id in uid_set:
    uid_dict.update({id: count})
    count += 1

count = 1
for id in pid_set:
    pid_dict.update({id: count})
    count += 1

for i in range(len(data)):
    data[i][0] = uid_dict[data[i][0]]
    data[i][1] = pid_dict[data[i][1]]
    test_data[i][0] = uid_dict[test_data[i][0]]
    test_data[i][1] = pid_dict[test_data[i][1]]

with open('food_training.csv', mode='w', newline='') as training_file:
    training_writer = csv.writer(training_file)
    training_writer.writerows(data)

with open('food_testing.csv', mode='w', newline='') as testing_file:
    testing_writer = csv.writer(testing_file)
    testing_writer.writerows(test_data)
