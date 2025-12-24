---
name: draft
description: Creates a new blog post draft from a topic.
args:
  - name: topic
    type: string
    description: The topic of the blog post.
  - name: tags
    type: string
    description: A comma-separated list of tags for the blog post.
---

This workflow generates a high-quality draft for a blog post based on the provided topic and tags. It includes the necessary frontmatter and saves the draft to a temporary file for review before publishing.

**Dependencies:**
- This workflow uses the `claude-ai` command to generate content. If this command is not available in the system's PATH, the workflow will use placeholder text and issue a warning.

```claude-code
#!/bin/bash

# The topic of the blog post
TOPIC="$1"

# The tags for the blog post, in comma-separated format
TAGS_CSV="$2"

# Generate a unique filename for the draft
DRAFT_FILENAME="draft-$(date +%s).md"
DRAFT_PATH="$HOME/.claude/scratchpad/$DRAFT_FILENAME"

# Check for the claude-ai command and generate content
if command -v claude-ai &> /dev/null; then
    POST_CONTENT=$(claude-ai "Write a blog post about '$TOPIC'. The post should have a title, an introduction, a main body, and a conclusion. The tone should be informative and engaging.")
else
    echo "WARNING: The 'claude-ai' command was not found." >&2
    echo "This skill requires an AI command-line tool to generate content." >&2
    echo "Using placeholder content for the draft." >&2
    POST_CONTENT="This is a placeholder for the blog post content. Please replace this with the actual content."
fi

# Start creating the draft file with frontmatter
{
  echo "---"
  echo "title: \"$TOPIC\""
  echo "date: \"$(date --iso-8601=seconds)\""
  echo "tags:"

  # Split the comma-separated tags and format them as a YAML list
  IFS=',' read -ra TAGS_ARRAY <<< "$TAGS_CSV"
  for tag in "${TAGS_ARRAY[@]}"; do
    # Trim whitespace from the tag
    trimmed_tag=$(echo "$tag" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    echo "  - $trimmed_tag"
  done

  echo "---"
  echo ""
  echo "$POST_CONTENT"
} > "$DRAFT_PATH"

# Output the path to the draft file
echo "Draft created at: $DRAFT_PATH"
```
