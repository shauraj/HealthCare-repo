# HealthCare-repo

A small, menu-driven patient management application written in Python. It uses only the Python standard library and stores records in memory while the program is running.

## Requirements

Python 3.10 or newer.

## Run

```sh
python app.py
```

Choose an option from the menu to:

- Admit a patient and receive a patient ID.
- Assign a doctor to a patient.
- Generate a bill with an amount and description.
- Print a patient summary report with billing totals.
- Print the list of admitted patients.

Patient IDs are assigned sequentially (for example, `P0001`). Data is not saved after exiting the application.

## Use as a module

`HospitalManager` provides the same operations for use from other Python code:

```python
from decimal import Decimal
from app import HospitalManager

hospital = HospitalManager()
patient = hospital.admit_patient("Jordan Lee", 34, "Observation")
hospital.assign_doctor(patient.patient_id, "Dr. Patel")
hospital.generate_bill(patient.patient_id, Decimal("125.50"), "Consultation")
print(hospital.generate_summary_report(patient.patient_id))
hospital.print_patients()
```
