export default function Section({ title, description, children, actions }) {
  return (
    <section className="mt" style={{marginTop:28}}>
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'flex-end', gap:16, flexWrap:'wrap'}}>
        <div>
          <h3 style={{margin:'0 0 4px 0'}}>{title}</h3>
          {description && <p style={{margin:'0 0 12px 0', fontSize:13, color:'#64748b'}}>{description}</p>}
        </div>
        {actions && <div style={{display:'flex', gap:8}}>{actions}</div>}
      </div>
      {children}
    </section>
  );
}
