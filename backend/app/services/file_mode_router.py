from __future__ import annotations
from pathlib import Path
from typing import Any
from app.models.schemas import MigrationProject

MODE_RULES = {
    '.zip': ('Package', 'Extract package → inventory every member → route each child by extension'),
    '.twbx': ('Packaged Workbook', 'Extract → parse TWB XML → associate extracts/local files/assets'),
    '.tdsx': ('Packaged Data Source', 'Extract → parse TDS XML → recover connections and extract lineage'),
    '.tflx': ('Packaged Prep Flow', 'Extract → parse TFL → recover preparation sequence and outputs'),
    '.twb': ('Workbook Definition', 'Parse workbook XML → sheets/dashboards/stories/data sources/calculations'),
    '.tds': ('Data Source Definition', 'Parse data-source XML → connections/model/fields/filters'),
    '.tfl': ('Prep Flow', 'Parse preparation flow → inputs/cleaning/joins/unions/outputs'),
    '.hyper': ('Hyper Extract', 'Read metadata/preview when API is available; prefer original source for production'),
    '.tde': ('Legacy TDE', 'Recover upstream logic from Tableau metadata; validation/fallback only'),
    '.csv': ('Tabular Source', 'Profile 10 rows → infer types/keys → generate Power Query source'),
    '.xlsx': ('Tabular Source', 'Inspect sheets → profile 10 rows → infer types/keys'),
    '.xls': ('Tabular Source', 'Inspect sheets → profile 10 rows → infer types/keys'),
    '.json': ('Structured Source', 'Inspect schema → normalize records/lists → profile columns'),
    '.xml': ('Structured Source', 'Inspect nodes → map repeating records → profile columns'),
    '.parquet': ('Columnar Source', 'Read schema/statistics → profile sample → generate connector logic'),
    '.sql': ('SQL Logic', 'Review SQL → classify source-side logic → Value.NativeQuery/view recommendation'),
}

TDE_REQUIRED_INFORMATION = [
    'Associated TWB/TWBX/TDS/TDSX/TFL/TFLX metadata',
    'Original source type and connection details',
    'Server/database/schema/table or original file paths',
    'Custom SQL, joins, unions, relationships and source filters',
    'Extract filters, aggregation, row limits and incremental-refresh key',
    'Calculated fields, LOD expressions, table calculations, aliases/groups',
    'Expected columns, datatypes, keys, row counts and business totals',
    'Credentials/gateway details supplied securely outside the package',
]

def build_file_processing_tree(project: MigrationProject) -> list[dict[str, Any]]:
    roots: dict[str, dict[str, Any]] = {}
    for item in project.inventory:
        ext = item.extension.lower()
        mode, process = MODE_RULES.get(ext, ('Manual Review', 'Inventory and classify; do not silently ignore'))
        package = item.folder_path.split('/')[0] if item.folder_path else 'Uploaded files'
        root = roots.setdefault(package, {'id': package, 'label': package, 'node_type': 'package', 'children': []})
        node = {
            'id': f"{package}:{item.folder_path}:{item.file_name}",
            'label': item.file_name,
            'extension': ext,
            'role': item.role,
            'mode': mode,
            'processing_path': process,
            'status': item.parsed_status,
            'warnings': item.warnings,
            'errors': item.errors,
            'children': [],
        }
        if ext == '.tde':
            node['production_source_allowed'] = False
            node['recommended_usage'] = 'Validation baseline or temporary static fallback only'
            node['required_information'] = TDE_REQUIRED_INFORMATION
        root['children'].append(node)
    return list(roots.values())
