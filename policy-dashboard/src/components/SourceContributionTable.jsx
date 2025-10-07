export default function SourceContributionTable({ data }) {
  if(!data || data.length === 0) return <p style={{color:'#64748b'}}>No source data available.</p>;
  return (
    <table className="table">
      <thead><tr><th>Source</th><th style={{textAlign:'right'}}>Contribution</th></tr></thead>
      <tbody>
        {data.map((s,i)=> (
          <tr key={i}>
            <td>{s.source_type || s.region || 'Unknown'}</td>
            <td style={{textAlign:'right'}}>{((s.contribution||0)*100).toFixed(1)}%</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
