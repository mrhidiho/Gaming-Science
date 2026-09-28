"""Lesson 40.4 computational slice.

Check evidence-ledger structure. Each claim needs id, tier, artifact, requirement, limitations; known_artifacts is a list of paths. Allowed tiers: analytical, functional_model, cycle_model, synthesis, host_measurement, physical_measurement. Report structural omissions, not scientific approval. Arbitrary unsupported tiers never become measurements by renaming files.
"""
from __future__ import annotations

def solve(case: dict) -> dict:
    allowed={'analytical','functional_model','cycle_model','synthesis','host_measurement','physical_measurement'}
    known=set(case['known_artifacts']); issues=[]; seen=set()
    for record in case['claims']:
        identity=record.get('id','')
        if not identity or identity in seen: issues.append('missing_or_duplicate_id')
        seen.add(identity)
        if record.get('tier') not in allowed: issues.append(identity+':tier')
        if record.get('artifact') not in known: issues.append(identity+':artifact')
        if not record.get('requirement'): issues.append(identity+':requirement')
        if not record.get('limitations'): issues.append(identity+':limitations')
    if not case['claims']: issues.append('empty_ledger')
    return {'issues':sorted(issues),'structurally_complete':not issues}
