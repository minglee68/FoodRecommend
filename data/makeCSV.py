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
            data.append([row[2], row[1], row[6]])
            if line_count % 1000 == 0:
                test_data.append([row[2], row[1], row[6], 'q'])
            else:
                test_data.append([row[2], row[1], row[6], 'c'])
            line_count += 1

with open('food_training.csv', mode='w', newline='') as training_file:
    training_writer = csv.writer(training_file)
    training_writer.writerow(fieldname)
    training_writer.writerows(data)

with open('food_testing.csv', mode='w', newline='') as testing_file:
    testing_writer = csv.writer(testing_file)
    testing_writer.writerow(test_fieldname)
    testing_writer.writerows(test_data)
