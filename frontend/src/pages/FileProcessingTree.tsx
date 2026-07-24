import { useState } from 'react';
import { ChevronDown, ChevronRight, FileArchive, FileCode2, Database, AlertTriangle } from 'lucide-react';
import { Card, Badge } from '../components/Cards';
import { MigrationProject } from '../types/project';

function Node({node, depth=0}: {node:any; depth?:number}) {
  const [open, setOpen] = useState(depth < 1);
  const children = node.children || [];
  return <div className="treeNode" style={{marginLeft: depth * 18}}>
    <button className="treeRow" onClick={() => setOpen(!open)}>
      <span>{children.length ? (open ? <ChevronDown size={16}/> : <ChevronRight size={16}/>) : <span className="treeSpacer"/>}</span>
      {node.node_type === 'package' ? <FileArchive size={18}/> : node.extension === '.tde' || node.extension === '.hyper' ? <Database size={18}/> : <FileCode2 size={18}/>} 
      <b>{node.label}</b><span className="treeMode">{node.mode || node.node_type}</span><Badge tone={node.errors?.length ? 'bad' : node.warnings?.length ? 'warn' : 'good'}>{node.status || 'Detected'}</Badge>
    </button>
    {open && node.processing_path && <div className="treeDetail"><b>Processing route:</b> {node.processing_path}
      {node.extension === '.tde' && <><div className="tdeTreeRule"><AlertTriangle size={16}/> TDE is not a production source. Recover its original source and use TDE only for validation/fallback.</div><b>Required supporting information</b><ul>{(node.required_information || []).map((x:string) => <li key={x}>{x}</li>)}</ul></>}
    </div>}
    {open && children.map((c:any) => <Node key={c.id} node={c} depth={depth+1}/>)}
  </div>
}
export default function FileProcessingTree({project}:{project:MigrationProject}) {
 return <div className="page"><Card title="File Mode Processing Tree" right={<Badge tone="neutral">{project.inventory.length} inventoried files</Badge>}>
   <div className="note">Every uploaded file is routed by its type. Packages are expanded first, then workbook definitions, data sources, extracts, preparation flows, source files, SQL, and assets are processed by their dedicated pipeline mode.</div>
   <div className="treePanel">{(project.file_processing_tree || []).map((n:any) => <Node key={n.id} node={n}/>)}</div>
 </Card></div>;
}
