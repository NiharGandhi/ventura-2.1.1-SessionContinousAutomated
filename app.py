import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import pandas as pd
import base64

# Check if the Firebase app is already initialized
if not firebase_admin._apps:
    # Initialize Firebase app
    cred = credentials.Certificate('<Replace with your service account key file>')  
    firebase_admin.initialize_app(cred, {
        'databaseURL': '<Replace with your Firebase project's URL>'
    })

# Rest of the code for Streamlit web app
def main():
    st.title('Attendance Viewer')

    # Function to fetch attendance data from Firebase based on filters
    def get_attendance_data(filter_year, filter_month, filter_day):
        ref = db.reference('/attendance')
        attendance_data = ref.get()

        if attendance_data is None:
            return None

        filtered_data = []
        for year, year_data in attendance_data.items():
            if year != filter_year:
                continue

            for month, month_data in year_data.items():
                if month.lower() != filter_month.lower():
                    continue

                if filter_day != 'All' and filter_day.capitalize() not in month_data.keys():
                    continue

                day_data = month_data.get(filter_day.capitalize())
                if day_data is None:
                    continue

                for name, records in day_data.items():
                    # Check if there are any records available for a particular day
                    if isinstance(records, dict):
                        # Take the first entry as Clock In and the last entry as Clock Out
                        clock_in_record = list(records.values())[0]
                        clock_out_record = list(records.values())[-1]
                        filtered_data.append(clock_in_record)
                        filtered_data.append(clock_out_record)

        return filtered_data

    # Get distinct years, months, and days from the database
    ref = db.reference('/attendance')
    attendance_data = ref.get()
    if attendance_data is not None:
        years = sorted(list(attendance_data.keys()))
        months = sorted(list(set(month.lower() for year in attendance_data.values() for month in year.keys())))
        days = sorted(list(set(day for year in attendance_data.values() for month in year.values() for day in month.keys())))
    else:
        years = []
        months = []
        days = []

    # Display filters
    filter_year = st.selectbox('Filter by Year', ['All'] + years)
    if filter_year != 'All':
        ref = db.reference(f'/attendance/{filter_year}')
        year_data = ref.get()
        if year_data is not None:
            months = sorted(list(year_data.keys()))
        else:
            months = []
        filter_month = st.selectbox('Filter by Month', ['All'] + months)
    else:
        filter_month = 'All'

    if filter_month != 'All':
        ref = db.reference(f'/attendance/{filter_year}/{filter_month.capitalize()}')
        month_data = ref.get()
        if month_data is not None:
            days = sorted(list(month_data.keys()))
        else:
            days = []
        filter_day = st.selectbox('Filter by Day', ['All'] + days)
    else:
        filter_day = 'All'

    if st.button('Get Attendance'):
        attendance_data = get_attendance_data(filter_year, filter_month, filter_day)
        if attendance_data is None or len(attendance_data) == 0:
            st.info('No attendance records found.')
        else:
            df = pd.DataFrame(attendance_data)
            st.dataframe(df)

            # Get the date of the attendance record
            if filter_day == 'All':
                date_str = 'All'
            else:
                date_str = datetime.datetime.strptime(f"{filter_month} {filter_day}, {filter_year}", "%B %d, %Y").strftime("%Y-%m-%d")

            # Create a button to download the filtered data as a CSV file
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="attendance_{date_str}.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
