import datetime
from .models import DoctorAppointment


def calculate_available_slots(doctor_id, schedules):
    # Define the time slot duration (e.g., 30 minutes)
    slot_duration = datetime.timedelta(minutes=30)

    # Retrieve existing appointments for the doctor
    existing_appointments = DoctorAppointment.objects.filter(doctor_id=doctor_id)

    # Set the range of days you want to show the available slots for (e.g., 7 days)
    range_days = 7
    today = datetime.date.today()
    range_start = datetime.datetime.combine(today, datetime.time.min)
    range_end = range_start + datetime.timedelta(days=range_days)

    # Initialize the list of available slots
    available_slots = []

    for schedule in schedules:
        # Convert the day_of_week string to a weekday integer (0 = Monday, 6 = Sunday)
        day_of_week = day_of_week_string_to_int(schedule["day_of_week"])

        # Calculate the date of the next occurrence of the scheduled day
        current_date = today + datetime.timedelta((day_of_week - today.weekday()) % 7)

        # Convert string times to datetime.time objects
        start_time = datetime.datetime.strptime(
            schedule["start_time"], "%H:%M:%S"
        ).time()
        end_time = datetime.datetime.strptime(schedule["end_time"], "%H:%M:%S").time()
        break_start_time = datetime.datetime.strptime(
            schedule["break_start_time"], "%H:%M:%S"
        ).time()
        break_end_time = datetime.datetime.strptime(
            schedule["break_end_time"], "%H:%M:%S"
        ).time()

        while current_date <= range_end.date():
            # Calculate the start and end times of the working hours for the current date
            work_start = datetime.datetime.combine(current_date, start_time)
            work_end = datetime.datetime.combine(current_date, end_time)

            # Generate time slots within the working hours
            slot_start = work_start
            while slot_start + slot_duration <= work_end:
                # Check if the slot overlaps with the break time
                # Check if the slot overlaps with the break time
                break_start = datetime.datetime.combine(current_date, break_start_time)
                break_end = datetime.datetime.combine(current_date, break_end_time)
                if slot_start >= break_start and slot_start < break_end:
                    slot_start = break_end
                    continue

                # Check if the slot overlaps with an existing appointment
                slot_end = slot_start + slot_duration
                overlapping_appointments = existing_appointments.filter(
                    appointment_start_time__lt=slot_end,
                    appointment_end_time__gt=slot_start,
                )

                if not overlapping_appointments.exists():
                    available_slots.append({"start": slot_start, "end": slot_end})

                slot_start += slot_duration

            current_date += datetime.timedelta(days=7)

    return available_slots


def day_of_week_string_to_int(day_of_week):
    days = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }
    return days.get(day_of_week)
