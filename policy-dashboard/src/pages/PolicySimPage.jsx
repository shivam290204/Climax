import { useState } from 'react';
import { PolicyAPI, SourcesAPI } from '../services/api';

export default function PolicySimPage(){
  const [measure, setMeasure] = useState('traffic_restriction');
  const [intensity, setIntensity] = useState(25);
  const [duration, setDuration] = useState(7);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function runSimulation(e){
    e.preventDefault();
    setError(null);
    try {
      setLoading(true);
      const payload = { measure, intensity: Number(intensity), duration_days: Number(duration) };
      const res = await PolicyAPI.simulate(payload);
      setResult(res);
    } catch(e){
      setError(e.message || 'Simulation failed');
    } finally { setLoading(false); }
  }

  return (
    <div className="page">
      <h2>Policy Simulator</h2>
      <p style={{maxWidth:680}}>Experiment with hypothetical interventions to estimate short-term AQI impact. These results are illustrative (model stub) and should be validated with full causal modeling.</p>

      <form onSubmit={runSimulation} style={{maxWidth:420}}>
        <div className="form-group">
          <label>Measure</label>
          <select value={measure} onChange={e=>setMeasure(e.target.value)}>
            <option value="traffic_restriction">Traffic Restriction (Odd-Even)</option>
            <option value="construction_halt">Construction Halt</option>
            <option value="stubble_management">Enhanced Stubble Mgmt</option>
            <option value="industrial_controls">Industrial Controls</option>
            <option value="dust_suppression">Dust Suppression</option>
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

      {error && <p style={{color:'crimson', marginTop:16}}>{error}</p>}

      {result && (
        <div className="card" style={{marginTop:24}}>
          <h3>Simulation Result</h3>
          <p style={{fontSize:14, color:'#475569'}}>Projected AQI reduction and qualitative impact. (Placeholder model)</p>
          <div style={{display:'flex', gap:32, flexWrap:'wrap'}}>
            <div>
              <div style={{fontSize:12, textTransform:'uppercase', color:'#64748b'}}>Expected Reduction</div>
              <div style={{fontSize:28,fontWeight:600}}>{result.expected_reduction ? (result.expected_reduction*100).toFixed(1)+'%' : '—'}</div>
            </div>
            <div>
              <div style={{fontSize:12, textTransform:'uppercase', color:'#64748b'}}>Confidence</div>
              <div style={{fontSize:28,fontWeight:600}}>{result.confidence || '—'}</div>
            </div>
            <div>
              <div style={{fontSize:12, textTransform:'uppercase', color:'#64748b'}}>Timeframe</div>
              <div style={{fontSize:28,fontWeight:600}}>{result.timeframe || result.duration || duration+'d'}</div>
            </div>
          </div>
          {result.notes && <p style={{marginTop:16}}>{result.notes}</p>}
        </div>
      )}
    </div>
  );
}
