import requests
from pandas import DataFrame

visa_url = "https://api.schengenvisaappointments.com/api/visa-list/?format=json"
message = """Available Visa Appointments:
    - Source Country: {source_country}
    - Mission Country: {mission_country}
    - Visa Type: {visa_type_id}
    - Visa Category: {visa_category}
    - Visa Subcategory: {visa_subcategory}
    - People Looking: {people_looking}
    - Center Name: {center_name}
    - Appointment Date: {appointment_date}
    - Book Now Link: {book_now_link}
    - Last Checked: {last_checked}"""


def prepare_message(row):
    return message.format(
        source_country=row["source_country"],
        mission_country=row["mission_country"],
        visa_type_id=row["visa_type_id"],
        visa_category=row["visa_category"],
        visa_subcategory=row["visa_subcategory"],
        people_looking=row["people_looking"],
        center_name=row["center_name"],
        appointment_date=row["appointment_date"],
        book_now_link=row["book_now_link"],
        last_checked=row["last_checked"]
    )


def send_message(row):
    message = row["message"]


def main():
    response = requests.get(visa_url)
    df = DataFrame(response.json())
    mission_countries = {"Greece", "Spain", "Belgium", "Netherlands", "Germany", "France", "Italy", "Portugal"}
    visa_categories = {"schengen", "short"}

    df["visa_category"] = df["visa_category"].str.lower()
    df = df.loc[
        (df["source_country"] == "Turkiye") &
        (df["mission_country"].isin(mission_countries)) &
        (df["visa_category"].apply(lambda x: any(category in x for category in
                                                 visa_categories)))
    ]

    if df.empty:
        return None

    df["message"] = df.apply(prepare_message, axis=1)



if __name__ == "__main__":
    main()
