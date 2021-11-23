import openpyxl
import os
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

"""
 Map of rollNo to dicts of subCode whose feedback is filled, which further contains
 info about the type of feedback filled for a given subject
 """
rollFeedbackMap = {}

"""
 Map of rollNo to someStuff, where someStuff in itself is
 a map of subCode to the schedule sem
"""
rollSubcodeSemMap = {}

"""
A map of rollNo to studInfo, which contains semInfo, emails, name and contact num
"""
studInfoMap = {}

def prepStudInfoMap():
  for index, contents in enumerate(csv.reader(open(studInfoFile))):
    if index > 0:
      studInfoMap[contents[1]] = [contents[0], contents[8], contents[9], contents[10]]
  return studInfoMap


"""
Returns the type of valid feedbacks applicable for a subject with known ltp
e.g., @returns [1, 3] if first and last bit are non-zero
                [1] if only the first bit is non-zero; and so on
"""
def validFeedbackOptionsfFromLtp(ltpStr: str) -> int:
  validEntries = []
  formattedList = ltpStr.split("-")
  for i in range(0, 3):
    if formattedList[i] != "0":
      validEntries.append(str(i + 1))
  return validEntries


"""
@param contents: subNo | subName | ltp | creds |
------------------------------------------------
corresp. indices:  0   |   1     |  2  |   3   |
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
      regnSem = contents[1]
      scheduledSem = contents[2]
      subCode = contents[3]
      if roll not in rollSubcodeSemMap:
        rollSubcodeSemMap[roll] = {}
      if subCode not in rollSubcodeSemMap[roll]:
        rollSubcodeSemMap[roll][subCode] = []
      rollSubcodeSemMap[roll][subCode] = [regnSem, scheduledSem]
  return rollSubcodeSemMap


"""
 Prepares the rollNo to feedback map, where @param [dict].value itself is a
 dict of dicts which means a map of course code to the type of feedback filled,
 and all of this chained together for a specific rollNo
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
      if roll in rollSubcodeSemMap and feedbackType in idealSubFeedbackEntriesMap[subCode] and [rollSubcodeSemMap[roll][subCode][1], feedbackType] not in feedbacksListForSub:
        feedbacksListForSub.append([rollSubcodeSemMap[roll][subCode][1], feedbackType])
  return rollFeedbackMap

def feedback_not_submitted():
  output_file_name = os.path.join(pwd, "course_feedback_remaining.xlsx")
  if os.path.exists(output_file_name):
    os.remove(output_file_name)

  wb = openpyxl.Workbook()
  sheet = wb.active
  sheet.append(["rollno", "reg_sem", "schedule_sem", "subno", "name", "email", "aemail", "contact"])

  for roll in rollSubcodeSemMap:
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
    for subCode in rollSubcodeSemMap[roll]:
      regSem = rollSubcodeSemMap[roll][subCode][0]
      currentSem = rollSubcodeSemMap[roll][subCode][1]
      if roll not in rollFeedbackMap:
        if subCode.strip() not in ["NSO", "NSS"] and len(idealSubFeedbackEntriesMap[subCode]) > 0:
          sheet.append([roll,regSem, currentSem, subCode, name, email, aemail, contact])

      elif subCode not in rollFeedbackMap[roll].keys():
        if subCode in idealSubFeedbackEntriesMap and len(idealSubFeedbackEntriesMap[subCode]) > 0:
          sheet.append([roll,regSem, currentSem, subCode, name, email, aemail, contact])
      else:
        lsss = sorted(rollFeedbackMap[roll][subCode])
        newList = []
        for sth in lsss:
          for ftype in sth:
            ind = 0
            if ftype not in newList:
              newList.append(sth[1])
            ind += 1
        if sorted(newList) != sorted(idealSubFeedbackEntriesMap[subCode]) and len(idealSubFeedbackEntriesMap[subCode]) > 0:
          sheet.append([roll,regSem, currentSem, subCode, name, email, aemail, contact])
  wb.save(output_file_name)


prepStudInfoMap()
prepRollSubcodeSemMap()
subFeedbackInfo()
prepRollFeedbackMap()
feedback_not_submitted()
