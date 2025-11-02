"""Template loader utilities for Amazon Connect MCP."""

import json
from pathlib import Path
from typing import Any

TEMPLATES_DIR = Path(__file__).parent


def list_templates(category: str | None = None) -> list[dict[str, Any]]:
    """List available templates, optionally filtered by category."""
    templates = []
    
    categories = {
        "cases": TEMPLATES_DIR / "cases",
        "views": TEMPLATES_DIR / "views",
        "data_tables": TEMPLATES_DIR / "data_tables",
        "routing": TEMPLATES_DIR / "routing",
        "profiles": TEMPLATES_DIR / "profiles",
        "ai": TEMPLATES_DIR / "ai",
        "campaigns": TEMPLATES_DIR / "campaigns",
        "iac": TEMPLATES_DIR / "iac",
    }
    
    if category:
        categories = {category: categories.get(category)} if category in categories else {}
    
    for cat_name, cat_path in categories.items():
        if cat_path and cat_path.exists():
            for file_path in cat_path.rglob("*.json"):
                templates.append({
                    "category": cat_name,
                    "name": file_path.stem,
                    "path": str(file_path.relative_to(TEMPLATES_DIR)),
                    "subcategory": file_path.parent.name if file_path.parent != cat_path else None,
                })
            for file_path in cat_path.rglob("*.yaml"):
                templates.append({
                    "category": cat_name,
                    "name": file_path.stem,
                    "path": str(file_path.relative_to(TEMPLATES_DIR)),
                    "subcategory": file_path.parent.name if file_path.parent != cat_path else None,
                })
    
    return templates


def _get_cfn_yaml_loader():
    """Get a YAML loader that handles CloudFormation intrinsic functions."""
    import yaml
    
    class CFNLoader(yaml.SafeLoader):
        pass
    
    # Add constructors for CloudFormation intrinsic functions
    cfn_tags = ['!Ref', '!GetAtt', '!Sub', '!Join', '!If', '!Equals', '!Not', 
                '!And', '!Or', '!Condition', '!FindInMap', '!Select', '!Split',
                '!ImportValue', '!GetAZs', '!Cidr', '!Base64']
    
    def cfn_constructor(loader, tag_suffix, node):
        if isinstance(node, yaml.ScalarNode):
            return {tag_suffix: loader.construct_scalar(node)}
        elif isinstance(node, yaml.SequenceNode):
            return {tag_suffix: loader.construct_sequence(node)}
        elif isinstance(node, yaml.MappingNode):
            return {tag_suffix: loader.construct_mapping(node)}
    
    for tag in cfn_tags:
        CFNLoader.add_multi_constructor(tag, cfn_constructor)
    
    return CFNLoader


def get_template(category: str, name: str, subcategory: str | None = None) -> dict[str, Any]:
    """Load a template by category and name."""
    if subcategory:
        path = TEMPLATES_DIR / category / subcategory / f"{name}.json"
    else:
        path = TEMPLATES_DIR / category / f"{name}.json"
    
    if not path.exists():
        # Try yaml
        yaml_path = path.with_suffix(".yaml")
        if yaml_path.exists():
            import yaml
            with open(yaml_path) as f:
                return yaml.load(f, Loader=_get_cfn_yaml_loader())
        raise FileNotFoundError(f"Template not found: {path}")
    
    with open(path) as f:
        return json.load(f)


def customize_template(template: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    """Apply customizations to a template."""
    result = template.copy()
    
    for key, value in overrides.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = {**result[key], **value}
        else:
            result[key] = value
    
    return result
