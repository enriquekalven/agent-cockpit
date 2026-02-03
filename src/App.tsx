import React, { useState, Suspense, lazy } from 'react';
import { Routes, Route, Link, Navigate, Outlet } from 'react-router-dom';
import { Activity } from 'lucide-react';

// Dynamic Imports for Code Splitting (v1.0 Architecture Optimization)
const DocLayout = lazy(() => import('./docs/DocLayout').then(m => ({ default: m.DocLayout })));
const DocPage = lazy(() => import('./docs/DocPage').then(m => ({ default: m.DocPage })));
const DocHome = lazy(() => import('./docs/DocHome').then(m => ({ default: m.DocHome })));
const Home = lazy(() => import('./components/Home').then(m => ({ default: m.Home })));
const ReportSamples = lazy(() => import('./components/ReportSamples').then(m => ({ default: m.ReportSamples })));

import { A2UISurfaceRenderer } from './a2ui/A2UIRenderer';
import { ThemeToggle } from './components/ThemeToggle';

import './index.css';

// AgentOps Cockpit version: Playground removed.


function App() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center min-h-screen bg-slate-950">
        <Activity className="w-8 h-8 text-blue-500 animate-spin" />
      </div>
    }>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/docs" element={<DocLayout />}>
          <Route index element={<DocHome />} />
          <Route path=":docId" element={<DocPage />} />
        </Route>

        <Route path="/samples" element={<ReportSamples />} />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}

export default App;
