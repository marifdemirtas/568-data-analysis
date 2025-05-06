import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import csv

def analyze_message_statistics(json_path, output_path='message_statistics.png', csv_path='message_statistics.csv'):
    # Load data
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    tag_colors = {
        # Student tags - Blue family
        'Question Prompt': '#1E88E5',  # Primary blue
        'Question Summary': '#64B5F6',  # Lighter blue
        'Request': '#D5FFFF',  # Lightest blue
        'Question Clarification': '#FFE0E0',  # Light red


        # Student tags - Purple family
        'Exploration': '#7E57C2',  # Primary purple
        'Clarifying Question': '#B39DDB',  # Lighter purple
        'Error Message': '#FF5722',  # Orange

        # Student tags - Teal family
        'Partial Solution': '#00897B',  # Primary teal
        'Pseudocode Solution': '#4DB6AC',  # Lighter teal
        
        # Assistant tags
        'Solution': '#43A047',  # Green
        'Leading Question': '#FFD600',  # Yellow
        'Feedback': '#FB8C00',  # Orange
        'Unrelated': '#9E9E9E'  # Gray
    }


    # Initialize statistics
    tutor_stats = defaultdict(lambda: defaultdict(int))
    total_messages = defaultdict(int)
    
    # Process each user's messages
    for user, messages in data.items():
        if not messages:
            continue
            
        tutor = messages[0].get('tutor', 'Unknown')
        
        # Count message types for this user's tutor
        for msg in messages:
            if msg.get('role') == 'student':
                tag = msg.get('tag', 'Unknown')
                tutor_stats[tutor][tag] += 1
                total_messages[tutor] += 1
    
    # Print statistics
    print("\nMessage Statistics by Tutor:")
    print("-" * 50)
    for tutor, stats in sorted(tutor_stats.items()):  # Sort tutors alphabetically
        print(f"\nTutor: {tutor}")
        print(f"Total Messages: {total_messages[tutor]}")
        print("Message Types:")
        for tag, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_messages[tutor]) * 100
            print(f"  - {tag}: {count} ({percentage:.1f}%)")
    
    # Export to CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Tutor', 'Message Type', 'Count', 'Percentage'])
        
        # Write data rows
        for tutor in sorted(tutor_stats.keys()):
            for tag, count in sorted(tutor_stats[tutor].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_messages[tutor]) * 100
                writer.writerow([tutor, tag, count, f"{percentage:.1f}%"])
    
    print(f"\nStatistics exported to {csv_path}")
    
    # Create visualization
    tutors = sorted(list(tutor_stats.keys()))  # Sort tutors alphabetically
    tags = set()
    for stats in tutor_stats.values():
        tags.update(stats.keys())
    tags = sorted(list(tags))
    
    # Prepare data for stacked bar chart
    x = np.arange(len(tutors))
    width = 0.8
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot stacked bars
    bottom = np.zeros(len(tutors))
    for i, tag in enumerate(tags):
        counts = [tutor_stats[tutor].get(tag, 0) for tutor in tutors]
        color = tag_colors.get(tag, '#9E9E9E')  # Use predefined colors, fallback to gray if not found
        ax.bar(x, counts, width, bottom=bottom, label=tag, color=color)
        bottom += counts
    
    # Customize the plot
    ax.set_ylabel('Number of Messages')
    ax.set_title('Message Types by Tutor')
    ax.set_xticks(x)
    ax.set_xticklabels(tutors, rotation=45, ha='right')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"\nStatistics visualization saved to {output_path}")

if __name__ == '__main__':
    analyze_message_statistics('user_messages.json') 