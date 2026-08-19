# Challenge: Designing Ambiguity-Resistant Tool Schemas

## Objective

Design an airtight JSON Schema for a multi-tenant cloud provisioning tool that minimizes the probability of LLM hallucinations and invalid argument combinations.

---

## The Scenario

You are exposing a tool `provision_cloud_cluster` to an autonomous infrastructure agent.

### Requirements:
1. **Cloud Provider Constraint**: Must strictly be one of `"aws"`, `"gcp"`, `"azure"`.
2. **Region Validation**: Must follow standard region naming (e.g. `^[a-z]{2}-[a-z]+-[0-9]$` for AWS/GCP).
3. **Node Sizing Constraints**:
   - `min_nodes`: integer between 1 and 50
   - `max_nodes`: integer between `min_nodes` and 100
   - `node_type`: enum of approved compute instances (e.g. `"c6i.xlarge"`, `"m6i.xlarge"`, `"r6i.xlarge"`)
4. **Tagging & Compliance**:
   - `tags`: dictionary of string-to-string mappings
   - Required tag: `"Owner"` (non-empty string)
   - Required tag: `"CostCenter"` (integer string or code)

---

## Challenge Deliverable

- Write a Pydantic v2 model implementing these constraints with model validators (`@model_validator(mode='after')` to ensure `max_nodes >= min_nodes`).
- Justify how each constraint protects against catastrophic cloud billing spikes and configuration drift.
