## About
This is the code and (most) data for a research project done in CS499/579 Empirical Computer Security

There were two main goals of this research:
1. What features do threat actors look for in domain registrars?
2. Does domain pricing (like sales) influence malicious domain registration?

Pricing data has been left out due to its large size. It was a daily scrape of tld-list prices.

## Files
- `service-payment-analysis.ipynb`: Analysis of correlation between services offered + payment methods and malicious activity
- `pricing-analysis.ipynb`: Analysis of pricing data and its correlation with purchasing
- `data/`: Most of the data we used
    - `tld-list-match-registrar-by-id.csv`: Used to give 
    - `registrar_properties.csv`: Manually collected features and payment methods for some registrars
    - `registrar_domain_count.json`: Number of domains managed by each registrar (not 100% accurate)
    - `registrar_domain_count_flat.json`: Flattened version of above
    - `registrar_domain_count_flat_deduplicated.json`: Deduplicated version of above 
    - `registrar_domain_count_flat_deduplicated_links.json`: Above but shell registrars merged on common ICANN contact info
    - `all_types_domains_balanced_registered_domains_whois_parsed.json`: Reported domains put through VirusTotal for more data
    - `all_types_domains_balanced_registered_domains_whois_parsed_correct_registrar_names.json`: Above but registrar names have been corrected
    - `all_types_domains_balanced_registered_domains_whois_parsed_correct_registrar_names_deduplicated_ids.json`: Above but deduplicated
    - `all_types_domains_balanced_registered_domains_whois_parsed_correct_registrar_names_deduplicated_ids_links.json`: Above but registrars have been merged on common ICANN contact info
    - `Accredited-Registrars-202412054424.csv`: List of accredited registrars
- `cleaning/`: Data cleaning scripts
    - `condense.py`: Condense all pricing data into one file
    - `stratified_sampler.ipynb`: Didn't use this but it would randomly sample malicious registrars
    - `deduplicate_shells_by_contact.ipynb`: Deduplicate registrars based on them having identical ICANN contact info
    - `deduplicate_shell_companies.py`: Deduplicate registrars based on them having the same name when special characters and numbers are excluded
    - `flatten_domain_count_data.py`: Very small script to just flatten domain count data
    - `correct_registrar_names.py`: Fix registrar names by looking up their ID number
