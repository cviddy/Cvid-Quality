def write_results_to_local_file(hotfix_dates_urls):
    """
    Writes results ot a local file
    
    :param hotfix_date_urls:
    """

    with open('results.txt', 'a') as file:

        # DELETE old contents of results
        file.seek(0)
        file.truncate()

        # Add new
        for hotfix in hotfix_dates_urls:
            file.write(hotfix + "\n")
    