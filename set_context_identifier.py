#!/usr/bin/env python

import hashlib
from tabulate import tabulate
import inquirer
import os
import sys
from pprint import pprint
sys.path.append(os.path.realpath("."))

project = {
    "file_A.txt": [
        "Which of the following have you heard of?",
        "Events or online activities organised by together.eu",
        "Petitions to the European Parliament", # repeated
        "Contacting an MEP about an issue",
        "foo",
        "And which of these have you actively taken part in?",
        "Events or online activities organised by together.eu",
        "Petitions to the European Parliament", # repeated
        "Contacting an MEP about an issue",
        "bar"
    ],
    "file_B.txt": [
        "baz",
        "Petitions to the European Parliament", # repeated
        "qux"
    ],
    "file_C.txt": [
        "Events or online activities organised by together.eu",
        "Petitions to the European Parliament", # repeated
        "Contacting an MEP about an issue"
    ]
}

def set_segment_identifier(approach, consider_file = True):
    """ Sets the segment context identifier based on the approach chosen. """
    hash_table = []
    count = {}
    absolute_segment_number = 0
    for filename, segments in project.items():
        if not filename in count:
            count[filename] = {}
        for i, segment in enumerate(segments):
            absolute_segment_number += 1

            if approach == "relative-segment-number":
                if consider_file:
                    context = filename + str(i)
                else:
                    context = absolute_segment_number
            elif approach == "repetition-count-per-file":
                if not segment in count[filename]:
                    count[filename][segment] = 0
                count[filename][segment] += 1
                if consider_file:
                    context = filename + segment + str(count[filename][segment])
                else:
                    context = segment + str(count[filename][segment])
            else: # prev/next (current default)
                prev = segments[i-1] if i > 0 else "START"
                next = segments[i+1] if i < len(segments)-1 else "END"
                if consider_file:
                    context = filename + prev + next
                else:
                    context = prev + next

            hash = hashlib.md5(context.encode()).hexdigest()
            hash_table.append([str(absolute_segment_number).zfill(2), filename, str(i).zfill(2), hash, segment])
    return hash_table



# for filename, segments in project.items():
#     print(filename)
#     print("="*len(filename))
#     for i, segment in enumerate(segments, start=1):
#         relative_number_context = filename + str(i)
#         hash = hashlib.md5(relative_number_context.encode()).hexdigest()
#         print(i, hash, segment)
#     print()
#
#
# for filename, segments in project.items():
#     print(filename)
#     print("="*len(filename))
#     for i, segment in enumerate(segments):
#         prev = segments[i-1] if i > 0 else "START"
#         next = segments[i+1] if i < len(segments)-1 else "END"
#         prev_next_context = prev + next
#         hash = hashlib.md5(prev_next_context.encode()).hexdigest()
#         print(i, hash, segment)
#     print()

# print(str(hash("Hello World")))
print("Given the following project:")
pprint(project)
print("Please select the approach")

questions = [
    inquirer.List(
        "approach",
        message="What approach do you want to use to set context identifiers for every segment in the project?",
        choices=[
            "prev/next",
            "relative-segment-number",
            "repetition-count-per-file"
            ]
    ),
    inquirer.Confirm("consider_file", message="Would you like to consider the filepath as part of the context?", default=True)
]
answers = inquirer.prompt(questions)

approach = answers["approach"]
consider_file = answers["consider_file"]

hash_table = set_segment_identifier(approach, consider_file = True)

print(tabulate(hash_table, headers=['Abs#', 'File', 'Rel#', 'ID', 'Segment']))

segment = "Petitions to the European Parliament"
repeated_seg_ids = [row[3] for row in hash_table if segment in row]

print()
print(f"There are {len(repeated_seg_ids)} instances of segment '{segment}' in the project, with identifiers:\n")
for id in repeated_seg_ids:
    print(f" * {id}")

print()
print("Alternative translations can be bound to the identifiers above.")
print("As many alternative translations are possible for this segment as unique identifiers the list above contains.")
