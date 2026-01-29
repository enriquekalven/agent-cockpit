import React, { useState } from 'react';
import { Routes, Route, Link, Navigate, Outlet } from 'react-router-dom';
import { Activity } from 'lucide-react';
import { A2UISurfaceRenderer } from './a2ui/A2UIRenderer';
import { DocLayout } from './docs/DocLayout';
import { DocPage } from './docs/DocPage';
import { DocHome } from './docs/DocHome';
import { ThemeToggle } from './components/ThemeToggle';
import { Home } from './components/Home';
import { OpsDashboard } from './components/OpsDashboard';
import { ReportSamples } from './components/ReportSamples';

import './index.css';

// AgentOps Cockpit version: Playground removed.


function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route path="/docs" element={<DocLayout />}>
        <Route index element={<DocHome />} />
        <Route path=":docId" element={<DocPage />} />
      </Route>


      <Route path="/ops" element={<OpsDashboard />} />
      
      <Route path="/samples" element={<ReportSamples />} />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
