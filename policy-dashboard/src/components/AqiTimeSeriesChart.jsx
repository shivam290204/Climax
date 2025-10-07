import { useMemo } from 'react';
import { LineChart, Line, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function AqiTimeSeriesChart({ data }) {
  const chartData = useMemo(()=> (data||[]).map(d=> ({
    time: d.timestamp || d.time || d.date,
    aqi: d.aqi || d.avg_aqi || null,
  })).filter(d=> d.time && d.aqi !== null), [data]);

  if(!chartData.length) return <div className="chart-placeholder">No AQI data</div>;

  return (
    <div style={{width:'100%', height:260}}>
      <ResponsiveContainer>
        <LineChart data={chartData} margin={{top:10,right:20,bottom:5,left:0}}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="time" tick={{fontSize:11}} interval={Math.ceil(chartData.length/8)} />
          <YAxis tick={{fontSize:11}} domain={['auto','auto']} />
          <Tooltip />
          <Line type="monotone" dataKey="aqi" stroke="#134e9b" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
