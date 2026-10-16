from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation


@dataclass
class Bill:
    amount: Decimal
    description: str
    generated_on: date = field(default_factory=date.today)


@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    condition: str
    admitted_on: date = field(default_factory=date.today)
    doctor: str | None = None
    bills: list[Bill] = field(default_factory=list)


class HospitalManager:
    def __init__(self) -> None:
        self.patients: dict[str, Patient] = {}
        self._next_patient_number = 1

    def admit_patient(self, name: str, age: int, condition: str) -> Patient:
        if not name.strip():
            raise ValueError("Patient name cannot be empty.")
        if age <= 0:
            raise ValueError("Age must be a positive number.")

        patient_id = f"P{self._next_patient_number:04d}"
        self._next_patient_number += 1
        patient = Patient(patient_id, name.strip(), age, condition.strip())
        self.patients[patient_id] = patient
        return patient

    def assign_doctor(self, patient_id: str, doctor_name: str) -> Patient:
        patient = self._get_patient(patient_id)
        if not doctor_name.strip():
            raise ValueError("Doctor name cannot be empty.")
        patient.doctor = doctor_name.strip()
        return patient

    def generate_bill(
        self, patient_id: str, amount: Decimal, description: str
    ) -> Bill:
        patient = self._get_patient(patient_id)
        if amount < 0:
            raise ValueError("Bill amount cannot be negative.")
        if not description.strip():
            raise ValueError("Bill description cannot be empty.")

        bill = Bill(amount, description.strip())
        patient.bills.append(bill)
        return bill

    def generate_summary_report(self, patient_id: str) -> str:
        patient = self._get_patient(patient_id)
        total_billed = sum((bill.amount for bill in patient.bills), Decimal("0.00"))
        doctor = patient.doctor or "Not assigned"
        return (
            f"Patient Summary\n"
            f"ID: {patient.patient_id}\n"
            f"Name: {patient.name}\n"
            f"Age: {patient.age}\n"
            f"Condition: {patient.condition or 'Not specified'}\n"
            f"Admitted: {patient.admitted_on.isoformat()}\n"
            f"Doctor: {doctor}\n"
            f"Number of bills: {len(patient.bills)}\n"
            f"Total billed: ${total_billed:.2f}"
        )

    def print_patients(self) -> None:
        if not self.patients:
            print("No patients have been admitted.")
            return

        print("Patient list")
        print("------------")
        for patient in self.patients.values():
            doctor = patient.doctor or "Not assigned"
            print(
                f"{patient.patient_id} | {patient.name} | Age {patient.age} | "
                f"Doctor: {doctor}"
            )

    def _get_patient(self, patient_id: str) -> Patient:
        try:
            return self.patients[patient_id.strip().upper()]
        except KeyError as error:
            raise ValueError(f"Patient '{patient_id}' was not found.") from error


def read_amount(prompt: str) -> Decimal:
    try:
        return Decimal(input(prompt).strip()).quantize(Decimal("0.01"))
    except InvalidOperation as error:
        raise ValueError("Enter a valid amount, for example 125.50.") from error


def run_app() -> None:
    manager = HospitalManager()
    while True:
        print(
            "\nPatient Management\n"
            "1. Admit patient\n"
            "2. Assign doctor\n"
            "3. Generate bill\n"
            "4. Patient summary report\n"
            "5. Print patient list\n"
            "0. Exit"
        )
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                patient = manager.admit_patient(
                    input("Patient name: "),
                    int(input("Age: ")),
                    input("Condition: "),
                )
                print(f"Admitted {patient.name}. Patient ID: {patient.patient_id}")
            elif choice == "2":
                patient = manager.assign_doctor(
                    input("Patient ID: "), input("Doctor name: ")
                )
                print(f"Assigned {patient.doctor} to {patient.name}.")
            elif choice == "3":
                bill = manager.generate_bill(
                    input("Patient ID: "),
                    read_amount("Amount: $"),
                    input("Description: "),
                )
                print(f"Bill generated: ${bill.amount:.2f} ({bill.description})")
            elif choice == "4":
                print(manager.generate_summary_report(input("Patient ID: ")))
            elif choice == "5":
                manager.print_patients()
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Choose one of the listed options.")
        except (ValueError, InvalidOperation) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    run_app()
