import { CheckCircle2, CircleHelp, FileArchive, Info } from 'lucide-react';
import { Card, Badge } from '../components/Cards';
import { MigrationProject, UploadModelDefinition } from '../types/project';

function ModelCard({ model, detected }: { model: UploadModelDefinition; detected: boolean }) {
  return <div className={`modelCard ${detected ? 'detectedModel' : ''}`}>
    <div className="modelHeader">
      <div><h3>{model.name}</h3><p>{model.description}</p></div>
      {detected && <Badge tone="good">Detected</Badge>}
    </div>
    <div className="modelColumns">
      <section><h4><CheckCircle2 size={16}/> Mandatory</h4>{model.mandatory_files.map((x,i)=><div className="requirementRow" key={i}>{x}</div>)}</section>
      <section><h4><CircleHelp size={16}/> Optional / Recommended</h4>{model.optional_files.map((x,i)=><div className="requirementRow optional" key={i}>{x}</div>)}</section>
    </div>
    <details><summary><FileArchive size={16}/> How to obtain or extract these files</summary>
      <ol>{model.extraction_notes.map((x,i)=><li key={i}>{x}</li>)}</ol>
    </details>
    <div className="readinessNote"><Info size={15}/>{model.readiness_note}</div>
  </div>
}

export default function UploadModels({ project }: { project?: MigrationProject }) {
  const models = project?.upload_model_catalogue || [];
  const detected = project?.upload_model;
  return <div className="page">
    <Card title="Customer Upload Models" right={detected?.model_name ? <Badge tone="good">{detected.model_name}</Badge> : undefined}>
      <p className="lead">The application classifies the uploaded assets as a migration model, then shows what is mandatory, optional and still missing. Passwords and access tokens must never be uploaded in a package.</p>
      {detected?.model_name && <div className="detectedPanel">
        <div><b>Detected model</b><h2>{detected.model_name}</h2><p>{detected.description}</p></div>
        <div><b>Confidence</b><h2>{Math.round((detected.confidence || 0) * 100)}%</h2><p>{detected.readiness_note}</p></div>
        <div><b>Detected extensions</b><p>{(detected.detected_extensions || []).join(', ') || 'None'}</p></div>
        <div><b>Missing information</b>{detected.missing_information?.length ? <ul>{detected.missing_information.map((x,i)=><li key={i}>{x}</li>)}</ul> : <p>Nothing mandatory detected as missing.</p>}</div>
      </div>}
    </Card>
    <Card title={`${models.length || 14} Supported Upload Models`}>
      <div className="modelGrid">{models.map(m => <ModelCard key={m.id} model={m} detected={m.id === detected?.model_id}/>)}</div>
      {!models.length && <div className="note">Upload a project to load the model catalogue and automatic classification.</div>}
    </Card>
  </div>;
}
