# - 在某个 intermediate 上 late merge 多个 compact features，生成 final panel
#   - 不要在本文件里重复生成已可独立生成的 feature
#   - 这个文件的职责应集中在 panel assembly

PIPELINE_SPEC = {
    "kind": "panel",
    "notes": "Fill in reads_intermediate, reads_features, writes_panel, grain, and merge_keys when implementing.",
}
