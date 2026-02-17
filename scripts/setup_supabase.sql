-- v1.8.5 Sovereign Launch: Supabase Schema for 100% Free Telemetry
-- Location: Paste this into the Supabase SQL Editor

-- 1. Create the events table
create table if not exists public.telemetry_events (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default now(),
  event_name text not null,
  user_id text,
  session_id text,
  properties jsonb default '{}'::jsonb,
  context jsonb default '{}'::jsonb
);

-- 2. Enable Row Level Security (RLS)
alter table public.telemetry_events enable row level security;

-- 3. Security Policy: Allow anonymous INSERTS (No reads allowed for anon users)
create policy "Allow anonymous inserts"
on public.telemetry_events
for insert
with check (true);

-- 4. Admin Policy: Allow owner to read and delete (for aggregation/maintenance)
-- (Automatically granted to service_role)

print('✅ SQL Prepared. Please execute in Supabase SQL Editor.');
