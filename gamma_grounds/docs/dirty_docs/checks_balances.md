When loading new data run this to check for duplicate report_id:

existing_ids = set(df['report_id'])
new_data = new_data[~new_data['report_id'].isin(existing_ids)]

Check which incidents are apart of aggregated data:
Trace back from aggregated data to original incidents
panel_row = panel_df[(panel_df['date'] == '2024-01-01') & (panel_df['npu_id'] == 'NPU-M')]
"Which specific crimes contributed to this count?"
original_crimes = incidents_df[
    (incidents_df['report_id'].isin(trace_ids)) &
    (incidents_df['date'] == '2024-01-01')
]

For auditing (maybe some other way as report_id's arent a huge help)...maybe create a new id that includes date, year, hour_block?

 "Show me the 5 crimes that occurred in NPU-M on 2024-01-01 at 3am"
df[df['report_id'].isin(['123456', '123457', ...])]