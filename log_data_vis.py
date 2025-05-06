import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import matplotlib.gridspec as gridspec

def visualize_user_traces(json_path, users=None, output_path='user_trace_diagram.png', show_assistant_actions=False):
    # Load data
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # If users is None, use all users in the data
    if users is None:
        users = list(data.keys())
    
    # Define color mapping for tags
    tag_colors = {
        # Student tags - Blue family
        'Question Prompt': '#1E88E5',  # Primary blue
        'Question Summary': '#64B5F6',  # Lighter blue
        'Request': '#D5FFFF',  # Lightest blue
        
        # Student tags - Purple family
        'Exploration': '#7E57C2',  # Primary purple
        'Clarification': '#B39DDB',  # Lighter purple
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

    # Prepare the plot with gridspec for legends
    fig = plt.figure(figsize=(18, max(4, len(users))))
    gs = gridspec.GridSpec(1, 2, width_ratios=[5, 1], wspace=0.05)
    ax = fig.add_subplot(gs[0])
    legend_ax = fig.add_subplot(gs[1])
    legend_ax.axis('off')

    y_ticks = []
    y_labels = []
    
    # Pre-create legend handles in the desired order
    legend_handles_student = []
    legend_handles_assistant = []
    
    # Create legend handles in the order of tag_colors
    for tag, color in tag_colors.items():
        if tag in ['Question Prompt', 'Question Summary', 'Request', 'Exploration', 
                  'Clarification', 'Partial Solution', 'Pseudocode Solution', 'Error Message']:
            legend_handles_student.append(mpatches.Patch(facecolor=color, edgecolor='black', label=tag))
        elif tag in ['Solution', 'Leading Question', 'Feedback', 'Unrelated']:
            legend_handles_assistant.append(mpatches.Patch(facecolor=color, edgecolor='none', label=tag))
    
    # Group users by their tutors
    tutor_groups = {}
    for user in users:
        messages = data.get(user, [])
        tutor = messages[0].get('tutor', 'Unknown') if messages else 'Unknown'
        if tutor not in tutor_groups:
            tutor_groups[tutor] = []
        tutor_groups[tutor].append(user)
    
    # Sort tutors alphabetically
    sorted_tutors = sorted(tutor_groups.keys())
    
    # Create a divider line between tutor groups
    divider_y = []
    current_y = 0
    
    for tutor in sorted_tutors:
        group_users = tutor_groups[tutor]
        for user in group_users:
            messages = data.get(user, [])
            y = current_y
            y_ticks.append(y)
            y_labels.append(f"{user}\n({tutor})")
            
            # Track the actual x position for messages
            x_pos = 0
            for msg in messages:
                tag = msg.get('tag', '')
                role = msg.get('role', '')
                
                # Skip assistant messages if show_assistant_actions is False
                if not show_assistant_actions and role == 'assistant':
                    continue
                    
                color = tag_colors.get(tag, '#9E9E9E')  # Use gray for unknown tags
                rect = plt.Rectangle((x_pos, y-0.4), 1, 0.8, color=color, ec='black' if role=='student' else 'none', lw=0.5 if role=='student' else 1.5)
                ax.add_patch(rect)
                x_pos += 1
            
            current_y += 1
        
        # Add a divider line after each tutor group
        if tutor != sorted_tutors[-1]:  # Don't add divider after the last group
            divider_y.append(current_y - 0.5)
            ax.axhline(y=current_y - 0.5, color='gray', linestyle='--', alpha=0.5)

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=12, fontweight='bold')
    ax.set_xlabel('Message Order', fontsize=14)
    ax.set_title('Trace Diagram of User Messages', fontsize=16, fontweight='bold')
    ax.set_xlim(-1, max((len([m for m in data.get(u, []) if show_assistant_actions or m.get('role') != 'assistant']) for u in users), default=1) + 1)
    ax.set_ylim(-1, len(users))

    # Place both legends in the legend_ax, stacked vertically
    legend1 = legend_ax.legend(
        handles=legend_handles_student,
        title='Student Tags',
        loc='upper left',
        frameon=True
    )
    legend_ax.add_artist(legend1)
    
    # Only show assistant legend if show_assistant_actions is True
    if show_assistant_actions:
        legend2 = legend_ax.legend(
            handles=legend_handles_assistant,
            title='Assistant Tags',
            loc='lower left',
            frameon=True
        )

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"Trace diagram saved to {output_path}")

if __name__ == '__main__':
    visualize_user_traces('user_messages.json', None, show_assistant_actions=False)
