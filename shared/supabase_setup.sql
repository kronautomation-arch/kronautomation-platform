-- ════════════════════════════════════════════════════
-- Kronautomation — Setup inicial de Supabase
-- ════════════════════════════════════════════════════
-- Ejecutar en: Supabase Dashboard → SQL Editor → New query
-- Una sola vez al crear el proyecto.

-- 1) Tabla de usuarios autorizados por proyecto
create table if not exists public.app_users (
  id          uuid primary key default gen_random_uuid(),
  email       text not null,
  project     text not null,        -- bareno | marfil | research | seo | cerebro | metric
  role        text default 'viewer', -- viewer | admin
  created_at  timestamptz default now(),
  unique (email, project)
);

-- 2) RLS — solo el dueño del email puede leer su propio registro
alter table public.app_users enable row level security;

create policy "users can read own row"
  on public.app_users for select
  using ( auth.jwt() ->> 'email' = email );

-- 3) Helper: crear usuario en auth.users + insertar en app_users
-- ⚠️ Esto se hace desde la consola de Supabase Authentication → Add user
--    Luego corres el INSERT correspondiente acá.
--
-- Ejemplo para dar acceso al asistente del Dr. Bareño:
--   1. Auth → Add user → email + password
--   2. Volver acá y correr:
--      insert into public.app_users (email, project, role)
--      values ('asistente.bareno@correo.com', 'bareno', 'viewer');
--
-- Si un usuario debe acceder a varios proyectos, repetir el INSERT con
-- diferentes valores de `project`.

-- 4) Verificar
-- select * from public.app_users;
