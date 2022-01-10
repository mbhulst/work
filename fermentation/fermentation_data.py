import pandas as pd
import dateutil.parser

# Which files should be formatted?
files = ["./6.xls", "./7.xls", "./8.xls", "./9.xls"]
sheet_names = ["A", "B", "C", "D"]

# Convert each excel file to a pandas data frame and edit the data

list_dfs = []  # initialize list for data frames
for file in files:
    # Import the excel file as pandas data frame
    df = pd.read_csv(file, skiprows=2, delimiter="\t")  # (skip first 2 rows)
    # Remove row that specifies the sampling rate
    df = df[1:]
    # Remove unnecessary columns by name of the column
    df = df.drop(["Time.1", "Time.2", "Time.3", "Time.4", "Time.5"], axis=1)  # choose columns(axis=1) not rows(=0)
    # Change the time column into a workable format
    df['Time'] = df['Time'].apply(lambda y: dateutil.parser.parse(y))
    # Calculate elapsed hours from time stamp & added acid & base
    time_hours = [0] * len(df['Time'])  # initialize list for time in hours column
    added_acid = [0] * len(df['Time'])  # initialize list for added acid
    added_base = [0] * len(df['Time'])  # initialize list for added base
    for time_point in range(1, len(df['Time'])):
        time_hours[time_point] = pd.Timedelta(df['Time'][time_point + 1] - df['Time'][1]).total_seconds() / 3600.0
        added_acid[time_point] = added_acid[time_point - 1] + df['Pump2'][time_point]/100  # Pump2 = acid
        added_base[time_point] = added_base[time_point - 1] + df['Pump1'][time_point]/100  # Pump1 = base
    # Add calculated values to data frame (convert list to column in data frame)
    df['Time (h)'] = time_hours
    df['Added acid'] = added_acid
    df['Added base'] = added_base
    # Rearrange columns
    df = df[["Time", "Time (h)", "pH", "DO", "Agit", "Temp", "Pump1", "Added base", "Pump2", "Added acid", "Temp"]]
    # Add data frames to the list
    list_dfs.append(df)

# Import data frames to excel output file
writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

for x in range(len(list_dfs)):
    list_dfs[x].to_excel(writer, sheet_name=sheet_names[x])

# Specify where to put the charts
workbook = writer.book  # Get the xlsxwriter workbook object.
worksheet = workbook.add_worksheet('Overview')  # Put charts in a new sheet nameed overview


# Functions that make the charts
def make_main_chart(x):
    """This function adds a chart of pH and DO data to the overview work sheet."""
    # Decide how much data should be plotted
    length = len(list_dfs[x][1:])
    # Add chart to overview sheet
    chart1 = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
    # Configure the series of the chart from the data frame data.
    chart1.add_series({
        'name': 'DO',
        'values': [sheet_names[x], 2, 4, length, 4],
        'categories': [sheet_names[x], 2, 2, length, 2],
    })
    chart1.add_series({
        'name': 'Agitation',
        'values': [sheet_names[x], 2, 5, length, 5],
        'categories': [sheet_names[x], 2, 2, length, 2],
        'y2_axis': 1  # put this data on secondary y-axis
    })
    # Add a chart title, axis labels and axis limits.
    chart1.set_title({'name': sheet_names[x]})
    chart1.set_x_axis({'name': 'Time (h)'})
    chart1.set_y_axis({'name': 'DO (%)', 'min': 0, 'max': 120})
    chart1.set_y2_axis({'name': 'Agitation (rpm)', 'min': 0, 'max': 1000})
    return chart1


def make_extra_chart(x):
    """This function adds a chart of agitation, temperature and acid/base addition to the overview work sheet."""
    # Decide how much data should be plotted
    length = len(list_dfs[x][1:])
    # Add chart to overview sheet
    chart2 = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
    # Configure the series of the chart from the data frame data.
    chart2.add_series({
        'name': 'Temperature',
        'values': [sheet_names[x], 2, 6, length, 6],
        'categories': [sheet_names[x], 2, 2, length, 2],
    })
    chart2.add_series({
        'name': 'pH',
        'values': [sheet_names[x], 2, 3, length, 3],
        'categories': [sheet_names[x], 2, 2, length, 2],
        'y2_axis': 1  # put this data on secondary y-axis
    })
    chart2.add_series({
        'name': 'Acid',
        'values': [sheet_names[x], 2, 8, length, 8],
        'categories': [sheet_names[x], 2, 2, length, 2],
        'y2_axis': 1  # put this data on secondary y-axis
    })
    chart2.add_series({
        'name': 'Base',
        'values': [sheet_names[x], 2, 10, length, 10],
        'categories': [sheet_names[x], 2, 2, length, 2],
        'y2_axis': 1  # put this data on secondary y-axis
    })
    # Add a chart title, axis labels and axis limits.
    chart2.set_title({'name': sheet_names[x]})
    chart2.set_x_axis({'name': 'Time (h)'})
    chart2.set_y_axis({'name': 'Temperature (C)', 'min': 0, 'max': 40})
    chart2.set_y2_axis({'name': 'pH, Added acid/base', 'min': 0, 'max': 8})
    return chart2


# Insert the charts into the chosen worksheet
placing = ['B2', 'K2', 'B18', 'K18']
for x in range(4):
    chart = make_main_chart(x)
    worksheet.insert_chart(placing[x], chart)

placing_extra = ['B37', 'K37', 'B53', 'K53']
for x in range(4):
    chart = make_extra_chart(x)
    worksheet.insert_chart(placing_extra[x], chart)

# Save all to the chosen excel file
writer.save()
