def get_input(prompt, optional=False, valid_values=None, validation_func=None):
    while True:
        user_input = input(prompt).strip()
        if optional and user_input == "":
            return None
        if valid_values and user_input not in valid_values:
            print(f"Invalid input. Please enter one of the following: {', '.join(valid_values)}")
        elif validation_func and not validation_func(user_input):
            print("Invalid input. Please enter a valid value.")
        else:
            return user_input

def validate_time(time_str):
    # Simple validation for time format (e.g., -24h, -7d, -1m, now)
    if time_str in ["now"]:
        return True
    if time_str.startswith("-") and (time_str.endswith("h") or time_str.endswith("d") or time_str.endswith("m")):
        try:
            int(time_str[1:-1])
            return True
        except ValueError:
            return False
    return False

def generate_query():
    print("Splunk Away !! New User ver 2.0\n")

    # Basic inputs
    index = get_input("Enter the index: ")
    sourcetype = get_input("Enter the sourcetype: ")
    keyword = get_input("Enter the keyword to search for (optional): ", optional=True)
    earliest = get_input("Enter the earliest time (e.g., -24h, -7d, -1m): ", validation_func=validate_time)
    latest = get_input("Enter the latest time (e.g., now, -1h, -1d): ", validation_func=validate_time)
    
    # Start building the query
    query = f'index={index} sourcetype={sourcetype}'
    if keyword:
        query += f' "{keyword}"'
    query += f' earliest={earliest} latest={latest}'

    # Advanced options
    advanced_option = get_input("Do you want to add advanced options? (yes/no): ", valid_values=["yes", "no"]).lower()
    if advanced_option == 'yes':
        print("\nAdvanced Options:")
        
        # Field extraction
        fields = get_input("Enter fields to extract (comma-separated, optional): ", optional=True)
        if fields:
            query += f' | fields {fields}'
        
        # Statistics and aggregation
        stats_option = get_input("Do you want to add statistics or aggregation? (yes/no): ", valid_values=["yes", "no"]).lower()
        if stats_option == 'yes':
            stats_type = get_input("Enter stats type (count, avg, sum, max, min, etc.): ")
            stats_field = get_input(f"Enter field for {stats_type}: ")
            group_by = get_input("Enter field to group by (optional): ", optional=True)
            if group_by:
                query += f' | stats {stats_type}({stats_field}) by {group_by}'
            else:
                query += f' | stats {stats_type}({stats_field})'
        
        # Timechart
        timechart_option = get_input("Do you want to add a timechart? (yes/no): ", valid_values=["yes", "no"]).lower()
        if timechart_option == 'yes':
            timechart_span = get_input("Enter time span (e.g., 1h, 1d): ")
            timechart_field = get_input("Enter field for timechart: ")
            timechart_stat = get_input("Enter statistic (count, avg, etc.): ")
            query += f' | timechart span={timechart_span} {timechart_stat}({timechart_field})'
        
        # Join
        join_option = get_input("Do you want to add a join? (yes/no): ", valid_values=["yes", "no"]).lower()
        if join_option == 'yes':
            join_index = get_input("Enter index for join: ")
            join_sourcetype = get_input("Enter sourcetype for join: ")
            join_field = get_input("Enter field to join on: ")
            query += f' | join type=inner {join_field} [ search index={join_index} sourcetype={join_sourcetype} ]'
        
        # Transaction
        transaction_option = get_input("Do you want to add a transaction? (yes/no): ", valid_values=["yes", "no"]).lower()
        if transaction_option == 'yes':
            start_with = get_input("Enter start condition: ")
            end_with = get_input("Enter end condition: ")
            transaction_field = get_input("Enter field to group by: ")
            query += f' | transaction startswith="{start_with}" endswith="{end_with}" by {transaction_field}'
        
        # Subsearch
        subsearch_option = get_input("Do you want to add a subsearch? (yes/no): ", valid_values=["yes", "no"]).lower()
        if subsearch_option == 'yes':
            subsearch = get_input("Enter your subsearch query: ")
            query += f' [ search {subsearch} ]'
        
        # Conditional evaluation
        eval_option = get_input("Do you want to add a conditional evaluation? (yes/no): ", valid_values=["yes", "no"]).lower()
        if eval_option == 'yes':
            eval_statement = get_input("Enter your eval statement (e.g., eval new_field=if(condition, true_value, false_value)): ")
            query += f' | eval {eval_statement}'
        
        # Regex extraction
        rex_option = get_input("Do you want to add a regex extraction? (yes/no): ", valid_values=["yes", "no"]).lower()
        if rex_option == 'yes':
            rex_field = get_input("Enter the field to apply regex on: ")
            rex_pattern = get_input("Enter your regex pattern: ")
            query += f' | rex field={rex_field} "{rex_pattern}"'
        
        # Lookups
        lookup_option = get_input("Do you want to add a lookup? (yes/no): ", valid_values=["yes", "no"]).lower()
        if lookup_option == 'yes':
            lookup_table = get_input("Enter the lookup table name: ")
            lookup_fields = get_input("Enter the lookup fields (comma-separated): ")
            query += f' | lookup {lookup_table} {lookup_fields}'

    print("\nGenerated Splunk Query:")
    print(query)

if __name__ == "__main__":
    generate_query()
