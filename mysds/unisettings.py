PASSMARK = 40

LATE_SUBMISSION_PENALTY = 5
# Penalty (in marks) that is deducted per day if a piece of coursework is late. This will not 
# be applied automatically, but merely proposed when filling out the marksheet.

# External Examiner Packs

def sample_size(number):
    if number < 25:
        return 5
    else:
        return 10
