import os
import re
import shutil

pwd = os.getcwd()
wrongRoot = os.path.join(pwd, "wrong_srt")
correctRoot = os.path.join(pwd, "corrected_srt")

"""
Renames the files of the specified directory semantically via truncating
redundant information using Regex
Accepts
@param seriesName: Name of Web Series which needs to be renamed
@param cleanerRegex: The Regex used to truncate / strip the unnecessary
information provided unsolicitely in the raw file name
@param sznAndEpRegex: The Regex used to extract out the string which contains
the information regarding the season number and episode number of the concerned
series in process
@param uniqueSeparator: The unique separator in the string containing fused Web
Series Season plus Episode information, separated via the separator being
discussed here
"""
def generic_rename(seriesName, cleanerRegex, sznAndEpRegex, uniqueSeparator):
    print(f"Renaming '{seriesName}'...")
    seriesWrongRoot = os.path.join(wrongRoot, seriesName)
    seriesCorrectRoot = os.path.join(correctRoot, seriesName)

    if os.path.exists(seriesCorrectRoot):
        print(
            f"[INFO] destination\n{seriesCorrectRoot}\nalready exists, overwriting contents!"
        )
        shutil.rmtree(seriesCorrectRoot)
    os.mkdir(seriesCorrectRoot)

    for filename in os.listdir(seriesWrongRoot):
        rawInfo = re.split(cleanerRegex, filename)
        mergedInfo = re.split(sznAndEpRegex, rawInfo[0])
        sznAndEpList = list(map(int, re.split(uniqueSeparator, mergedInfo[1])))
        desiredFileName = (
            mergedInfo[0]
            + (" -" if webseries_num != 1 else "")
            + " Season "
            + str(sznAndEpList[0]).zfill(season_padding)
            + " Episode "
            + str(sznAndEpList[1]).zfill(episode_padding)
            + (" -" if webseries_num != 1 else "")
            + ((" " + mergedInfo[2]) if (webseries_num != 1) else "")
            + rawInfo[1]
        )

        # Remove more than "Single" spacing in the file name
        # e.g. in Season 6 & Episode 8 of Lucifer(between 'Devil' & 'Save')
        exactDesiredNameWithSingleSpacing = re.sub(" +", " ", desiredFileName)
        absIncorrectDest = os.path.join(seriesWrongRoot, filename)
        absCorrectDest = os.path.join(seriesCorrectRoot, exactDesiredNameWithSingleSpacing)
        shutil.copy(absIncorrectDest, absCorrectDest)
    print(f"Successfully renamed '{seriesName}'!!\nFind contents at:\n{seriesCorrectRoot}")
    return

def regex_renamer():
    # Taking input from the user
    print("1. Breaking Bad")
    print("2. Game of Thrones")
    print("3. Lucifer")

    global season_padding, episode_padding, webseries_num
    webseries_num = int(
        input("Enter the number of the web series that you wish to rename. 1/2/3: ")
    )
    if webseries_num > 0 and webseries_num < 4:
        season_padding = int(input("Enter the Season Number Padding: "))
        episode_padding = int(input("Enter the Episode Number Padding: "))
        if not os.path.exists(correctRoot):
            os.mkdir(correctRoot)
        if webseries_num == 1:
            generic_rename("Breaking Bad", "\s7..*dr", "\sse?", "e")
        elif webseries_num == 2:
            generic_rename("Game of Thrones", "\..*en", "\s\-\s", "x")
        elif webseries_num == 3:
            generic_rename("Lucifer", "\..*en", "\s\-\s", "x")
    else:
        print("Invalid input detected! Please enter number in specified range")


regex_renamer()
