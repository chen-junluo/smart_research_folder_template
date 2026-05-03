# - 生成某个 intermediate base table
#   - 输入：raw-like source materials 或上游 standardized artifacts
#   - 输出：一个可被多个 features / panels 复用的 intermediate
#   - grain、merge keys、output path 在实现时明确写清

PIPELINE_SPEC = {
    "kind": "intermediate",
    "notes": "Fill in inputs, outputs, grain, and merge_keys when implementing.",
}
