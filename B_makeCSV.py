import csv

data = []
test_data = []

with open('Reviews.csv', mode='r') as review_file:
    review_reader = csv.reader(review_file)
    line_count = 0
    for row in review_reader:
        if line_count == 0:
            fieldname = [row[2], row[1], row[6]]
            test_fieldname = [row[2], row[1], row[6], 'test']
            line_count += 1
        else:
            data.append([row[2], row[1], float(row[6])])
            test_data.append([row[2], row[1], float(row[6]), 'c'])
            line_count += 1

uid = {}
pid = {}
for one in data:
    if one[0] in uid:
        uid[one[0]] += 1
    else:
        uid[one[0]] = 1

count = 0
for id in list(uid.keys()):
    if uid[id] < 5:
        del uid[id]
        continue
    if uid[id] > 100:
        del uid[id]
        continue

for one in data:
    if one[0] in uid:
        if one[1] not in pid:
            pid[one[1]] = 0
        pid[one[1]] += 1
print(len(pid))

skip = 0
count = 0
for i in range(len(test_data)):
    if skip < 100000:
        skip += 1
        continue
    if test_data[i][0] in uid:
        test_data[i][3] = 'q'
        count += 1
    if count > 5000:
        break

with open('training.csv', mode='w', newline='') as training_file:
    training_writer = csv.writer(training_file)
    training_writer.writerows(data)

with open('testing.csv', mode='w', newline='') as testing_file:
    testing_writer = csv.writer(testing_file)
    testing_writer.writerows(test_data)
