import pandas as pd
import streamlit as st

def sort_options(options):
    """
    Sorts options numerically if possible, otherwise alphabetically.
    Assumes options are provided as strings.
    """
    try:
        # Try converting all options to float for numeric sort.
        numeric_options = [float(option) for option in options]
        sorted_options = [str(x) for x in sorted(numeric_options)]
    except ValueError:
        sorted_options = sorted(options)
    return sorted_options

st.title("Know Your Lecture's Schedule in Minutes!")

# 1) File uploader with allowed extensions
uploaded_file = st.file_uploader(
    "Upload your file", 
    type=["xls", "xlsx", "csv"], 
    accept_multiple_files=False
)

if uploaded_file is not None:
    # Read file without a header (we'll set header manually later)
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, header=None)
    else:
        df = pd.read_excel(uploaded_file, header=None)

    st.success("✅ File uploaded successfully!")
    st.write("### Raw Data Preview (first 10 rows):")
    st.dataframe(df.head(10))

    # 2) Choose which row contains the column headers (1-based index)
    header_row = st.number_input(
        "Select the row number (1-10) that contains the column names:",
        min_value=1,
        max_value=10,
        value=1
    ) - 1  # convert to 0-based index

    # 3) Set the column headers using the selected row and ensure they're strings
    df.columns = df.iloc[header_row].astype(str)
    df = df[header_row + 1:].reset_index(drop=True)

    st.write("### Data Preview after setting headers:")
    st.dataframe(df.head(10))

    # -------------------------
    # Selections for filtering
    # -------------------------

    # Step 1: Semester column selection
    semester_option = st.selectbox(
        "1. Select the column name that contains 'Semester Number':",
        options=sort_options(list(df.columns))
    )

    # Step 2: Select a semester value from the chosen column
    if semester_option:
        semester_value = st.selectbox(
            "Select your Semester:",
            options=sort_options([str(val) for val in df[semester_option].unique()])
        )

    # Step 3: Section column selection
    section_option = st.selectbox(
        "2. Select the column name that contains your 'Section Number' [Core/Elective]:",
        options=sort_options(list(df.columns))
    )

    # Step 4: Select a section value (filtering on the chosen semester)
    if section_option:
        subset_df = df[df[semester_option] == semester_value]
        section_value = st.selectbox(
            "Select your required [Core/Elective] Section:",
            options=sort_options([str(val) for val in subset_df[section_option].unique()])
        )

    # Step 5: School column selection
    school_option = st.selectbox(
        "3. Select the column name that contains your School Name (e.g. SCSE, SBAS, etc.):",
        options=sort_options(list(df.columns))
    )

    # Step 6: Select a school value (filtering on the chosen semester & section)
    if school_option:
        subset_df = df[
            (df[semester_option] == semester_value) &
            (df[section_option] == section_value)
        ]
        school_value = st.selectbox(
            "Select your School:",
            options=sort_options([str(val) for val in subset_df[school_option].unique()])
        )

    # Final filtered DataFrame output
    if school_value:
        st.write("### 🎯 Schedules filtered based on your selections:")
        final_df = df[
            (df[semester_option] == semester_value) &
            (df[section_option] == section_value) &
            (df[school_option] == school_value)
        ]

        st.dataframe(final_df)
        st.write(f"✅ Total rows matching your criteria: **{len(final_df)}**")

        # Let user select columns for the final CSV export
        selected_columns = st.multiselect(
            "📌 Select the columns you want in the final CSV:",
            options=list(final_df.columns),
            default=list(final_df.columns)
        )

        # Download button for CSV export
        if selected_columns:
            csv_data = final_df[selected_columns].to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download your schedule as CSV File",
                data=csv_data,
                file_name="filtered_results.csv",
                mime="text/csv"
            )

            st.write(
                f"Rows in output may contain other classes with the same Section, "
                f"but it's easier to read **{len(final_df)} rows** instead of **{len(df)} rows**."
            )
else:
    st.info("📌 Drag & drop or click to upload a file (xls, xlsx, csv).")



























# import pandas as pd
# import streamlit as st

# def sort_options(options):
#     """
#     Sorts options numerically if possible, otherwise alphabetically.
#     Assumes options are provided as strings.
#     """
#     try:
#         # Try converting all options to float for numeric sort.
#         numeric_options = [float(option) for option in options]
#         sorted_options = [str(x) for x in sorted(numeric_options)]
#     except ValueError:
#         sorted_options = sorted(options)
#     return sorted_options

# st.title("Know Your Lecture's Schedule in Minutes !")

# # File uploader with allowed extensions
# uploaded_file = st.file_uploader("Upload your file", type=["xls", "xlsx", "csv"], accept_multiple_files=False)

# if uploaded_file is not None:
#     # Determine file type and read accordingly
#     if uploaded_file.name.endswith(".csv"):
#         df = pd.read_csv(uploaded_file)
#     else:
#         df = pd.read_excel(uploaded_file)
    
#     st.success("✅ File uploaded successfully!")
#     st.write("### Preview of Data:")
#     st.dataframe(df.head())

#     # Step 1: Choose the semester column using first-row value as display (sorted)
#     semester_option = st.selectbox(
#         "1. View the 'Preview of Data' & select the column name, that you think contain 'Semester Number'", 
#         options=sort_options([str(df.iloc[0][col]) for col in df.columns])
#     )
#     # Map the selected display value back to the actual column
#     semester_col = next((col for col in df.columns if str(df.iloc[0][col]) == semester_option), None)

#     # Step 2: Select a semester value from the chosen column (display only the value, sorted)
#     if semester_col:
#         semester_value = st.selectbox(
#             "Select your Semester:", 
#             options=sort_options([str(val) for val in df[semester_col].unique()])
#         )

#     # Step 3: Choose the core section column (display only first-row value, sorted)
#     section_option = st.selectbox(
#         "2. View the 'Preview of Data' & select the column name, that you think contain Your 'Section Number' [Core/Elective]", 
#         options=sort_options([str(df.iloc[0][col]) for col in df.columns])
#     )
#     section_col = next((col for col in df.columns if str(df.iloc[0][col]) == section_option), None)

#     # Step 4: Select the core section value (display only the value, sorted)
#     if section_col:
#         section_value = st.selectbox(
#             "Select your required [Core/Elective] Section", 
#             options=sort_options([str(val) for val in df[df[semester_col] == semester_value][section_col].unique()])
#         )

#     # Step 5: Choose the school name column (display only the first-row value, sorted)
#     school_option = st.selectbox(
#         "3. View the 'Preview of Data' & select the column name, that you think contain your `School Name (eg. SCSE, SBAS, etc)' [Don't get confused by Faculty's School Name as it may lead to false output]", 
#         options=sort_options([str(df.iloc[0][col]) for col in df.columns])
#     )
#     school_col = next((col for col in df.columns if str(df.iloc[0][col]) == school_option), None)

#     # Step 6: Select the school value (display only the value, sorted)
#     if school_col:
#         school_value = st.selectbox(
#             "Select your School:", 
#             options=sort_options([
#                 str(val) for val in df[
#                     (df[semester_col] == semester_value) & 
#                     (df[section_col] == section_value)
#                 ][school_col].unique()
#             ])
#         )

#     # ✅ Final filtered DataFrame output — shows all rows that match the selections
#     if school_value:
#         st.write("### 🎯 Schedules as per you Requirement is Filtered")
#         final_df = df[
#             (df[semester_col] == semester_value) & 
#             (df[section_col] == section_value) & 
#             (df[school_col] == school_value)
#         ]
        
#         st.dataframe(final_df)
#         st.write(f"✅ Total rows matching your criteria: **{len(final_df)}**")

#         # Create a mapping: column name -> its first row value (as string)
#         col_mapping = {col: str(df.iloc[0][col]) for col in final_df.columns}

#         # Here, we do NOT sort the final columns multiselect.
#         # They appear in the same order as they exist in final_df.
#         selected_display = st.multiselect(
#             "📌 Select the columns you want in the final CSV [Cross [x] out irrelevent column which will not help you to find your class, to make result concise", 
#             options=list(col_mapping.values()),       # Not sorted
#             default=list(col_mapping.values())        # Not sorted
#         )
#         # Map the selected display values back to the original column names
#         selected_columns = [col for col, disp in col_mapping.items() if disp in selected_display]

#         # Download button for CSV export (with selected columns)
#         if selected_columns:
#             csv_data = final_df[selected_columns].to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="📥 Download your schedule as CSV File",
#                 data=csv_data,
#                 file_name="filtered_results.csv",
#                 mime="text/csv"
#             )
#             st.write(f"Rows in output may contain another classes as well which might have same Section, but it's easy to read **{len(final_df)} rows** rather than **{len(df)} rows**")
# else:
#     st.info("📌 Drag & drop or click to upload a file (xls, xlsx, csv)")
