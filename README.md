# TA-allocation-algorithm

# Teaching Assistant (TA) Allocation

## Introduction
This Python program is designed to allocate Teaching Assistants (TAs) to specific courses while adhering to a set of constraints. It  addresses the challenge of optimizing TA allocation based on various criteria. The program generates a CSV file containing details of unallocated TAs and provides a summary of TA assignments for each course.

## Constraints
The program takes into account the following constraints during the TA allocation process:
1. TAs must have completed the course they are assigned to or a similar course with a decent grade.
2. Each course must have the required number of TAs, with the rate of 1 TA per approximately 90 students per credit.
3. Students may be eligible for multiple courses, but each student can only be assigned to one course.
4. There should be at least one PhD/MTech-PhD TA for every 100 students.
5. A course cannot have more than 60% undergraduate (UG) TAs.
6. TAs can only be assigned to courses offered to their academically junior batches.

## Algorithm
The TA allocation algorithm follows a forward search approach. Here's an overview of the algorithm's key steps:
1. Calculate the required number of TAs for each course based on student enrollment, credits, and user-defined preferences.
2. Identify eligible TAs for each course based on the three primary constraints.
3. Match each TA to an optimal course by selecting the one with the most unallocated TA slots. If multiple courses have the same number of slots, preferences are considered.
4. Sort eligible TAs based on seniority to prioritize postgraduate (PG) TAs over undergraduate (UG) TAs.
5. Handle situations where extra TAs are initially removed from courses with fewer slots by reassigning them to courses they prefer.

## Input Data
The program takes 1 input excel file with 2 sheets:
Sheet 1: Details of courses, including course codes, names, credits, and the number of students.
Sheet 2: Details of TAs, which include their roll numbers, programs, preferences, and grades in the preferred courses.

To use your own data with the program:

- Delete the default data in the provided Excel file.
- Add your preferred data to the Excel file with the same column names as in the default file.
- Save the file.

or 

- Delete the default Excel file from the folder.
- Add your file in the same folder (ensure it has the same columns as in the default file).
- Rename the file to "data" (without the double inverted commas).

## Execution Details
Extract the zip file.
Open the terminal in the folder that you have extracted all the files.
Run the commands mentioned below in the terminal to install all necessary libraries.

pip install numpy
pip install pandas
pip install openpyxl

After installing these libraries run the command mentioned below in the terminal.

python ta_allocation_algorithm.py

After you have run the command mentioned above, You will be asked for an input (ie. number of students per TA).
After you have entered the input press 'enter' to run the code.
---

## Output Details
The program will print courses (those having required number of TAs > 0) along with a list of Roll Numbers of TAs assigned to that course.
The program will also save a .csv file having all the details of unassigned TAs in the same folder.

For detailed instructions on how to run this program and interpret the output, refer to the code and report provided in this repository.

**Author:** Aditya Dhaduk (B21AI014)
**Course:** CSL3090: Artificial Intelligence
**Date:** 12-10-2023
