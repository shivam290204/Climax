import { useEffect, useState } from 'react';
import { ForecastAPI, SourcesAPI, PolicyAPI } from '../services/api';

export default function OverviewPage() {
  const [current, setCurrent] = useState(null);
  const [sources, setSources] = useState([]);
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(()=>{
    async function load() {
      try {
        setLoading(true);
        const [c, s, r] = await Promise.all([
          ForecastAPI.current(),
          SourcesAPI.current(),
          PolicyAPI.recommendations()
        ]);
        setCurrent(c);
        setSources(s.sources || s);
        setRecs(r.recommendations || r);
      } catch(e){
        setError(e.message || 'Failed to load overview data');
      } finally { setLoading(false); }
    }
    load();
  },[]);

  if (loading) return <div className="page"><h2>Overview</h2><p>Loading...</p></div>;
  if (error) return <div className="page"><h2>Overview</h2><p style={{color:'crimson'}}>{error}</p></div>;

  const aqi = current?.aqi;
  const category = current?.category;

  return (
    <div className="page">
      <h2>Overview</h2>
      <div className="cards">
        <div className="card">
          <h3>Current AQI</h3>
          <div style={{fontSize:34, fontWeight:700}}>{aqi ?? '—'}</div>
          <div className="badge" style={{marginTop:8}}>{category}</div>
        </div>
        <div className="card">
          <h3>Primary Source</h3>
          <div style={{fontSize:15}}>{sources?.[0]?.source_type || 'N/A'}</div>
          <div style={{fontSize:12, color:'#64748b'}}>{sources?.[0] ? (sources[0].contribution*100).toFixed(1)+ '%' : ''}</div>
        </div>
        <div className="card">
          <h3>Interventions</h3>
            <div style={{fontSize:28,fontWeight:600}}>{recs.length}</div>
            <div style={{fontSize:12,color:'#64748b'}}>Recommended actions</div>
        </div>
        <div className="card">
          <h3>Data Timestamp</h3>
          <div>{current?.timestamp ? new Date(current.timestamp).toLocaleString() : '—'}</div>
        </div>
      </div>

      <div className="mt">
        <h3>Top Sources</h3>
        <table className="table">
          <thead><tr><th>Source</th><th>Contribution</th></tr></thead>
          <tbody>
            {sources.slice(0,8).map((s,i)=> (
              <tr key={i}><td>{s.source_type}</td><td>{(s.contribution*100).toFixed(1)}%</td></tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt">
        <h3>Policy Recommendations</h3>
        <div className="grid" style={{gridTemplateColumns:'repeat(auto-fill,minmax(280px,1fr))'}}>
          {recs.map((r,i)=> (
            <div key={i} className="card" style={{display:'flex',flexDirection:'column'}}>
              <strong>{r.title || r.measure || ('Recommendation '+(i+1))}</strong>
              <span style={{fontSize:12, color:'#64748b', margin:'6px 0'}}>{r.description || r.type || ''}</span>
              {r.expected_impact && <span className="badge">Impact: {r.expected_impact}</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
