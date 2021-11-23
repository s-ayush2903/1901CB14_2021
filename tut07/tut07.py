import openpyxl
from collections import defaultdict
import os
import shutil
import csv

"""
Maintain a map(dictionary) of 
* RollNo to feedback of subs not filled => Ans
* RollNo to subs taken, here the value will actually be a list of 
  (a map of sub to no of valid feedbacks?) 
  or we could use the map created already for the sub to valid feedbacks?
* Subs to type of valid feedbacks supposed to be filled => Master one, means in
  ideal scenario which feedbacks for a specific subject will be filled

Maintain a map(dictionary) of RollNo to feedback of subs not filled
"""

pwd = os.getcwd()
subLtpFile = os.path.join(pwd, "course_master_dont_open_in_excel.csv")
studFeedbackFile = os.path.join(pwd, "course_feedback_submitted_by_students.csv")
courseRegnFile = os.path.join(pwd, "course_registered_by_all_students.csv")
studInfoFile = os.path.join(pwd, "studentinfo.csv")

"""
Map of subject code to number of feedback entries in backend for it by a rollNo, ideally
"""
idealSubFeedbackEntriesMap = {}

"Map of rollNo to dicts of "
rollFeedbackMap = {}

"""
 Map of rollNo to someStuff, where someStuff in itself is
 a map of subCode to the schedule sem
"""
rollSubcodeSemMap = {}
studInfoMap = {}

def prepStudInfoMap():
  for index, contents in enumerate(csv.reader(open(studInfoFile))):
    if index > 0:
      studInfoMap[contents[1]] = [contents[0], contents[8], contents[9], contents[10]]
  return studInfoMap


def validFeedbackOptionsfFromLtp(ltpStr: str) -> int:
  validEntries = []
  formattedList = ltpStr.split("-")
  for i in range(0, 3):
    if formattedList[i] != "0":
      validEntries.append(str(i + 1))
  return validEntries


"""
@param contents: subNo, subName, ltp, creds
corresp. indices:  0  ,   1    ,  2 ,   3   
"""
def subFeedbackInfo():
  for index, contents in enumerate(csv.reader(open(subLtpFile))):
      if index > 0:
          validEntries = validFeedbackOptionsfFromLtp(contents[2])
          idealSubFeedbackEntriesMap[contents[0]] = validEntries
  return idealSubFeedbackEntriesMap


"""
@param contents: rollNo | regSem | scheduledSem | subCode |
-----------------------------------------------------------
corresp. indices:   0   |   1    |      2       |    3    |
"""
def prepRollSubcodeSemMap():
  for index, contents in enumerate(csv.reader(open(courseRegnFile))):
    if index > 0:
      roll = contents[0]
      scheduledSem = contents[2]
      subCode = contents[3]
      if roll not in rollSubcodeSemMap:
        rollSubcodeSemMap[roll] = {}
      if subCode not in rollSubcodeSemMap[roll]:
        rollSubcodeSemMap[roll][subCode] = 1
      rollSubcodeSemMap[roll][subCode] = scheduledSem
  return rollSubcodeSemMap


"""
  Can this be simplified? Means can we reduce one more iteration
  or
  could this be done in one go?
"""
def prepRollFeedbackMap():
  """
  @param contents: id | email | name | rollNo | courseCode | feedbackType |
  -------------------------------------------------------------------------
  corresp. indices: 0 |   1   |   2  |   3    |     4      |      5       |
  """
  for index, contents in enumerate(csv.reader(open(studFeedbackFile))):
    if index > 0:
        roll = contents[3]
        subCode = contents[4]
        feedbackType = contents[5]
        if roll not in rollFeedbackMap:
          rollFeedbackMap[roll] = {}
        if subCode not in rollFeedbackMap[roll]:
          rollFeedbackMap[roll][subCode] = []
        feedbacksListForSub = rollFeedbackMap[roll][subCode]
        if roll in rollSubcodeSemMap and feedbackType in idealSubFeedbackEntriesMap[subCode] and [rollSubcodeSemMap[roll][subCode], feedbackType] not in feedbacksListForSub:
          feedbacksListForSub.append([rollSubcodeSemMap[roll][subCode], feedbackType])
  return rollFeedbackMap
          


def feedback_not_submitted():
    ltp_mapping_feedback_type = {1: "lecture", 2: "tutorial", 3: "practical"}
    output_file_name = os.path.join(pwd, "course_feedback_remaining.xlsx")
    if os.path.exists(output_file_name):
      os.remove(output_file_name)

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(["rollno", "schedule_sem", "subno", "name", "email", "aemail", "contact"])

    for roll in rollSubcodeSemMap:
      for subCode in rollSubcodeSemMap[roll]:
        if roll not in rollFeedbackMap:
          if roll not in studInfoMap:
            name = "NA_IN_STUDENT_INFO"
            email = "NA_IN_STUDENT_INFO"
            aemail = "NA_IN_STUDENT_INFO"
            contact = "NA_IN_STUDENT_INFO"
          else:
            name = studInfoMap[roll][0]
            email = studInfoMap[roll][1]
            aemail = studInfoMap[roll][2]
            contact = studInfoMap[roll][3]
          if subCode.strip() not in ["NSO", "NSS"] and len(idealSubFeedbackEntriesMap[subCode]) > 0:
            sheet.append([roll, rollSubcodeSemMap[roll][subCode], subCode, name, email, aemail, contact])

        elif subCode not in rollFeedbackMap[roll].keys():
          name = "NA_IN_STUDENT_INFO"
          email = "NA_IN_STUDENT_INFO"
          aemail = "NA_IN_STUDENT_INFO"
          contact = "NA_IN_STUDENT_INFO"
          if roll in studInfoMap:
            name = studInfoMap[roll][0]
            email = studInfoMap[roll][1]
            aemail = studInfoMap[roll][2]
            contact = studInfoMap[roll][3]
          if subCode in idealSubFeedbackEntriesMap and len(idealSubFeedbackEntriesMap[subCode]) > 0:
            sheet.append([roll, rollSubcodeSemMap[roll][subCode], subCode, name, email, aemail, contact])
            # sheet.append([roll, rollSubcodeSemMap[roll][subCode], subCode])
        else:
          # name = "NA_IN_STUDENT_INFO"
          # email = "NA_IN_STUDENT_INFO"
          # aemail = "NA_IN_STUDENT_INFO"
          # contact = "NA_IN_STUDENT_INFO"
          if roll in studInfoMap:
            name = studInfoMap[roll][0]
            email = studInfoMap[roll][1]
            aemail = studInfoMap[roll][2]
            contact = studInfoMap[roll][3]
          lsss = sorted(rollFeedbackMap[roll][subCode])
          newList = []
          for sth in lsss:
            newList.append(sth[1])
          if newList != sorted(idealSubFeedbackEntriesMap[subCode]) and len(idealSubFeedbackEntriesMap[subCode]) > 0:
            sheet.append([roll, rollSubcodeSemMap[roll][subCode], subCode, name, email, aemail, contact])
            # sheet.append([roll, subCode, rollSubcodeSemMap[roll][subCode]])
    wb.save(output_file_name)


prepStudInfoMap()
prepRollSubcodeSemMap()
subFeedbackInfo()
prepRollFeedbackMap()
feedback_not_submitted()
