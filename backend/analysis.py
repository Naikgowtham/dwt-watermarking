import os
import re
from datetime import datetime
from collections import defaultdict

def parse_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    results = []
    
    for line in lines[2:]: # Skip header lines
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) == 3:
            image_name, nc_str, ber_str = parts[0], parts[1], parts[2]
            # Extract the base image name
            base_image_name_match = re.match(r'([a-f0-9]+)_wm', image_name)
            if base_image_name_match:
                base_image_name = base_image_name_match.group(1)
                results.append({"image": base_image_name, "nc": nc_str, "ber": ber_str})
            
    return results

def main():
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    files = [f for f in os.listdir(results_dir) if f.startswith('nc_ber_')]
    
    data = defaultdict(list)
    
    for f in sorted(files):
        attack_type = f.replace('nc_ber_', '').replace('.txt', '').replace('_', ' ').title()
        results = parse_file(os.path.join(results_dir, f))
        
        for result in results:
            data[result['image']].append({"attack": attack_type, "nc": result['nc'], "ber": result['ber']})
            
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(results_dir, f"analysis_summary_{timestamp}.txt")
    
    with open(output_filename, 'w') as out_file:
        out_file.write(f"{'Image':<20} {'Attack':<20} {'NC':<15} {'BER':<15}\n")
        out_file.write("=" * 70 + "\n")
        
        for image, attacks in data.items():
            out_file.write(f"Results for image: {image}\n")
            for attack_data in attacks:
                 out_file.write(f"  {attack_data['attack']:<18} | NC: {attack_data['nc']:<10} | BER: {attack_data['ber']:<10}\n")
            out_file.write("-" * 70 + "\n")

    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    main()
