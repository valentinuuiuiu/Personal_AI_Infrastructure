---
name: publish
description: Publishes a blog post draft to the Eleventy blog.
args:
  - name: draft_path
    type: string
    description: The path to the draft file to be published.
---

This workflow takes a draft blog post, moves it to the `blog/posts` directory, and then builds the Eleventy site to publish the new content.

**Dependencies:**
- This workflow assumes that the `PAI_DIR` environment variable is set to the root of the PAI repository.
- It also assumes that `npm install` has been run in the `blog/` directory to install the necessary dependencies for Eleventy.

```claude-code
#!/bin/bash

# Check if the PAI_DIR environment variable is set
if [ -z "$PAI_DIR" ]; then
  echo "Error: The PAI_DIR environment variable is not set."
  exit 1
fi

# Check if the draft file exists
if [ ! -f "$1" ]; then
  echo "Error: Draft file not found at $1"
  exit 1
fi

# Move the draft to the posts directory
POST_FILENAME=$(basename "$1")
POST_PATH="${PAI_DIR}/blog/posts/$POST_FILENAME"
mv "$1" "$POST_PATH"

# Navigate to the blog directory and build the site
cd "${PAI_DIR}/blog"
npx eleventy

# Output the success message
echo "Blog post published successfully!"
echo "You can view the new post in the _site directory."
```
