from __future__ import annotations
from app.core.name_sanitizer import clean_name

TEMP_MARKERS = ('temp', 'tmp', 'staging', 'stage', 'intermediate', 'helper', 'join_payload', 'union_payload', 'anonymous')

def is_model_table(mapping) -> tuple[bool, str]:
    text = ' '.join(str(x or '') for x in [mapping.datasource, mapping.table_name, mapping.mapping_status, mapping.original_connection_type]).lower()
    if '.tde' in text or 'legacy tde' in text:
        return False, 'Legacy TDE is validation/fallback only.'
    if any(marker in text for marker in TEMP_MARKERS):
        return False, 'Temporary/intermediate/join-payload table excluded from semantic model.'
    if str(mapping.parameter_values.get('include_in_model', 'true')).lower() == 'false':
        return False, 'Explicitly excluded from semantic model.'
    return True, 'Final/source-backed model table.'

def clean_join_expansion_columns(columns: list[dict]) -> list[dict]:
    """Remove duplicate technical payload columns after joins while preserving business keys."""
    result, seen = [], set()
    for column in columns:
        name = clean_name(column.get('name') or column.get('source_name') or '')
        source = clean_name(column.get('source_name') or name)
        normalized = name.lower()
        technical_duplicate = normalized.endswith(('_1', '_2', '.1', '.2')) or normalized.startswith(('joined_', 'expanded_'))
        if normalized in seen and technical_duplicate:
            continue
        # keep only one exact duplicate; key columns remain because their first occurrence is retained
        if normalized in seen:
            continue
        seen.add(normalized)
        column['name'] = name
        column['source_name'] = source
        result.append(column)
    return result
