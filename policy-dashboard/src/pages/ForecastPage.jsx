import { useEffect, useState } from 'react';
import { ForecastAPI } from '../services/api';

export default function ForecastPage(){
  const [current, setCurrent] = useState(null);
  const [hyperlocal, setHyperlocal] = useState(null);
  const [historical, setHistorical] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(()=>{
    async function load(){
      try {
        setLoading(true);
        const now = new Date();
        const start = new Date(now.getTime() - 24*3600*1000).toISOString();
        const end = now.toISOString();
        const [c, h, hist] = await Promise.all([
          ForecastAPI.current(),
          ForecastAPI.hyperlocal(28.6139, 77.2090),
          ForecastAPI.historical(start, end)
        ]);
        setCurrent(c);
        setHyperlocal(h);
        setHistorical(hist?.data || hist || []);
      } catch(e){
        setError(e.message || 'Failed to load forecast data');
      } finally { setLoading(false); }
    }
    load();
  },[]);

  if (loading) return <div className="page"><h2>Forecast & Historical</h2><p>Loading...</p></div>;
  if (error) return <div className="page"><h2>Forecast & Historical</h2><p style={{color:'crimson'}}>{error}</p></div>;

  return (
    <div className="page">
      <h2>Forecast & Historical</h2>
      <div className="cards">
        <div className="card">
          <h3>Current AQI</h3>
          <div style={{fontSize:30,fontWeight:600}}>{current?.aqi ?? '—'}</div>
          <div className="badge" style={{marginTop:6}}>{current?.category}</div>
        </div>
        <div className="card">
          <h3>Hyperlocal (Connaught Place)</h3>
          <div style={{fontSize:30,fontWeight:600}}>{hyperlocal?.aqi ?? '—'}</div>
          <div className="badge" style={{marginTop:6}}>{hyperlocal?.category}</div>
        </div>
        <div className="card">
          <h3>Forecast Horizon</h3>
          <div style={{fontSize:30,fontWeight:600}}>{current?.forecast_horizon_hours || 72}h</div>
          <div style={{fontSize:12,color:'#64748b'}}>Model horizon</div>
        </div>
      </div>

      <div className="mt">
        <h3>Historical (Past 24h)</h3>
        <div className="chart-placeholder">Time-series chart placeholder (Recharts to be added)</div>
        <table className="table" style={{marginTop:16}}>
          <thead><tr><th>Timestamp</th><th>AQI</th><th>PM2.5</th><th>PM10</th></tr></thead>
          <tbody>
            {historical.slice(0,50).map((r,i)=> (
              <tr key={i}>
                <td>{r.timestamp ? new Date(r.timestamp).toLocaleTimeString() : '—'}</td>
                <td>{r.aqi ?? '—'}</td>
                <td>{r.pm25 ?? '—'}</td>
                <td>{r.pm10 ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
