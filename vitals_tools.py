"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Returns a list of the systolic readings from the encounter records."""
    # collect the systolic value of every encounter into one list.

    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    """Returns the average of all systolic blood pressures."""
    # return None when there is nothing to average, then sum() / len().
    total = 0
    if not readings:
        return None
    for reading in readings:
        total += reading
    return total/len(readings)


def count_patients(encounters):
    """We return the count of unique patients/"""
    #collect the patient IDs and keep only the distinct ones.
    unique_patients = set()
    for encounter in encounters:
        unique_patients.add(encounter["patient_id"])
    return len(unique_patients)

        
def patients_at_or_above(encounters, cutoff):
    """ Returns a list of patients above a blood pressure cutoff."""
    # Keep each patient whose systolic reading is at or above cutoff.
    patients_kept = set()
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            patients_kept.add(encounter["patient_id"])
    return patients_kept
