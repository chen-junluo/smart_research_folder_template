"""Canonical artifact path registry placeholder.

Use this file to register stable artifact contracts for `intermediate`,
`feature`, and `panel` outputs. Keep it lightweight but explicit so later
pipeline scripts and AI collaborators can reuse the same names and paths.
"""

ARTIFACT_PATHS = {
    "intermediate": {
        "example_intermediate": {
            "path": "data/features/example_intermediate.parquet",
            "grain": "fill_me",
            "keys": ["fill_me"],
            "built_by": "src/panels/build_example_intermediate.py",
            "notes": "Replace with actual intermediate artifact contract.",
        },
    },
    "features": {
        "example_feature": {
            "path": "data/features/example_feature.parquet",
            "grain": "fill_me",
            "keys": ["fill_me"],
            "built_by": "src/features/build_example_feature.py",
            "notes": "Replace with actual feature artifact contract.",
        },
    },
    "panels": {
        "example_panel": {
            "path": "data/panels/example_panel.parquet",
            "grain": "fill_me",
            "keys": ["fill_me"],
            "built_by": "src/panels/build_example_panel.py",
            "notes": "Replace with actual panel artifact contract.",
        },
    },
}
