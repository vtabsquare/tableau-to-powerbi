from __future__ import annotations
from pathlib import Path
from typing import Any, Iterable

def model(id: str, name: str, description: str, mandatory: str, optional: str, notes: list[str], readiness: str) -> dict[str, Any]:
    return {'id': id, 'name': name, 'description': description, 'mandatory_files': [x.strip() for x in mandatory.split(';') if x.strip()], 'optional_files': [x.strip() for x in optional.split(';') if x.strip()], 'extraction_notes': notes, 'readiness_note': readiness}

MODELS = [
model('complete_project','Complete Tableau Project','Full migration package with workbook metadata and available source assets.','At least one .twb or .twbx','TDS/TDSX; TFL/TFLX; Hyper/TDE; CSV/Excel/JSON/XML/Parquet; SQL; images; documentation',[
'In Tableau Desktop use File > Save As and choose .twbx to package a workbook.',
'Place all related assets under one root folder before compressing the project as ZIP.',
'Do not place passwords, PAT tokens or private keys inside the package.'],'Best automation and lineage coverage.'),
model('twbx_only','Packaged Workbook Only','A .twbx is supplied without separately uploaded source files.','One .twbx','Original source files; connection notes; data dictionary; validation totals',[
'Open the workbook in Tableau Desktop and use File > Save As > Tableau Packaged Workbook (.twbx).',
'Enable inclusion of external files when Tableau provides that option.',
'For external databases, provide connection metadata separately without secrets.'],'Workbook logic can be parsed; source availability depends on package contents.'),
model('twbx_sources','Packaged Workbook + Source Files','A .twbx plus local files used by the workbook.','One .twbx; all locally referenced source files that are available','TDS/TDSX; extracts; SQL scripts; mapping documents',[
'Save the workbook as .twbx and copy CSV/Excel/JSON/XML/Parquet files into a Sources folder.',
'Keep original filenames and relative folder structure where possible.',
'Zip the .twbx and Sources folder together.'],'Recommended for file-based Tableau workbooks.'),
model('twbx_database','Packaged Workbook + Database Details','A .twbx with live or extract database sources and reconnect information.','One .twbx; database platform; server/host; database; schema/table or custom SQL','Port; warehouse; role; gateway notes; refresh rules; non-secret credential instructions',[
'Download or save the workbook as .twbx.',
'In Tableau review Data > Data Source > Edit Connection and record server, database, schema and authentication type.',
'Export custom SQL separately and never include passwords.'],'Supports source reconstruction after connection details are reviewed.'),
model('twb_only','Workbook Definition Only','An unpackaged Tableau workbook definition without source data.','One .twb','TDS/TDSX; source files; database details; extracts; screenshots',[
'Use Tableau Desktop File > Save As and select Tableau Workbook (.twb).',
'A .twb is XML metadata and normally does not contain source data.',
'Place connection notes beside the .twb when sources cannot be supplied.'],'Good metadata coverage; source mapping is mandatory before production export.'),
model('twb_sources','Workbook + Source Files','An unpackaged .twb and its local source files.','One .twb; all locally referenced source files that are available','TDS/TDSX; extracts; SQL; validation totals',[
'Save as .twb and copy referenced files without renaming them.',
'Preserve relative folder structure to improve automatic matching.',
'Zip the workbook and source folders together.'],'Strong option for transparent file-based migration.'),
model('twb_database','Workbook + Database Details','A .twb plus live database connection and SQL metadata.','One .twb; database platform; server/host; database; schema/table or custom SQL','Port; warehouse; role; gateway; refresh schedule; credential instructions',[
'Save the workbook as .twb.',
'Capture connection metadata from the Tableau Data Source page.',
'Export custom SQL and initial SQL as .sql or .txt.'],'Source validation is required before generating production M.'),
model('datasource_only','Tableau Data Source Only','A TDS/TDSX is supplied without workbook visuals.','One .tds or .tdsx','Source files; extracts; custom SQL; data dictionary',[
'Use Data > data source > Add to Saved Data Sources or save the data source from Tableau.',
'Use .tdsx when local files or extracts must be packaged.',
'Use .tds for XML metadata only.'],'Covers source model, joins and calculations; visuals are unavailable.'),
model('extract_metadata','Extract + Tableau Metadata','A Hyper/TDE extract accompanied by workbook or data-source metadata.','One .hyper or .tde; one associated .twb/.twbx/.tds/.tdsx','Original sources; custom SQL; refresh filters; row-count controls',[
'Locate extracts beside the workbook or in Tableau repository Datasources/Extracts folders.',
'For packaged files, rename a copy of .twbx/.tdsx to .zip and inspect the Data folder.',
'Keep the original package unchanged and upload the extract plus metadata.'],'Good recovery path; the original source remains preferred for production.'),
model('extract_only','Extract Only','Only a Hyper or legacy TDE extract is supplied.','One .hyper or .tde','Source system details; TWB/TDS metadata; SQL; refresh rules; expected totals',[
'Hyper files may be found inside packaged workbooks/data sources or Tableau repository folders.',
'TDE is legacy; locate related metadata using the original package or a compatible Tableau version.',
'Provide a source-build note describing joins, filters and refresh logic.'],'Recovery/manual-mapping mode; unsafe production export remains blocked until lineage is supplied.'),
model('prep_project','Tableau Prep Project','A Tableau Prep flow supplied alone or with workbook/source assets.','One .tfl or .tflx','Input files; output extracts; downstream TWB/TWBX; validation totals',[
'In Tableau Prep Builder use File > Save As and choose .tflx when local inputs can be packaged.',
'Use .tfl for flow metadata only.',
'Include all inputs and representative output samples in the same ZIP.'],'Prep steps can be translated; downstream visual logic requires a workbook.'),
model('partial_project','Partial or Missing-Source Project','Some Tableau assets are available but referenced sources are missing.','At least one Tableau metadata file: .twb/.twbx/.tds/.tdsx/.tfl/.tflx','Missing source files; extracts; database details; SQL; screenshots; validation totals',[
'Upload all available assets first; the application will inventory gaps.',
'Obtain missing items from the workbook owner, Tableau repository, packaged workbook, server download or source control.',
'Document unavailable items instead of substituting guessed files.'],'Guided remediation mode; incomplete items remain clearly flagged.'),
model('server_cloud_export','Tableau Server/Cloud Export Package','Downloaded workbook/data-source packages from Tableau Server or Tableau Cloud.','Downloaded .twbx/.twb and/or .tdsx/.tds','Extracts; source files; site/project inventory; refresh and permission notes',[
'From Tableau Server/Cloud use Download > Tableau Workbook when permitted.',
'Download published data sources separately when they are not embedded.',
'Ask an administrator to enable downloads or export through approved REST API tooling.'],'Processed as exported artifacts; direct server connectivity is not required.'),
model('documentation_assisted','Documentation-Assisted Recovery','Tableau assets supplemented by screenshots, specifications or mapping documents.','At least one Tableau artifact or extract','PDF/Word/Excel mapping; screenshots; data dictionary; KPI rules; sign-off totals',[
'Export dashboards as PDF or image from Tableau for visual reference.',
'Export crosstab data as validation evidence, not as replacement lineage.',
'Include functional specifications and calculation definitions where available.'],'Adds migration evidence; documentation alone cannot guarantee executable conversion.'),
]
MODEL_BY_ID = {m['id']: m for m in MODELS}

def catalogue() -> list[dict[str, Any]]:
    return MODELS

def _extensions(items: Iterable[Any]) -> set[str]:
    result: set[str] = set()
    for item in items:
        ext = getattr(item, 'extension', None) or Path(getattr(item, 'file_name', '')).suffix
        if ext: result.add(ext.lower())
    return result

def detect_upload_model(items: Iterable[Any]) -> dict[str, Any]:
    exts = _extensions(items)
    has = lambda *x: any(e in exts for e in x)
    meta = has('.twb','.twbx','.tds','.tdsx','.tfl','.tflx')
    workbook, package_wb = has('.twb','.twbx'), has('.twbx')
    datasource, prep, extract = has('.tds','.tdsx'), has('.tfl','.tflx'), has('.hyper','.tde')
    local_sources = has('.csv','.xlsx','.xls','.json','.xml','.parquet','.txt','.tsv')
    docs, sql = has('.pdf','.doc','.docx','.png','.jpg','.jpeg'), has('.sql')
    if workbook and (datasource or prep or extract) and (local_sources or sql): mid='complete_project'
    elif package_wb and local_sources: mid='twbx_sources'
    elif package_wb and not local_sources and not extract: mid='twbx_only'
    elif has('.twb') and local_sources: mid='twb_sources'
    elif has('.twb') and not local_sources and not extract: mid='twb_only'
    elif datasource and not workbook and not prep and not extract: mid='datasource_only'
    elif extract and meta: mid='extract_metadata'
    elif extract and not meta: mid='extract_only'
    elif prep and not workbook: mid='prep_project'
    elif docs and meta: mid='documentation_assisted'
    elif meta: mid='partial_project'
    else: mid='partial_project'
    m = MODEL_BY_ID[mid]
    missing: list[str] = []
    if mid in {'twb_only','twbx_only','partial_project'}: missing.append('Original source files or complete database connection metadata')
    if mid == 'extract_only': missing += ['Associated Tableau metadata', 'Original source lineage and refresh logic']
    if '.tde' in exts: missing.append('TDE build logic or original upstream source details')
    return {**m, 'model_id': m['id'], 'model_name': m['name'], 'detected_extensions': sorted(exts), 'missing_information': missing, 'confidence': .95 if mid not in {'partial_project','documentation_assisted'} else .78}
