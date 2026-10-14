#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """A Usable encounter is 
        1. it splits into 3 comma-separated fields;
        2. int() can read the third field; and
        3. the rading is from 60-250 mmHG inclusive

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    # read the rows and skip the header line.
    rows = data_path.read_text(encoding="utf-8").splitlines()
    encounters = []
    skipped = 0
    for row in rows[1:]:

    # keep a row only when it has three fields, int() can read the
    #       systolic field, and the reading is plausible.
        if not row.strip():
            print("Skipping a blank row.")
            skipped += 1
            continue
            
        fields = row.strip().split(",")
        if len(fields) != 3:
            print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
            skipped += 1
            continue
        patient_id, visit_date, raw_systolic = fields

        try:
            systolic = int(raw_systolic)
        except ValueError as error:
            print(f"Skipping {patient_id}: {error}")
            skipped += 1
            continue

        if not (60 <= systolic <= 250):
            print(f"Skipping {patient_id}: {systolic} mmHG is outside 60-250")
            skipped += 1
            continue
    # count every other data row as skipped, the blank line included,
    #       and print one line per skipped row so you can see what dropped out.
    encounters.append({
        "patient_id": patient_id,
        "visit_date": visit_date,
        "systolic": systolic,
    })
    # TODO: end with `return encounters, skipped`.
    return encounters, skipped


def main():
    """TODO: We output the vitals report as well as the follow-up list of patients."""
    encounters, skipped = read_encounters(DATA_PATH)
    readings = systolic_readings(encounters)
    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]
    report_text = "\n".join(report_lines) + "\n"

    # build the six report lines and write them to output/vitals_report.txt.
    (OUTPUT_DIR / "vitals_report.txt").write_text(report_text, encoding = "utf-8")
    
    # TODO: read the file back and print it, so you can see what was saved.
    
    print((OUTPUT_DIR / "vitals_report.txt").read_text(encoding="utf-8"), end="")

    # choose your follow-up cutoff, then write output/followup_list.txt
    #       with the Cutoff line, the Reason line, and one patient ID per line.
    cutoff = 140
    reason = "140 mmHg marks stage 2 hypertension and yields a call list the clinic can realistically complete this week."
    follow_up_lines = [
        f"Cutoff: {cutoff} mmHg",
        f"Reason: {reason}",
    ] + sorted(patients_at_or_above(encounters, cutoff))

    (OUTPUT_DIR / "followup_list.txt").write_text("\n".join(follow_up_lines) + "\n", encoding="utf-8")

    print((OUTPUT_DIR / "followup_list.txt").read_text(encoding="utf-8"), end="")

if __name__ == "__main__":
    main()
