import { useEffect, useState } from 'react';
import { SourcesAPI } from '../services/api';

export default function SourcesPage(){
  const [current, setCurrent] = useState([]);
  const [regional, setRegional] = useState([]);
  const [fires, setFires] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(()=>{
    async function load(){
      try {
        setLoading(true);
        const [c, r, f] = await Promise.all([
          SourcesAPI.current(),
          SourcesAPI.regional(),
          SourcesAPI.fires()
        ]);
        setCurrent(c.sources || c);
        setRegional(r.regional || r);
        setFires(f.fires || f);
      } catch(e){
        setError(e.message || 'Failed to load sources');
      } finally { setLoading(false); }
    }
    load();
  },[]);

  if (loading) return <div className="page"><h2>Source Attribution</h2><p>Loading...</p></div>;
  if (error) return <div className="page"><h2>Source Attribution</h2><p style={{color:'crimson'}}>{error}</p></div>;

  return (
    <div className="page">
      <h2>Source Attribution</h2>
      <div className="cards">
        <div className="card">
          <h3>Top Source Now</h3>
          <div style={{fontSize:18}}>{current?.[0]?.source_type || 'N/A'}</div>
          <div style={{fontSize:12,color:'#64748b'}}>{current?.[0] ? (current[0].contribution*100).toFixed(1)+'%' : ''}</div>
        </div>
        <div className="card">
          <h3>Active Fires</h3>
          <div style={{fontSize:32,fontWeight:600}}>{fires.length}</div>
          <div style={{fontSize:12,color:'#64748b'}}>Detected hotspots</div>
        </div>
      </div>

      <div className="mt">
        <h3>Current Source Mix</h3>
        <div className="chart-placeholder">Pie / Bar chart placeholder</div>
        <table className="table" style={{marginTop:16}}>
          <thead><tr><th>Source</th><th>Contribution</th></tr></thead>
          <tbody>
            {current.map((s,i)=> <tr key={i}><td>{s.source_type}</td><td>{(s.contribution*100).toFixed(1)}%</td></tr>)}
          </tbody>
        </table>
      </div>

      <div className="mt">
        <h3>Regional Transport</h3>
        <table className="table">
          <thead><tr><th>Region</th><th>Contribution</th></tr></thead>
          <tbody>
            {regional.map((s,i)=> <tr key={i}><td>{s.region || s.source_type}</td><td>{((s.contribution||0)*100).toFixed(1)}%</td></tr>)}
          </tbody>
        </table>
      </div>

      <div className="mt">
        <h3>Fire Hotspots (sample)</h3>
        <table className="table">
          <thead><tr><th>Lat</th><th>Lon</th><th>Confidence</th></tr></thead>
          <tbody>
            {fires.slice(0,40).map((f,i)=> <tr key={i}><td>{f.latitude?.toFixed(2)}</td><td>{f.longitude?.toFixed(2)}</td><td>{f.confidence || '—'}</td></tr>)}
          </tbody>
        </table>
      </div>
    </div>
  );
}
