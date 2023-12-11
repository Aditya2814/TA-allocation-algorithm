# Importing necessary libraries
import pandas as pd
import numpy as np

# Reading the excel files.
xls = pd.ExcelFile(r"data.xlsx")
df1 = pd.read_excel(xls, 'Sheet1')
df2 = pd.read_excel(xls, 'Sheet2')

# Changing all the NaN values to None for convenience.
df2 = df2.where(pd.notnull(df2), None)

# Taking the two inputs according to the requirements from the users.
one_TA_per_credit_per_how_many_students = int(input('1 TA per credit per approximately how many students = '))
number_of_students_for_no_TAs = 20

# The below code calculates the required number of TAs for each course according to number of students enrolled in that course.
# According to the formula: required_number_of_TAs_in_a_course = number_of_students_in_that_course * credits_in_that_course / one_TA_per_credit_per_how_many_students
# If number_of_students_in_that_course < number_of_students_for_no_TAs then required_number_of_TAs_in_a_course = 0
required_number_of_TAs = []
for index, rows in df1.iterrows():
    credits = int(rows['Credits'][0]) + int(rows['Credits'][2]) + 0.5*int(rows['Credits'][4])
    if rows['No. of Students'] <= number_of_students_for_no_TAs:
        required_number_of_TAs.append(0)
    elif rows['No. of Students']*credits < one_TA_per_credit_per_how_many_students:
        required_number_of_TAs.append(0)
    else:
        required_number_of_TAs.append(round(rows['No. of Students']*credits / one_TA_per_credit_per_how_many_students))

df1['Required_Number_of_TAs'] = required_number_of_TAs

# Order to be used while allocating TAs according to their seniority and checking if a TA is allocated to his junior batches only.
order = {
    'UG-1': 1,
    'UG-2': 2,
    'UG-3': 3,
    'UG-4': 4,
    'MTech-1': 5,
    'MTech-2': 6,
    'MTech-PhD-1': 5,
    'MTech-PhD-2': 6,
    'MTech-PhD-3': 9,
    'MTech-PhD-4': 10,
    'MTech-PhD-5': 11,
    'PhD-1': 7,
    'PhD-2': 8,
    'PhD-3': 9,
    'PhD-4': 10,
    'PhD-5': 11
}

# Grades order to be used while allocating according to their grades in the respective course.
# An additional constraint is that when two TAs share the same level of seniority, the differentiating factor becomes their grade.
grades_order = {
    'A': 10,
    'A-': 9,
    'B': 8,
    'B-': 7,
    'C': 6,
    'C-': 5,
}

'''Checking if a TA is eligible using 3 constraints:
1) The TA should have done that course.
2) The TA should have a decent grade (A or A-) in that course.
3) The TA should be assigned only to his junior batches using the "order" dictionary.'''
def is_eligible(ta_program, course_offered_for, preferences, course_name):
  return course_name in preferences.keys() and preferences[course_name] in ['A', 'A-'] and order[ta_program] > order[course_offered_for]

course_assignments = {} # This dictionary stores course codes(for courses which have required number of TAs > 0) as keys and eligible TAs(according to the 3 conditions) as values.
eligible_tas_list = set() # This set stores TAs which are eligible(according to the 3 conditions) in atleast one of the courses which have requirement of TAs > 0.
for _, course_row in df1.iterrows():
  course_code = course_row['Course Code']
  course_name = course_row['Course Name']

  if course_row['Required_Number_of_TAs'] == 0:
    continue

  eligible_tas = []

  for index, ta_row in df2.iterrows():
    preferences = {ta_row['Preference-1']: df2.iloc[index, 6], ta_row['Preference-2']: df2.iloc[index, 8], ta_row['Preference-3']: df2.iloc[index, 10]}
    if ta_row['Preference-4'] is not None:
      preferences[ta_row['Preference-4']] = df2.iloc[index, 12]
      if ta_row['Preference-5'] is not None:
        preferences[ta_row['Preference-5']] = df2.iloc[index, 14]

    if is_eligible(ta_row['Program'], course_row['Offered for'], preferences, course_name):
      eligible_tas.append(ta_row['Roll No. '])
      eligible_tas_list.add(ta_row['Roll No. '])

  course_assignments[course_code] = eligible_tas

ineligible_tas = [] # This list Stores all the TAs which are ineligible(according to the 3 conditions) in any of the courses in their preferences.

for ta in df2['Roll No. '].values:
    if ta not in eligible_tas_list:
        ineligible_tas.append(ta)

difference = {} # This dictionary stores the course code as key and the required number of TAs - number of TAs allocated to that course as the value.
for course in course_assignments:
  required = df1.loc[df1['Course Code'] == course, 'Required_Number_of_TAs'].values[0]
  present = len(course_assignments[course])
  difference[course] = required-present

ta_assignments = {} # This dictionary stores the TAs as keys and their respective courses they are allocated to as values.
for course in course_assignments:
  tas = course_assignments[course]
  for ta in tas:
    if ta not in ta_assignments.keys():
      ta_assignments[ta] = [course]
    else:
      ta_assignments[ta].append(course)

# In the code below, each TA initially has a list of eligible courses. To reduce that list to a size of 1, courses should be selectively removed, retaining the most optimal course for each TA.
# For this, I am choosing that course which has the most number of required TAs, i.e., the difference[course] should be max and the next differentiating factor will be preference.
for ta in ta_assignments:
  courses = ta_assignments[ta]
  preference_course_names = list(df2.loc[df2['Roll No. '] == ta, ['Preference-1', 'Preference-2', 'Preference-3', 'Preference-4', 'Preference-5']].values[0])
  preferences = []
  for preference in preference_course_names:
    if preference is not None:
      preferences.append(df1.loc[df1['Course Name'] == preference, 'Course Code'].values[0])

  temp = [item for item in preferences if item in courses]
  courses = temp
  if len(courses) > 1:
    diffs = []
    for course in courses:
      diff = difference[course]
      diffs.append(diff)

    max_index = np.argmax(diffs)
    assigned_course = courses[max_index]

    for course in courses:
      difference[course] += 1
      course_assignments[course].remove(ta)

    ta_assignments[ta] = [assigned_course]
    difference[assigned_course] -= 1
    course_assignments[assigned_course].append(ta)

# The below code sorts TAs according to their hierarchy hence more preference is given to PG TAs than UG TAs.
# This leads to an increased proportion of Postgraduate (PG) TAs compared to Undergraduate (UG) TAs, and this shift occurs for each individual course as well as for the overall distribution.
for course in course_assignments:
  tas = np.array(course_assignments[course])
  programs = [df2.loc[df2['Roll No. '] == ta, 'Program'].values[0] for ta in tas]
  priorities1 = [order[program] for program in programs]
  sorted_priorities1 = np.argsort(priorities1)[-1::-1]
  sorted_tas = tas[sorted_priorities1].tolist()
  course_assignments[course] = sorted_tas

extra_tas = [] # This list stores TAs which were eligible in a particular course but were excluded beacuse of less vacancies.
for course in difference:
  while difference[course] < 0:
    difference[course] += 1
    extra_ta = course_assignments[course].pop()
    del ta_assignments[extra_ta]
    extra_tas.append(extra_ta)


# The below code checks if there are any vacancies left which matches with the extra TAs' preferences.
for ta in extra_tas:
  row = df2.loc[df2['Roll No. '] == ta]
  preferences = [row['Preference-1'].values[0], row['Preference-2'].values[0], row['Preference-3'].values[0]]
  if row['Preference-4'].values[0] is not None:
    preferences.append(row['Preference-4'].values[0])
    if row['Preference-5'].values[0] is not None:
      preferences.append(row['Preference-5'].values[0])

  for course in preferences:
    course_code = df1.loc[df1['Course Name'] == course, 'Course Code'].values[0]
    if course_code in difference and difference[course_code] > 0:
      course_assignments[course_code].append(ta)
      ta_assignments[ta] = [course_code]
      difference[course_code] -= 1
      extra_tas.remove(ta)
      break

print(course_assignments)

# Merging the lists of unassigned TAs
unassigned_tas = ineligible_tas + extra_tas

details_of_unassigned_tas = df2[df2['Roll No. '].isin(unassigned_tas)]

details_of_unassigned_tas.to_csv(r'Details of unassigned TAs.csv', index=False)