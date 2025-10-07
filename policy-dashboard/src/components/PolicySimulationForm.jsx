import { useState } from 'react';

const MEASURES = [
  { value:'traffic_restriction', label:'Traffic Restriction (Odd-Even)'},
  { value:'construction_halt', label:'Construction Halt'},
  { value:'stubble_management', label:'Enhanced Stubble Mgmt'},
  { value:'industrial_controls', label:'Industrial Controls'},
  { value:'dust_suppression', label:'Dust Suppression'}
];

export default function PolicySimulationForm({ onRun, loading }) {
  const [measure, setMeasure] = useState(MEASURES[0].value);
  const [intensity, setIntensity] = useState(25);
  const [duration, setDuration] = useState(7);

  function submit(e){
    e.preventDefault();
    onRun?.({ measure, intensity:Number(intensity), duration_days:Number(duration) });
  }

  return (
    <form onSubmit={submit} style={{maxWidth:420}}>
      <div className="form-group">
        <label>Measure</label>
        <select value={measure} onChange={e=>setMeasure(e.target.value)}>
          {MEASURES.map(m=> <option key={m.value} value={m.value}>{m.label}</option>)}
        </select>
      </div>
      <div className="form-group">
        <label>Intensity (%)</label>
        <input type="number" min={1} max={100} value={intensity} onChange={e=>setIntensity(e.target.value)} />
      </div>
      <div className="form-group">
        <label>Duration (days)</label>
        <input type="number" min={1} max={60} value={duration} onChange={e=>setDuration(e.target.value)} />
      </div>
      <button disabled={loading}>{loading ? 'Running...' : 'Run Simulation'}</button>
    </form>
  );
}
