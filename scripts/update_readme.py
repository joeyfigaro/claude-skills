#!/usr/bin/env python3
"""
Generate README.md from skill definitions.

Scans for */SKILL.md files, parses frontmatter, and creates a table of skills.
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict
import yaml


def find_skill_files(root_dir: str = ".") -> List[Path]:
    """Find all SKILL.md files in subdirectories."""
    root_path = Path(root_dir)
    skill_files = []

    for item in root_path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            skill_file = item / "SKILL.md"
            if skill_file.exists():
                skill_files.append(skill_file)

    return skill_files


def parse_frontmatter(file_path: Path) -> Dict[str, str]:
    """Extract YAML frontmatter from a skill file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match YAML frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter_text = match.group(1)
    try:
        return yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError:
        return {}


def is_auto_invoked(description: str) -> bool:
    """Determine if a skill is auto-invoked based on description keywords."""
    if not description:
        return False

    keywords = ['always', 'automatically', 'every']
    description_lower = description.lower()
    return any(keyword in description_lower for keyword in keywords)


def generate_command(skill_name: str, description: str) -> str:
    """Generate the command/invocation string for a skill."""
    if is_auto_invoked(description):
        return "Auto-invoked"
    return f"/{skill_name}"


def generate_readme(skills: List[Dict[str, str]]) -> str:
    """Generate README content from skill data."""
    # Sort skills alphabetically by name
    skills.sort(key=lambda x: x['name'].lower())

    readme = """# Skills

This repository contains Claude Code skills. The README is automatically generated from skill definitions.

## Available Skills

| Skill | Description | Command |
|-------|-------------|---------|
"""

    for skill in skills:
        name = skill['name']
        description = skill['description']
        path = skill['path']
        command = generate_command(name, description)

        # Escape pipe characters in description
        description = description.replace('|', '\\|')

        # Create markdown link to skill file
        skill_link = f"[{name}]({path})"

        readme += f"| {skill_link} | {description} | {command} |\n"

    # Add footer with timestamp
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    readme += f"\n---\n*Last updated: {timestamp}*\n"

    return readme


def main():
    """Main entry point."""
    # Find all skill files
    skill_files = find_skill_files()

    if not skill_files:
        print("No skill files found.")
        return

    # Parse each skill file
    skills = []
    for skill_file in skill_files:
        frontmatter = parse_frontmatter(skill_file)

        if 'name' in frontmatter and 'description' in frontmatter:
            skills.append({
                'name': frontmatter['name'],
                'description': frontmatter['description'],
                'path': str(skill_file)
            })
            print(f"Found skill: {frontmatter['name']}")
        else:
            print(f"Warning: {skill_file} missing name or description in frontmatter")

    if not skills:
        print("No valid skills found.")
        return

    # Generate and write README
    readme_content = generate_readme(skills)
    readme_path = Path("README.md")

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"\nGenerated README.md with {len(skills)} skill(s)")


if __name__ == '__main__':
    main()
