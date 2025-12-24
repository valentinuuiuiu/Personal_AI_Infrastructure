---
name: Blogging
description: |
  A skill for creating and publishing blog posts.

  This skill automates the entire blogging workflow, from drafting a post on a given topic to publishing it to the Eleventy blog.
USE WHEN: The user wants to create or publish a blog post.

WORKFLOWS:
- draft: Creates a new blog post draft from a topic.
- publish: Publishes an existing draft to the blog.
---

# Blogging Skill

This skill provides a complete, end-to-end solution for creating and managing blog content. It is designed to streamline the writing and publishing process, allowing the user to focus on ideas rather than the technical details of the blogging platform.

## Workflows

### Draft

The `draft` workflow is the starting point for any new blog post. It takes a user-provided topic and generates a high-quality draft, complete with appropriate frontmatter. The draft is saved to a temporary location, allowing for review and modification before publishing.

### Publish

Once a draft is finalized, the `publish` workflow handles the rest. It moves the approved content to the correct directory for the Eleventy blog, runs the build process, and makes the new post live on the site. This automated process ensures consistency and eliminates the manual steps that can often lead to errors.
