from vitals_tools import (
    count_patients, mean_systolic, patients_at_or_above, systolic_readings,
)

sample = [
    {"patient_id": "P1", "visit_date": "2026-03-02", "systolic": 120},
    {"patient_id": "P2", "visit_date": "2026-03-02", "systolic": 150},
    {"patient_id": "P1", "visit_date": "2026-03-05", "systolic": 160},
]

readings = systolic_readings(sample)
print(readings)
print(mean_systolic(readings))
print(mean_systolic([]))
print(count_patients(sample))
print(patients_at_or_above(sample, 140))