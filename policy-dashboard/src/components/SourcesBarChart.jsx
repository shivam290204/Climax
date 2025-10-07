import { useMemo } from 'react';
import { BarChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Bar, ResponsiveContainer } from 'recharts';

export default function SourcesBarChart({ data }) {
  const rows = useMemo(()=> (data||[]).map(d=> ({
    source: d.source_type || d.region || 'Unknown',
    contribution: Number(((d.contribution||0)*100).toFixed(2))
  })), [data]);

  if(!rows.length) return <div className="chart-placeholder">No source data</div>;

  return (
    <div style={{width:'100%', height:260}}>
      <ResponsiveContainer>
        <BarChart data={rows} margin={{top:10,right:20,left:0,bottom:5}}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="source" tick={{fontSize:11}} interval={0} angle={-20} textAnchor="end" height={60} />
          <YAxis tick={{fontSize:11}} domain={[0,100]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="contribution" name="Contribution %" fill="#2563eb" radius={[4,4,0,0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
