from qradar import get_offenses, get_source_ip_and_url
from misp import add_attribute_to_existing_event, publish_event

def display_for_approval(ip_and_urls):
    print("\n--- IP AND URL LIST ---\n")
    numbered_ip_and_urls = [(i+1, ip, url) for i, (ip, url) in enumerate(ip_and_urls)]
    for num, ip, url in numbered_ip_and_urls:
        print(f"{num}. IP: {ip} | URL: {url}")
    
    approve_input = input("\nEnter the numbers you want to approve (e.g. 1, 2, 3), type 'all' or 'exit': ").strip().lower()

    if approve_input == "exit":
        print("Exiting...")
        return []
    
    try:
        if approve_input == "all":
            approved_ips_and_urls = ip_and_urls
        else:
            approved_numbers = [int(num.strip()) for num in approve_input.split(",")]
            approved_ips_and_urls = [ip_and_urls[num-1] for num in approved_numbers if 1 <= num <= len(ip_and_urls)]
    except ValueError:
        print("Invalid entry. Please enter valid numbers.")
        return []

    if approved_ips_and_urls:
        print("Approved data is processed.")
        add_attribute_to_existing_event(approved_ips_and_urls)
    else:
        print("No approved data available.")
    
    return approved_ips_and_urls

def main():
    print("\n--- Launching Script ---\n")
    
    offenses = get_offenses()
    if offenses:
        ip_and_urls = get_source_ip_and_url(offenses)
        if ip_and_urls:
            approved_ips_and_urls = display_for_approval(ip_and_urls)
            if approved_ips_and_urls:
                publish_event()
        else:
            print("No IP and URL found.")

if __name__ == "__main__":
    main()

