import { useEffect, useState } from 'react';
import { PolicyAPI, AlertsAPI, HealthAPI } from '../services/api';

export default function ReportsPage(){
  const [ongoing, setOngoing] = useState([]);
  const [emergency, setEmergency] = useState([]);
  const [healthAlerts, setHealthAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(()=>{
    async function load(){
      try {
        setLoading(true);
        const [og, em, ha] = await Promise.all([
          PolicyAPI.ongoing(),
          PolicyAPI.emergency(),
          AlertsAPI.active().catch(()=>[])
        ]);
        setOngoing(og.interventions || og);
        setEmergency(em.measures || em);
        setHealthAlerts(ha.alerts || ha);
      } catch(e){
        setError(e.message || 'Failed to load reports');
      } finally { setLoading(false); }
    }
    load();
  },[]);

  if (loading) return <div className="page"><h2>Reports & Interventions</h2><p>Loading...</p></div>;
  if (error) return <div className="page"><h2>Reports & Interventions</h2><p style={{color:'crimson'}}>{error}</p></div>;

  return (
    <div className="page">
      <h2>Reports & Interventions</h2>

      <div className="mt">
        <h3>Ongoing Interventions</h3>
        <table className="table">
          <thead><tr><th>Measure</th><th>Status</th><th>Expected Impact</th></tr></thead>
          <tbody>
            {ongoing.map((i,idx)=>(
              <tr key={idx}><td>{i.name || i.measure}</td><td>{i.status || 'active'}</td><td>{i.expected_impact || '—'}</td></tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt">
        <h3>Emergency Actions</h3>
        <table className="table">
          <thead><tr><th>Action</th><th>Trigger</th><th>Notes</th></tr></thead>
          <tbody>
            {emergency.map((m,idx)=>(
              <tr key={idx}><td>{m.action || m.measure}</td><td>{m.trigger || m.reason || '—'}</td><td>{m.notes || '—'}</td></tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt">
        <h3>Active Alerts</h3>
        {healthAlerts.length === 0 && <p>No active alerts.</p>}
        {healthAlerts.length>0 && (
          <table className="table">
            <thead><tr><th>Type</th><th>Severity</th><th>Message</th></tr></thead>
            <tbody>
              {healthAlerts.map((a,i)=> <tr key={i}><td>{a.type}</td><td>{a.severity}</td><td>{a.message}</td></tr>)}
            </tbody>
          </table>
        )}
      </div>

      <div className="mt">
        <h3>Export (Coming Soon)</h3>
        <p style={{color:'#64748b'}}>Download structured PDF/CSV reports for policy review sessions. This feature will aggregate source trends, intervention outcomes, exposure risk metrics and recommended action bundles.</p>
      </div>
    </div>
  );
}
