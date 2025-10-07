export default function KpiCard({ title, value, subtitle, badge, color }) {
  return (
    <div className="card" style={{borderTop: color ? `4px solid ${color}` : undefined}}>
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'flex-start'}}>
        <div>
          <div style={{fontSize:12, textTransform:'uppercase', letterSpacing:0.5, color:'#64748b', fontWeight:600}}>{title}</div>
          <div style={{fontSize:30, fontWeight:700, lineHeight:1.1, marginTop:4}}>{value ?? '—'}</div>
          {subtitle && <div style={{fontSize:12, color:'#64748b', marginTop:4}}>{subtitle}</div>}
        </div>
        {badge && <span className="badge" style={{background:'#134e9b', color:'#fff'}}>{badge}</span>}
      </div>
    </div>
  );
}
