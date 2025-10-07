export function LoadingSpinner({ label='Loading...' }) {
  return (
    <div style={{display:'flex', alignItems:'center', gap:10, fontSize:14, color:'#475569'}}>
      <div style={{width:16,height:16,border:'3px solid #cbd5e1', borderTopColor:'#134e9b', borderRadius:'50%', animation:'spin 0.9s linear infinite'}} />
      <span>{label}</span>
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </div>
  );
}

export function ErrorMessage({ message }) {
  if(!message) return null;
  return <div style={{padding:12, background:'#fee2e2', border:'1px solid #fecaca', color:'#b91c1c', borderRadius:8, fontSize:13}}>{message}</div>;
}
