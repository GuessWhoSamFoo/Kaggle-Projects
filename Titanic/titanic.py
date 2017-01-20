import csv as csv
import numpy as np

csv_file_object = csv.reader(open('train.csv','rb'))
header = csv_file_object.next()

data = []
for row in csv_file_object:
    data.append(row)
data = np.array(data)

number_passengers = np.size(data[0::,1].astype(np.float))
number_survived = np.sum(data[0::,1].astype(np.float))
proportion_suvivors = number_survived/number_passengers

women_only_stats = data[0::,4] == 'female'
men_only_stats = data[0::,4] != 'female'

women_onboard = data[women_only_stats,1].astype(np.float)
men_onboard = data[men_only_stats,1].astype(np.float)

prop_women_survived = np.sum(women_onboard) / np.size(women_onboard)
prop_men_survived = np.sum(men_onboard) / np.size(men_onboard)

print 'women survived is %s' % prop_women_survived
print 'men survived is %s' %prop_men_survived

test_file = open('test.csv','rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()

prediction_file = open('genderbasedmodel.csv','wb')
prediction_file_object = csv.writer(prediction_file)

prediction_file_object.writerow(['PassengerId','Survived'])
for row in test_file_object:
    if row[3] == 'female':
        prediction_file_object.writerow([row[0],'1'])
    else:
        prediction_file_object.writerow([row[0],'0'])
test_file.close()
prediction_file.close()

fare_ceiling = 40
data[data[0::,9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1.0

fare_bracket_size = 10
num_price_brackets = fare_ceiling / fare_bracket_size

num_of_classes = len(np.unique(data[0::,2]))

survival_table = np.zeros((2,num_of_classes, num_price_brackets))

for i in xrange(num_of_classes):
    for j in xrange(num_of_classes):
        women_only_stats = data[
            (data[0::,4] == 'female')
            & (data[0::,2].astype(np.float) == i+1)
            & (data[0:,9].astype(np.float) >= j*fare_bracket_size)
            & (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size),
            1
        ]

for i in xrange(num_of_classes):
    for j in xrange(num_of_classes):
        men_only_stats = data[
            (data[0::,4] != 'female')
            & (data[0::,2].astype(np.float) == i+1)
            & (data[0:,9].astype(np.float) >= j*fare_bracket_size)
            & (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size),
            1
        ]

survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float))
survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))

print survival_table
