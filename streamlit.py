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

st.title("📁 File Upload: Drag & Drop or Browse")

# File uploader with allowed extensions
uploaded_file = st.file_uploader("Upload your file", type=["xls", "xlsx", "csv"], accept_multiple_files=False)

if uploaded_file is not None:
    # Determine file type and read accordingly
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("✅ File uploaded successfully!")
    st.write("### Preview of Data:")
    st.dataframe(df.head())

    # Step 1: Choose the semester column using first-row value as display (sorted)
    semester_option = st.selectbox(
        "1. Choose the column that contains your Semester:", 
        options=sort_options([str(df.iloc[0][col]) for col in df.columns])
    )
    # Map the selected display value back to the actual column
    semester_col = next((col for col in df.columns if str(df.iloc[0][col]) == semester_option), None)

    # Step 2: Select a semester value from the chosen column (display only the value, sorted)
    if semester_col:
        semester_value = st.selectbox(
            "Select your Semester value:", 
            options=sort_options([str(val) for val in df[semester_col].unique()])
        )

    # Step 3: Choose the core section column (display only first-row value, sorted)
    section_option = st.selectbox(
        "2. Choose the column that contains your Core Section:", 
        options=sort_options([str(df.iloc[0][col]) for col in df.columns])
    )
    section_col = next((col for col in df.columns if str(df.iloc[0][col]) == section_option), None)

    # Step 4: Select the core section value (display only the value, sorted)
    if section_col:
        section_value = st.selectbox(
            "Select your Core Section value:", 
            options=sort_options([str(val) for val in df[df[semester_col] == semester_value][section_col].unique()])
        )

    # Step 5: Choose the school name column (display only the first-row value, sorted)
    school_option = st.selectbox(
        "3. Choose the column that contains your School Name:", 
        options=sort_options([str(df.iloc[0][col]) for col in df.columns])
    )
    school_col = next((col for col in df.columns if str(df.iloc[0][col]) == school_option), None)

    # Step 6: Select the school value (display only the value, sorted)
    if school_col:
        school_value = st.selectbox(
            "Select your School Name value:", 
            options=sort_options([
                str(val) for val in df[
                    (df[semester_col] == semester_value) & 
                    (df[section_col] == section_value)
                ][school_col].unique()
            ])
        )

    # ✅ Final filtered DataFrame output — shows all rows that match the selections
    if school_value:
        st.write("### 🎯 Final Filtered DataFrame (All Matching Rows):")
        final_df = df[
            (df[semester_col] == semester_value) & 
            (df[section_col] == section_value) & 
            (df[school_col] == school_value)
        ]
        
        st.dataframe(final_df)
        st.write(f"✅ Total rows matching your criteria: **{len(final_df)}**")

        # Create a mapping: column name -> its first row value (as string)
        col_mapping = {col: str(df.iloc[0][col]) for col in final_df.columns}

        # Here, we do NOT sort the final columns multiselect.
        # They appear in the same order as they exist in final_df.
        selected_display = st.multiselect(
            "📌 Select the columns you want in the final CSV:", 
            options=list(col_mapping.values()),       # Not sorted
            default=list(col_mapping.values())        # Not sorted
        )
        # Map the selected display values back to the original column names
        selected_columns = [col for col, disp in col_mapping.items() if disp in selected_display]

        # Download button for CSV export (with selected columns)
        if selected_columns:
            csv_data = final_df[selected_columns].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv_data,
                file_name="filtered_results.csv",
                mime="text/csv"
            )
else:
    st.info("📌 Drag & drop or click to upload a file (xls, xlsx, csv)")
