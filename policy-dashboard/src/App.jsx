import React from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';
import OverviewPage from './pages/OverviewPage';
import ForecastPage from './pages/ForecastPage';
import SourcesPage from './pages/SourcesPage';
import PolicySimPage from './pages/PolicySimPage';
import ReportsPage from './pages/ReportsPage';

export default function App() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <h1 className="logo">Policy Dashboard</h1>
        <nav>
          <NavLink to="/" end>Overview</NavLink>
          <NavLink to="/forecast">Forecasting</NavLink>
            <NavLink to="/sources">Sources</NavLink>
            <NavLink to="/policy">Policy Simulator</NavLink>
            <NavLink to="/reports">Reports</NavLink>
        </nav>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/forecast" element={<ForecastPage />} />
          <Route path="/sources" element={<SourcesPage />} />
          <Route path="/policy" element={<PolicySimPage />} />
          <Route path="/reports" element={<ReportsPage />} />
        </Routes>
      </main>
    </div>
  );
}
