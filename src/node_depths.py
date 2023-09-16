import os
import yaml
import re

def get_topic_list(directory, topic_name, depth_of_research):
    researched = []
    skipped = []

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            # Extract the title of the .md file
            topic = re.sub(r'\.md$', '', filename)

            with open(os.path.join(directory, filename), 'r') as file:
                # Extract the frontmatter
                frontmatter = re.match(r'^---\n(.+?)\n---', file.read(), re.DOTALL)

                if frontmatter:
                    yaml_content = yaml.safe_load(frontmatter.group(1))

                    if 'node_depth' in yaml_content and topic_name in yaml_content['node_depth']:
                        # Get the depth level
                        node_depth = int(yaml_content['node_depth'].split(' -> ')[1])

                        if node_depth <= depth_of_research:
                            researched.append(topic)
                        elif topic in researched and node_depth > depth_of_research:
                            researched.remove(topic)
                        else:
                            skipped.append(topic)
    

    
    return researched, skipped

if __name__ == "__main__":
    r, s = get_topic_list('/Users/erik/Documents/Obsidian/research', 'Quantum Mechanics', 1)
    print(r)
    print(f"Number of topics about to be researched: {len(r)}. Nodes left unexplored for now: {len(s)}")
    print(s)